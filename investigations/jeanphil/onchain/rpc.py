"""Client JSON-RPC Solana minimal, avec cache disque et retries.

Aucune dépendance externe : urllib + json. Le cache évite de re-télécharger
les transactions (qui sont immuables une fois finalisées).
"""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request

DEFAULT_RPC = "https://api.mainnet-beta.solana.com"


class Rpc:
    def __init__(self, url=None, cache_dir=None, min_interval=0.12, max_retries=6):
        self.url = url or os.environ.get("SOLANA_RPC_URL", DEFAULT_RPC)
        self.cache_dir = cache_dir
        self.min_interval = min_interval
        self.max_retries = max_retries
        self._last = 0.0
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    # --- bas niveau -------------------------------------------------------
    def call(self, method, params, cacheable=False):
        key = None
        if cacheable and self.cache_dir:
            key = hashlib.sha1(json.dumps([method, params], sort_keys=True).encode()).hexdigest()
            path = os.path.join(self.cache_dir, key[:2], key + ".json")
            if os.path.exists(path):
                with open(path) as f:
                    return json.load(f)
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
        delay = 1.0
        for attempt in range(self.max_retries):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            try:
                req = urllib.request.Request(self.url, data=body, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = json.load(r)
                if "error" in data:
                    err = data["error"]
                    # -32429 / 429 : rate limit ; -32004/-32007 : bloc indisponible
                    if attempt < self.max_retries - 1 and err.get("code") in (-32429, 429, -32005, -32004):
                        time.sleep(delay)
                        delay *= 2
                        continue
                    raise RuntimeError(f"RPC {method} error: {err}")
                result = data.get("result")
                if key and result is not None:
                    path = os.path.join(self.cache_dir, key[:2], key + ".json")
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w") as f:
                        json.dump(result, f)
                return result
            except (urllib.error.URLError, TimeoutError, ConnectionError):
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(delay)
                delay *= 2
        raise RuntimeError("unreachable")

    # --- helpers ----------------------------------------------------------
    def signatures(self, address, until_time=None, since_time=None, limit_total=None):
        """Toutes les signatures d'une adresse, des plus récentes aux plus anciennes.

        since_time : on s'arrête quand blockTime < since_time.
        until_time : on ignore les signatures dont blockTime > until_time
        (elles sont quand même paginées, getSignaturesForAddress ne sait pas
        démarrer à une date).
        """
        out, before = [], None
        while True:
            opts = {"limit": 1000}
            if before:
                opts["before"] = before
            page = self.call("getSignaturesForAddress", [address, opts])
            if not page:
                break
            for s in page:
                bt = s.get("blockTime")
                if since_time is not None and bt is not None and bt < since_time:
                    return out
                if until_time is not None and bt is not None and bt > until_time:
                    continue
                out.append(s)
                if limit_total and len(out) >= limit_total:
                    return out
            before = page[-1]["signature"]
            if len(page) < 1000:
                break
        return out

    def oldest_signatures(self, address, n=50):
        """Les n plus anciennes signatures (pour retrouver le financement initial)."""
        allsigs = self.signatures(address)
        return list(reversed(allsigs))[:n]

    def tx(self, signature):
        return self.call(
            "getTransaction",
            [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}],
            cacheable=True,
        )

    def token_supply(self, mint):
        return self.call("getTokenSupply", [mint])

    def largest_accounts(self, mint):
        return self.call("getTokenLargestAccounts", [mint])

    def token_accounts_by_owner(self, owner, mint):
        return self.call("getTokenAccountsByOwner", [owner, {"mint": mint}, {"encoding": "jsonParsed"}])

    def balance(self, address):
        return self.call("getBalance", [address])
