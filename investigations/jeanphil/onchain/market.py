#!/usr/bin/env python3
"""Données de marché (ESTIMATIONS de tiers, GeckoTerminal / DexScreener) et
nombre de holders actuel (Helius DAS, on-chain).

  python3 market.py MINT T0_UNIX OUT_DIR

Écrit OUT_DIR/market.json : pools, volume cumulé USD par pool, ATH (plus haut
horaire du pool principal, puis affiné à la minute si disponible), prix aux
repères de temps, cours SOL/USD horaire, holders actuels.
"""
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rpc import Rpc  # noqa: E402

GT = "https://api.geckoterminal.com/api/v2/networks/solana"
SOL_USDC_POOL = "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"  # Raydium SOL/USDC
OFFSETS_MIN = [0, 5, 15, 30, 38, 60, 120, 240, 480, 720, 1440, 2880, 4320, 7200, 10080]


def get(url):
    for i in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception:  # noqa: BLE001
            time.sleep(3 * (i + 1))
    raise RuntimeError(url)


def ohlcv(pool, tf="hour", agg=1, start=None, pages=20):
    out, before = {}, None
    for _ in range(pages):
        u = f"{GT}/pools/{pool}/ohlcv/{tf}?aggregate={agg}&limit=1000&currency=usd&token=base"
        if before:
            u += f"&before_timestamp={before}"
        rows = get(u)["data"]["attributes"]["ohlcv_list"]
        time.sleep(2.1)
        if not rows:
            break
        for c in rows:
            out[c[0]] = c
        before = min(c[0] for c in rows)
        if start and before <= start:
            break
    return [out[k] for k in sorted(out)]


def sol_usd(start):
    rows = ohlcv(SOL_USDC_POOL, "hour", 1, start=start)
    return [(c[0], c[4]) for c in rows]


def holders_now(rpc, mint):
    """Nombre de comptes de tokens avec solde > 0 (Helius DAS getTokenAccounts)."""
    owners, cursor = set(), None
    while True:
        p = {"mint": mint, "limit": 1000}
        if cursor:
            p["cursor"] = cursor
        res = rpc.call("getTokenAccounts", p)
        for a in res.get("token_accounts", []):
            if int(a.get("amount", 0)) > 0:
                owners.add(a["owner"])
        cursor = res.get("cursor")
        if not cursor or not res.get("token_accounts"):
            return len(owners)


def main():
    mint, t0, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    ds = get(f"https://api.dexscreener.com/latest/dex/tokens/{mint}")
    pairs = [p for p in ds.get("pairs") or [] if (p.get("liquidity") or {}).get("usd") or p["volume"].get("h24")]
    pairs.sort(key=lambda p: -((p.get("liquidity") or {}).get("usd") or 0))
    main_pool = pairs[0]["pairAddress"] if pairs else None
    pools = {}
    for p in pairs[:6]:
        rows = ohlcv(p["pairAddress"], "hour", 1, start=t0)
        pools[p["pairAddress"]] = {
            "dex": p["dexId"], "created": (p.get("pairCreatedAt") or 0) // 1000,
            "liquidity_usd_now": (p.get("liquidity") or {}).get("usd"), "fdv_now": p.get("fdv"),
            "volume_usd_total": sum(c[5] for c in rows), "hourly": rows,
        }
    res = {"source": "GeckoTerminal OHLCV (USD, token=base) + DexScreener pairs", "main_pool": main_pool, "pools": pools}
    if main_pool:
        h = pools[main_pool]["hourly"]
        top = max(h, key=lambda c: c[2])
        minute = ohlcv(main_pool, "minute", 1, start=top[0] - 60, pages=40)
        mh = [c for c in minute if top[0] <= c[0] < top[0] + 3600]
        m = max(mh, key=lambda c: c[2]) if mh else None
        res["ath_main_pool"] = {"hour": top[0], "high_usd": top[2],
                                "minute": m[0] if m else None, "minute_high_usd": m[2] if m else None}
        res["price_marks_main_pool"] = []
        for off in OFFSETS_MIN:
            t = t0 + off * 60
            prev = [c for c in h if c[0] <= t]
            vol = sum(c[5] for p in pools.values() for c in p["hourly"] if c[0] < t)
            res["price_marks_main_pool"].append({"minutes": off, "time": t,
                                                 "close_usd": prev[-1][4] if prev else None,
                                                 "cum_volume_usd_all_pools_hourly": vol})
        res["ath_all_pools_hourly"] = sorted(
            ({"pool": k, "high_usd": max(c[2] for c in v["hourly"]),
              "hour": max(v["hourly"], key=lambda c: c[2])[0]} for k, v in pools.items() if v["hourly"]),
            key=lambda x: -x["high_usd"])
    res["sol_usd_hourly"] = sol_usd(t0 - 3600)
    try:
        res["holders_now"] = holders_now(Rpc(), mint)
    except Exception as ex:  # noqa: BLE001
        res["holders_now_error"] = str(ex)
    with open(os.path.join(out, "market.json"), "w") as f:
        json.dump(res, f)
    print(json.dumps({k: v for k, v in res.items() if k not in ("pools", "sol_usd_hourly")}, indent=1))
    print({k: (v["dex"], round(v["volume_usd_total"])) for k, v in pools.items()})


if __name__ == "__main__":
    main()
