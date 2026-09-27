#!/usr/bin/env python3
"""Comparaison quantitative de deux tokens analysés par investigate.py.

  python3 compare.py ../data/jeanphil ../data/david
"""
import json
import os
import sys


def load(d):
    with open(os.path.join(d, "facts.json")) as fh:
        return json.load(fh)


def metrics(F):
    tl = {m["minutes"]: m for m in F["timeline"]}
    eb = F["early_buyers"]
    cr = F["wallets"].get(F["creator_declared"] or F["creation"]["fee_payer"], {})
    return {
        "Dev buy (SOL)": F["creation"].get("dev_buy_sol"),
        "Dev buy (% supply)": 100 * (F["creation"].get("dev_buy_tokens_ui") or 0) / F["supply_current_ui"],
        "Top 10 au snapshot (% supply)": F["snapshot"]["top10_pct_total"],
        "Acheteurs dans le slot de création": sum(1 for r in eb if r["same_slot_as_creation"]),
        "SOL des 20 premiers acheteurs": sum(r["sol_spent"] for r in eb[:20]),
        "% supply des 20 premiers acheteurs": sum(r["pct_supply"] for r in eb[:20]),
        "Tx d'achat multi-receveurs (bundles stricts)": len(F.get("multi_receiver_buy_txs") or {}),
        "Market cap +1 h (SOL)": (tl.get(60) or {}).get("mcap_sol"),
        "Market cap +24 h (SOL)": (tl.get(1440) or {}).get("mcap_sol"),
        "Holders +24 h": (tl.get(1440) or {}).get("holders"),
        "Volume +24 h (SOL)": (tl.get(1440) or {}).get("cum_volume_sol"),
        "Minutes jusqu'à la graduation": (F.get("graduation") or {}).get("minutes_after_creation"),
        "ATH market cap (SOL)": (F.get("ath_observed") or {}).get("mcap_sol"),
        "Volume total observé (SOL)": F.get("total_volume_sol_observed"),
        "Creator fees attribuables (SOL)": (F.get("creator_fees") or {}).get("accrued_total_sol"),
        "P&L réalisé créateur (SOL)": cr.get("realized_pnl_sol"),
        "P&L réalisé hypothèse top10 (SOL)": F["hypothesis_top10_is_creator"]["realized_pnl_sol"],
    }


def main():
    a, b = load(sys.argv[1]), load(sys.argv[2])
    ma, mb = metrics(a), metrics(b)
    print(f"| Indicateur | {a['mint'][:6]}… | {b['mint'][:6]}… | Ratio |")
    print("|---|---|---|---|")
    for k in ma:
        x, y = ma[k], mb[k]
        r = f"{x / y:,.1f}×" if isinstance(x, (int, float)) and isinstance(y, (int, float)) and y else "n/d"
        fx = lambda v: "n/d" if v is None else f"{v:,.2f}"  # noqa: E731
        print(f"| {k} | {fx(x)} | {fx(y)} | {r} |")


if __name__ == "__main__":
    main()
