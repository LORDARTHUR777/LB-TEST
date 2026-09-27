#!/usr/bin/env python3
"""Génère le rapport forensique Markdown à partir de facts.json.

  python3 report.py --data ../data/jeanphil --sol-usd-csv sol_usd.csv > ../RAPPORT_ONCHAIN.md

--sol-usd-csv : CSV "unix_time,price" (ex. klines horaires SOL/USDT).
Sans prix SOL/USD, tout reste en SOL (aucune conversion inventée).
"""
import argparse
import bisect
import csv
import datetime as dt
import json
import os


def ts(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if t else "n/d"


def f(x, n=2):
    if x is None:
        return "n/d"
    if abs(x) >= 1e6:
        return f"{x/1e6:,.2f} M"
    return f"{x:,.{n}f}"


class Usd:
    def __init__(self, path):
        self.t, self.p = [], []
        if path:
            with open(path) as fh:
                for row in csv.reader(fh):
                    try:
                        self.t.append(int(float(row[0])))
                        self.p.append(float(row[1]))
                    except (ValueError, IndexError):
                        continue

    def at(self, t):
        if not self.t or t is None:
            return None
        i = max(0, bisect.bisect_right(self.t, t) - 1)
        return self.p[i]

    def fmt(self, sol, t):
        p = self.at(t)
        return f"{f(sol)} SOL" + (f" (≈ {f(sol * p, 0)} $, ESTIMATION au prix SOL de {ts(t)[:16]})" if p and sol is not None else "")


def sig(s):
    return f"[`{s[:10]}…`](https://solscan.io/tx/{s})" if s else "n/d"


def addr(a):
    return f"[`{a[:6]}…{a[-4:]}`](https://solscan.io/account/{a})" if a else "n/d"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--sol-usd-csv")
    a = ap.parse_args()
    with open(os.path.join(a.data, "facts.json")) as fh:
        F = json.load(fh)
    U = Usd(a.sol_usd_csv)
    c = F["creation"]
    t0 = c["block_time"]
    now = max((e.get("last_time") or 0) for e in F["wallets"].values()) or t0
    L = []
    p = L.append
    p(f"# Rapport on-chain — mint `{F['mint']}`\n")
    p("Légende : **FAIT** = lu directement on-chain · **INDICE** = élément compatible avec un lien, non probant seul · "
      "**HYPOTHÈSE** = supposition explicite · **ESTIMATION** = calcul dépendant d'un paramètre externe.\n")
    if F["warnings"]:
        p("## Avertissements de collecte\n")
        for w in F["warnings"]:
            p(f"- {w}")
        p("")

    p("## 1. Création (FAIT)\n")
    p(f"- Transaction : {sig(c['signature'])} — slot {c['slot']} — {ts(t0)}")
    p(f"- Signataires : {', '.join(addr(s) for s in c['signers'])} — instructions : {', '.join(c['instructions'])}")
    p(f"- SOL du créateur juste avant : {f((c.get('creator_sol_before_creation_lamports') or 0)/1e9, 4)} SOL")
    p(f"- Variation SOL totale du créateur dans la tx de création : {f(c.get('launch_total_sol_delta'), 4)} SOL "
      f"(dont dev buy : {f(c.get('dev_buy_sol'), 4)} SOL pour {f(c.get('dev_buy_tokens_ui'))} tokens)")
    fa = c.get("creator_first_activity") or {}
    p(f"- Première transaction connue du wallet créateur : {sig(fa.get('signature'))} ({ts(fa.get('block_time'))})")
    for x in c.get("creator_first_funding") or []:
        p(f"  - financement : {addr(x['from'])} → {f(x['lamports']/1e9, 4)} SOL le {ts(x['t'])} ({sig(x['sig'])})")
    p("")

    p("## 2. Timeline des premières 24 h (FAIT, prix côté pool)\n")
    p("| Temps | Heure | Market cap (SOL) | Market cap ($, ESTIMATION) | Volume cumulé (SOL) | Holders |")
    p("|---|---|---|---|---|---|")
    for m in F["timeline"]:
        usd = U.at(m["time"])
        p(f"| +{m['minutes']} min | {ts(m['time'])} | {f(m['mcap_sol'])} | "
          f"{f(m['mcap_sol'] * usd, 0) if usd and m['mcap_sol'] else 'n/d'} | {f(m['cum_volume_sol'])} | {m['holders']} |")
    ath = F.get("ath_observed") or {}
    p(f"\n**ATH observé** : {f(ath.get('mcap_sol'))} SOL de market cap le {ts(ath.get('block_time'))} "
      f"({sig(ath.get('signature'))}) ; volume cumulé à ce moment {f(ath.get('cum_volume_sol'))} SOL ; holders {ath.get('holders')}.")
    if ath.get("block_time") and U.at(ath["block_time"]):
        p(f"≈ {f(ath['mcap_sol'] * U.at(ath['block_time']), 0)} $ (ESTIMATION). La market cap n'est PAS une valeur encaissable.")
    p("")

    g = F.get("graduation")
    p("## 3. Graduation Pump.fun → PumpSwap (FAIT)\n")
    if g:
        p(f"- Tx : {sig(g['signature'])} — {ts(g['block_time'])} — +{f(g['minutes_after_creation'])} min après création")
        p(f"- Pool : {addr(g['pool_owner'])} — liquidité initiale : {f(g['pool_tokens_in_ui'])} tokens + {f(g['pool_sol_in'])} SOL")
    else:
        p("- Non trouvée dans l'historique analysé.")
    p("")

    s = F["snapshot"]
    p(f"## 4. Snapshot à +{s['minutes_after_creation']} min (FAIT) — top 10 = {f(s['top10_pct_total'])} % de la supply\n")
    p("| Rang | Wallet | Tokens | % supply | Créateur ? |")
    p("|---|---|---|---|---|")
    for r in s["top20"][:10]:
        p(f"| {r['rank']} | {addr(r['owner'])} | {f(r['tokens_ui'])} | {f(r['pct_supply'])} % | {'oui' if r['is_creator'] else ''} |")
    p("\nComparer aux valeurs de la première investigation (4,1 / 4,1 / 3,7 / 3,6 / 3,2 / 2,3 / 2,1 / 2,1 / 1,8 / 1,8 %) : "
      "un écart peut venir d'un horodatage différent du snapshot ou de l'exclusion/inclusion de la bonding curve.\n")

    p("## 5. Premiers acheteurs (FAIT)\n")
    p("| # | Wallet | +s | Slot +n | SOL | Tokens | % supply | MC avant (SOL) | Jito | Payé par |")
    p("|---|---|---|---|---|---|---|---|---|---|")
    for r in F["early_buyers"][:100]:
        p(f"| {r['rank']} | {addr(r['owner'])}{' (créateur)' if r['is_creator'] else ''} | {r['seconds_after_creation']} | "
          f"{r['slots_after_creation']} | {f(r['sol_spent'], 3)} | {f(r['tokens_ui'])} | {f(r['pct_supply'])} | "
          f"{f(r['mcap_sol_before'])} | {'oui' if r['jito_tip'] else ''} | {', '.join(addr(x) for x in r['paid_by'] or [])} |")
    same = F.get("same_slot_groups") or {}
    p(f"\n**Achats dans un même slot (INDICE de bundle)** : {len(same)} slots avec ≥ 2 acheteurs.")
    for sl, ws in list(same.items())[:20]:
        p(f"- slot {sl} : {', '.join(addr(w) for w in ws)}")
    mr = F.get("multi_receiver_buy_txs") or {}
    p(f"\n**Transactions d'achat créditant plusieurs wallets (FAIT : bundle au sens strict)** : {len(mr)}")
    for sg, ws in list(mr.items())[:20]:
        p(f"- {sig(sg)} → {', '.join(addr(w) for w in ws)}")
    p("")

    p("## 6. Wallets clés — P&L (FAIT pour les flux, ESTIMATION pour la valeur latente)\n")
    p("| Wallet | Relation | SOL investi | % supply max | Tokens vendus | SOL récupéré | P&L réalisé (SOL) | "
      "Position restante | Valeur spot (SOL) | Valeur liquidation (SOL) |")
    p("|---|---|---|---|---|---|---|---|---|---|")
    ws = sorted(F["wallets"].values(), key=lambda d: -(d["max_pct_supply"] or 0))
    for d in ws:
        p(f"| {addr(d['wallet'])} | {d['relation']} | {f(d['sol_invested'], 3)} | {f(d['max_pct_supply'])} % | "
          f"{f(d['tokens_sold'])} | {f(d['sol_recovered'], 3)} | {f(d['realized_pnl_sol'], 3)} | {f(d['balance_now_ui'])} | "
          f"{f(d.get('unrealized_spot_sol'), 3)} | {f(d.get('unrealized_liquidation_sol'), 3)} |")
    p("\nDétail par wallet (transferts, sources, destinations) : voir `facts.json` → `wallets`.\n")

    cr = F["wallets"].get(F["creator_declared"] or c["fee_payer"], {})
    p("## 7. Wallet créateur (FAIT)\n")
    p(f"- Achats : {cr.get('n_buys')} · ventes : {cr.get('n_sells')} · transferts entrants : {cr.get('n_transfers_in')} "
      f"· sortants : {cr.get('n_transfers_out')}")
    p(f"- Tokens reçus par transfert : {f(cr.get('tokens_transferred_in'))} depuis {', '.join(addr(x) for x in cr.get('transfer_in_sources') or []) or '—'}")
    p(f"- SOL investi {f(cr.get('sol_invested'), 3)} · récupéré {f(cr.get('sol_recovered'), 3)} · position actuelle {f(cr.get('balance_now_ui'))}")
    p("- Chronologie des mouvements du token :")
    for e in cr.get("events", []):
        p(f"  - {ts(e['block_time'])} {e['kind']} {f(e['token_raw'] / 10 ** F['decimals'])} tokens, "
          f"{f(e['sol_lamports'] / 1e9, 4)} SOL — {sig(e['signature'])}")
    p("")

    cf = F.get("creator_fees", {})
    p("## 8. Creator fees (FAIT)\n")
    p(f"- Vaults : {', '.join(addr(v) for v in cf.get('vaults', []))}")
    p(f"- Fees accumulées attribuables à ce token : **{f(cf.get('accrued_total_sol'), 3)} SOL** "
      f"(somme des crédits au vault dans les trades de ce mint)")
    p(f"- Claims signés par le créateur : {len(cf.get('claims', []))} — total reçu {f(cf.get('claimed_total_sol'), 3)} SOL "
      "(peut inclure d'autres tokens du même créateur)")
    for cl in cf.get("claims", []):
        p(f"  - {ts(cl['block_time'])} : {f(cl['sol_received'], 4)} SOL — {sig(cl['signature'])}")
    p("")

    p("## 9. Liens entre wallets\n")
    p(f"Hubs exclus (≥ 40 wallets financés, probablement CEX/services) : {', '.join(addr(h) for h in F.get('hubs_excluded', [])) or '—'}\n")
    p("| A | B | Type | Via | Force |")
    p("|---|---|---|---|---|")
    for e in F.get("link_edges", [])[:200]:
        p(f"| {addr(e['a'])} | {addr(e['b'])} | {e['type']} | {e['via'] if e['via'] is None or isinstance(e['via'], int) else addr(e['via']) if len(str(e['via'])) < 50 else sig(e['via'])} | {e['strength']} |")
    p(f"\nCluster du créateur (liens FAIT/INDICE fort uniquement) : {', '.join(addr(w) for w in F.get('creator_cluster', []))}\n")

    h = F["hypothesis_top10_is_creator"]
    p("## 10. HYPOTHÈSE — les 10 plus gros wallets du snapshot appartiennent au créateur\n")
    p("> **Ceci est une simulation. Elle ne prouve rien : elle calcule ce que serait le résultat SI l'hypothèse était vraie.**\n")
    p(f"- Wallets : {len(h['members'])} — {f(h['pct_supply_snapshot'])} % de la supply au snapshot")
    p(f"- SOL injectés : {U.fmt(h['sol_injected'], t0)}")
    p(f"- SOL récupérés en ventes : {U.fmt(h['sol_recovered'], now)} — tokens vendus {f(h['tokens_sold'])} "
      f"— prix moyen {f(h['avg_sell_price_sol'], 12)} SOL/token")
    p(f"- Tokens restants : {f(h['tokens_remaining'])} — valeur spot {f(h['remaining_spot_value_sol'], 3)} SOL, "
      f"valeur de liquidation avec slippage {f(h['remaining_liquidation_value_sol'], 3)} SOL (ESTIMATION)")
    p(f"- P&L réalisé du cluster : {f(h['realized_pnl_sol'], 3)} SOL")
    T = h["total"]
    p(f"\n**Total hypothétique (créateur + 10 wallets)** : mis de sa poche {f(T['sol_out_of_pocket'], 3)} SOL · "
      f"encaissé en ventes {f(T['sol_cash_recovered_from_sales'], 3)} SOL · creator fees {f(T['creator_fees_sol'], 3)} SOL · "
      f"réalisé fees incluses {f(T['realized_incl_fees_sol'], 3)} SOL · tokens restants {f(T['tokens_remaining_incl_creator'])}.\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
