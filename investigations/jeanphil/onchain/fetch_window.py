#!/usr/bin/env python3
"""Télécharge toutes les transactions (complètes, jsonParsed) d'une adresse
dans l'ordre chronologique, entre deux instants, via la méthode Helius
getTransactionsForAddress. Sortie : JSONL (une tx par ligne).

  python3 fetch_window.py ADDRESS START_UNIX END_UNIX out.jsonl [--token-accounts]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rpc import Rpc  # noqa: E402


def fetch(rpc, address, start, end, out_path, token_accounts=False, max_tx=None):
    n, tok = 0, None
    with open(out_path, "w") as out:
        while True:
            o = {"transactionDetails": "full", "sortOrder": "asc", "limit": 100, "encoding": "jsonParsed",
                 "maxSupportedTransactionVersion": 1,
                 "filters": {"blockTime": {"gte": start, "lte": end}}}
            if token_accounts:
                o["filters"]["tokenAccounts"] = "balanceChanged"
            if tok:
                o["paginationToken"] = tok
            res = rpc.call("getTransactionsForAddress", [address, o])
            for tx in res.get("data", []):
                out.write(json.dumps(tx) + "\n")
                n += 1
            tok = res.get("paginationToken")
            if n % 1000 < 100:
                print(f"  {n} tx", file=sys.stderr, flush=True)
            if not tok or not res.get("data") or (max_tx and n >= max_tx):
                break
    return n


if __name__ == "__main__":
    a = sys.argv
    print(fetch(Rpc(), a[1], int(a[2]), int(a[3]), a[4], "--token-accounts" in a))
