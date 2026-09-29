#!/usr/bin/env python3
"""Réglages du token, référencements et actions signées par le créateur.
Ajoute la clé "setup" à facts.json.

  python3 creator_setup.py ../data/jeanphil
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import instruction_names, native_deltas, sol_deltas_by_owner  # noqa: E402
from rpc import Rpc  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
IPFS_GATEWAYS = ["https://gateway.pinata.cloud/ipfs/", "https://ipfs.io/ipfs/"]
NOISE = {"GetAccountDataSize", "InitializeImmutableOwner", "InitializeAccount3"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.load(r)
    except Exception as ex:  # noqa: BLE001
        return {"_error": str(ex)}


def main():
    d = sys.argv[1]
    path = os.path.join(d, "facts.json")
    with open(path) as f:
        F = json.load(f)
    rpc = Rpc()
    mint, C = F["mint"], F["creation"]["signers"][0]
    info = rpc.account_info(mint)["value"]["data"]["parsed"]["info"]
    ext = {e["extension"]: e.get("state") for e in info.get("extensions", [])}
    meta_uri = (ext.get("tokenMetadata") or {}).get("uri")
    offchain = None
    if meta_uri and "/ipfs/" in meta_uri:
        cid = meta_uri.split("/ipfs/")[1]
        for g in IPFS_GATEWAYS:
            offchain = get(g + cid)
            if "_error" not in offchain:
                break
    ds_orders = get(f"https://api.dexscreener.com/orders/v1/solana/{mint}")
    ds = get(f"https://api.dexscreener.com/latest/dex/tokens/{mint}")
    ds_info = (ds.get("pairs") or [{}])[0].get("info") if isinstance(ds, dict) else None
    jup = get(f"https://lite-api.jup.ag/tokens/v2/search?query={mint}")
    jup = jup[0] if isinstance(jup, list) and jup else jup
    gt = get(f"https://api.geckoterminal.com/api/v2/networks/solana/tokens/{mint}")
    gt_attr = (gt.get("data") or {}).get("attributes", {}) if isinstance(gt, dict) else {}

    # Détail du coût de la transaction de création
    ctx = rpc.tx(F["creation"]["signature"])
    cost = sorted(((k, v / 1e9) for k, v in native_deltas(ctx).items() if k != C), key=lambda kv: -kv[1])

    # Actions signées par le créateur (hors réceptions passives)
    actions = []
    for tx in rpc.txs_for_address(C, limit_total=5000):
        keys = tx["transaction"]["message"]["accountKeys"]
        signers = [k["pubkey"] for k in keys if k.get("signer")]
        if C not in signers:
            continue
        names = [n for n in instruction_names(tx) if n not in NOISE]
        actions.append({"t": tx["blockTime"], "sig": tx["transaction"]["signatures"][0], "instructions": names,
                        "sol_delta": sol_deltas_by_owner(tx).get(C, 0) / 1e9,
                        "programs": sorted({ix.get("programId") for ix in tx["transaction"]["message"]["instructions"]})})
    passive = {"airdrops_other_tokens": 0, "fee_sharing_configs_by_third_parties": 0}
    for tx in rpc.txs_for_address(C, limit_total=5000):
        signers = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"] if k.get("signer")]
        if C in signers:
            continue
        n = instruction_names(tx)
        if "CreateFeeSharingConfig" in n:
            passive["fee_sharing_configs_by_third_parties"] += 1
        elif any(b.get("owner") == C and b["mint"] != mint for b in tx["meta"]["postTokenBalances"]):
            passive["airdrops_other_tokens"] += 1
    F["setup"] = {
        "mint_authority": info.get("mintAuthority"), "freeze_authority": info.get("freezeAuthority"),
        "token_program": F.get("token_program"), "decimals": info.get("decimals"),
        "metadata": ext.get("tokenMetadata"), "metadata_pointer": ext.get("metadataPointer"),
        "offchain_metadata": offchain,
        "dexscreener_orders": ds_orders, "dexscreener_info": ds_info,
        "jupiter": {k: v for k, v in (jup or {}).items() if not k.startswith("stats")} if isinstance(jup, dict) else jup,
        "geckoterminal": {k: gt_attr.get(k) for k in ("name", "symbol", "coingecko_coin_id", "launchpad_details")},
        "creation_cost_breakdown": cost, "creation_network_fee": ctx["meta"]["fee"] / 1e9,
        "creator_signed_actions": actions, "creator_passive": passive,
    }
    with open(path, "w") as f:
        json.dump(F, f, indent=1, default=str)
    print(json.dumps({k: v for k, v in F["setup"].items() if k not in ("creator_signed_actions",)}, indent=1)[:4000])
    print(len(actions), "actions signées")


if __name__ == "__main__":
    main()
