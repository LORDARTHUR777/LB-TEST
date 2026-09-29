#!/usr/bin/env python3
"""Piste des fonds du créateur : sorties de SOL, revenus DistributeCreatorFees,
et un saut de plus pour chaque destination (où partent les SOL ensuite).
Ajoute la clé "creator_trail" à facts.json.

  python3 creator_trail.py ../data/jeanphil
"""
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import instruction_names, sol_deltas_by_owner, sol_transfers  # noqa: E402
from rpc import Rpc  # noqa: E402

MIN = 50_000_000  # 0,05 SOL


def outflows(rpc, addr, start=None, limit=300):
    out = []
    for tx in rpc.txs_for_address(addr, start=start, limit_total=limit):
        for s, d, lam in sol_transfers(tx, MIN):
            if s == addr and d != addr:
                out.append({"to": d, "sol": lam / 1e9, "t": tx["blockTime"], "sig": tx["transaction"]["signatures"][0]})
    return out


def main():
    d = sys.argv[1]
    path = os.path.join(d, "facts.json")
    with open(path) as f:
        F = json.load(f)
    rpc = Rpc()
    C = F["creator_declared"]
    t0 = F["creation"]["block_time"]
    txs = rpc.txs_for_address(C, limit_total=5000)
    dist, dist_src = 0, defaultdict(int)
    creates = []
    for tx in txs:
        names = instruction_names(tx)
        if any(n.startswith("DistributeCreatorFees") for n in names):
            dist += sol_deltas_by_owner(tx).get(C, 0)
            for s, dd, lam in sol_transfers(tx, 1):
                if dd == C:
                    dist_src[s] += lam
        if any(n in ("Create", "CreateV2") for n in names):
            creates.append(tx["transaction"]["signatures"][0])
    outs = [o for o in outflows(rpc, C, start=t0, limit=5000)]
    hop = {}
    for dest in sorted({o["to"] for o in outs}):
        o2 = outflows(rpc, dest, limit=200)
        sinks = defaultdict(float)
        for x in o2:
            nxt = outflows(rpc, x["to"], limit=20)
            for y in nxt:
                sinks[y["to"]] += y["sol"]
        hop[dest] = {"balance_now": rpc.balance(dest)["value"] / 1e9, "outflows": o2,
                     "second_hop_sinks": dict(sorted(sinks.items(), key=lambda kv: -kv[1])[:5])}
    F["creator_trail"] = {
        "creator_balance_now_sol": rpc.balance(C)["value"] / 1e9,
        "creates_signed": creates,
        "distribute_creator_fees_income_sol": dist / 1e9,
        "distribute_sources": {k: v / 1e9 for k, v in sorted(dist_src.items(), key=lambda kv: -kv[1])},
        "sol_outflows": outs,
        "next_hops": hop,
    }
    with open(path, "w") as f:
        json.dump(F, f, indent=1, default=str)
    print(json.dumps({k: v for k, v in F["creator_trail"].items() if k != "next_hops"}, indent=1)[:3000])
    for k, v in hop.items():
        print(k, v["balance_now"], len(v["outflows"]), v["second_hop_sinks"])


if __name__ == "__main__":
    main()
