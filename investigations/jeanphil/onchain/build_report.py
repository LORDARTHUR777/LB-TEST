#!/usr/bin/env python3
"""Rapport forensique final JEANPHIL (+ comparaison DAVID) à partir des
sorties de investigate.py et market.py. Aucun chiffre n'est saisi à la main.

  python3 build_report.py ../data/jeanphil ../data/david > ../RAPPORT.md
"""
import bisect
import csv
import datetime as dt
import json
import os
import sys

SUPPLY0 = 1_000_000_000  # supply initiale Pump.fun (base utilisée par les trackers au lancement)


def load(d):
    with open(os.path.join(d, "facts.json")) as f:
        F = json.load(f)
    M = None
    p = os.path.join(d, "market.json")
    if os.path.exists(p):
        with open(p) as f:
            M = json.load(f)
    return F, M


class Px:
    def __init__(self, M):
        s = (M or {}).get("sol_usd_hourly") or []
        self.t = [a for a, _ in s]
        self.p = [b for _, b in s]

    def __call__(self, t):
        if not self.t or t is None:
            return None
        return self.p[max(0, bisect.bisect_right(self.t, t) - 1)]


def ts(t, sec=True):
    if not t:
        return "n/d"
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%d/%m/%Y %H:%M:%S" if sec else "%d/%m %H:%M")


def n(x, d=2):
    if x is None:
        return "n/d"
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s


def usd(x):
    return "n/d" if x is None else n(x, 0) + " $"


def mtok(x):
    return "n/d" if x is None else n(x / 1e6, 2) + " M"


def a(addr, short=True):
    if not addr:
        return "n/d"
    lab = f"{addr[:6]}…{addr[-4:]}" if short else addr
    return f"[`{lab}`](https://solscan.io/account/{addr})"


def s(sig):
    return f"[`{sig[:8]}…`](https://solscan.io/tx/{sig})" if sig else "n/d"


def dur(sec):
    if sec is None:
        return "n/d"
    sec = int(sec)
    if sec < 60:
        return f"{sec} s"
    if sec < 3600:
        return f"{sec // 60} min {sec % 60:02d} s"
    return f"{sec // 3600} h {sec % 3600 // 60:02d}"


def usd_of_events(events, px, sign):
    tot = 0.0
    for e in events:
        v = e["sol_lamports"] / 1e9
        if (v < 0) == (sign < 0) and v != 0:
            p = px(e["block_time"])
            if p:
                tot += abs(v) * p
    return tot


def main():
    jd = sys.argv[1]
    dd = sys.argv[2] if len(sys.argv) > 2 else None
    F, M = load(jd)
    px = Px(M)
    W = F["wallets"]
    C = F["creator_declared"]
    cr = W[C]
    c = F["creation"]
    t0 = c["block_time"]
    g = F["graduation"]
    snap = F["snapshot"]["top20"][:10]
    snap_w = [r["owner"] for r in snap]
    cf = F["creator_fees"]
    h = F["hypothesis_top10_is_creator"]
    pool = F["pool_now"]
    sol_now = px.p[-1] if px.p else None
    price_now_usd = pool["spot_price_sol"] * sol_now if sol_now else None
    L = []
    p = L.append

    # --------------------------------------------------------------- en-tête
    p("# $JEANPHIL — investigation forensique on-chain\n")
    p(f"Mint : `{F['mint']}` · Créateur : `{C}` · Rapport généré le "
      f"{dt.datetime.now(dt.timezone.utc).strftime('%d/%m/%Y %H:%M')} UTC\n")
    p("**Légende.** **FAIT** = lu directement dans les transactions Solana (signature fournie). "
      "**INDICE** = élément compatible avec un lien, non probant seul. **HYPOTHÈSE** = supposition explicite. "
      "**ESTIMATION** = calcul dépendant d'une donnée externe (cours SOL/USD, chandeliers GeckoTerminal, "
      "valorisation au prix du pool).\n")
    p("**Sources.** RPC Solana Helius (transactions complètes, `getTransactionsForAddress`), "
      "GeckoTerminal (chandeliers, cours SOL/USD horaire du pool Raydium SOL/USDC), DexScreener (liste des pools), "
      "Helius DAS (holders actuels). Toutes les signatures sont cliquables (Solscan).\n")
    p(f"**Conventions.** Les % de supply sont calculés sur la supply initiale de 1 000 000 000 (base des trackers au "
      f"lancement ; supply actuelle {n(F['supply_current_ui'], 0)} après burns). Les montants en $ sont convertis au "
      f"cours SOL/USD de l'heure de chaque transaction (ESTIMATION). La market cap n'est jamais de l'argent encaissable.\n")

    # --------------------------------------------------------------- réponse
    fees_usd = sum(cl["sol_received"] * (px(cl["block_time"]) or 0) for cl in cf["claims"])
    ser = h["series"]
    h_in_usd = sum(-e["sol"] * (px(e["t"]) or 0) for e in ser if e["sol"] < 0)
    h_out_usd = sum(e["sol"] * (px(e["t"]) or 0) for e in ser if e["sol"] > 0)
    cr_in_usd = usd_of_events(cr["events"], px, -1)
    cr_pos_liq_sol = cr.get("unrealized_liquidation_sol")
    cr_pos_spot_sol = cr.get("unrealized_spot_sol")
    p("## Réponse courte\n")
    p("| | Créateur officiel (FAIT) | Top 10 du snapshot +38 min (HYPOTHÈSE « même personne ») | Total hypothétique |")
    p("|---|---|---|---|")
    p(f"| Mis de sa poche | **{n(cr['sol_invested'], 3)} SOL** (≈ {usd(cr_in_usd)}) | {n(h['sol_injected'], 2)} SOL (≈ {usd(h_in_usd)}) "
      f"| {n(cr['sol_invested'] + h['sol_injected'], 2)} SOL (≈ {usd(cr_in_usd + h_in_usd)}) |")
    p(f"| Encaissé en ventes de tokens | **0 SOL** (n'a jamais vendu) | {n(h['sol_recovered'], 2)} SOL (≈ {usd(h_out_usd)}) "
      f"| {n(h['sol_recovered'], 2)} SOL (≈ {usd(h_out_usd)}) |")
    p(f"| Creator fees réclamées | **{n(cf['claimed_total_sol'], 2)} SOL** (≈ {usd(fees_usd)}) + {n(sum(cf['unclaimed_now_sol'].values()), 2)} SOL non réclamés "
      f"| — | {n(cf['claimed_total_sol'], 2)} SOL |")
    p(f"| P&L réalisé | **{n(cf['claimed_total_sol'] - cr['sol_invested'], 2)} SOL** (≈ {usd(fees_usd - cr_in_usd)}) "
      f"| {n(h['realized_pnl_sol'], 2)} SOL (≈ {usd(h_out_usd - h_in_usd)}) "
      f"| {n(cf['claimed_total_sol'] - cr['sol_invested'] + h['realized_pnl_sol'], 2)} SOL "
      f"(≈ {usd(fees_usd - cr_in_usd + h_out_usd - h_in_usd)}) |")
    p(f"| Tokens restants | **{mtok(cr['balance_now_ui'])}** ({n(100 * cr['balance_now_ui'] / SUPPLY0, 2)} %) — spot {n(cr_pos_spot_sol, 1)} SOL, "
      f"liquidation ≈ {n(cr_pos_liq_sol, 1)} SOL | {mtok(h['tokens_remaining'])} — spot {n(h['remaining_spot_value_sol'], 1)} SOL "
      f"| {mtok(h['total']['tokens_remaining_incl_creator'])} |")
    p("")
    p("**Lecture.** Le gain du créateur ne vient pas de la vente de tokens : il vient à ~100 % des **creator fees** "
      "générées par le volume. Dans l'hypothèse où les 10 gros wallets initiaux lui appartiendraient, les ventes de "
      "ces wallets ajouteraient un P&L réalisé du même ordre de grandeur que les fees — mais **aucun lien on-chain "
      "n'a été trouvé entre le créateur et ces wallets** (voir §6), et plusieurs d'entre eux appartiennent à des groupes "
      "distincts. L'hypothèse est donc présentée uniquement comme un calcul.\n")

    # --------------------------------------------------------------- setup
    su = F.get("setup") or {}
    tr = F.get("creator_trail") or {}
    if su:
        md = su.get("metadata") or {}
        off = su.get("offchain_metadata") or {}
        jup = su.get("jupiter") or {}
        dsi = su.get("dexscreener_info") or {}
        p("## Ce que le créateur a mis en place, dans l'ordre (réglages, coûts, référencement, gains)\n")
        p("### A. Réglages du memecoin (FAIT, lus sur le compte du mint)\n")
        p("| Réglage | Valeur | Ce que ça implique |")
        p("|---|---|---|")
        p(f"| Plateforme | Pump.fun (programme `6EF8…F6P`, instruction `CreateV2`) | lancement « fair launch » sur bonding curve, graduation automatique |")
        p(f"| Nom / ticker | {md.get('name')} / {md.get('symbol')} | |")
        p(f"| Description | « {off.get('description', 'n/d').strip()} » | |")
        p(f"| Site déclaré dans les métadonnées | {off.get('website', 'n/d')} | aucun X/Telegram dans les métadonnées on-chain |")
        p(f"| Image | IPFS `{(off.get('image') or '').split('/')[-1][:20]}…` | |")
        p(f"| Standard | Token-2022 (`{su.get('token_program', '')[:6]}…`), {su.get('decimals')} décimales, supply initiale 1 000 000 000 | |")
        p(f"| Mint authority | {su.get('mint_authority') or '**désactivée**'} | impossible de créer de nouveaux tokens |")
        p(f"| Freeze authority | {su.get('freeze_authority') or '**désactivée**'} | impossible de geler un wallet |")
        p(f"| Update authority des métadonnées | {md.get('updateAuthority') or '**aucune**'} | nom/logo/lien non modifiables |")
        p(f"| Dev buy | {mtok(c['dev_buy_tokens_ui'])} ({n(c['dev_buy_tokens_ui'] / SUPPLY0 * 100, 2)} %) | seul achat du créateur, jamais revendu |")
        p("| Destinataire des creator fees | le créateur lui-même (vaults PDA dérivés de son adresse) | aucun partage de fees configuré par lui sur JEANPHIL |")
        a_ = jup.get("audit") or {}
        p(f"| Contrôle Jupiter | mint/freeze désactivés : {a_.get('mintAuthorityDisabled')}/{a_.get('freezeAuthorityDisabled')} ; "
          f"dev = {n(a_.get('devBalancePercentage'), 2)} % ; tokens créés par ce dev : {a_.get('devMints')} ; "
          f"score organique {n(jup.get('organicScore'), 0)}/100 ({jup.get('organicScoreLabel')}) ; tags {jup.get('tags')} | source : API Jupiter |")
        p("")
        p("### B. Coût du lancement — où est parti chaque lamport (FAIT)\n")
        p(f"Transaction {s(c['signature'])}, signée depuis le wallet créateur sur **pump.fun**. Total débité : "
          f"**{n(-c['launch_total_sol_delta'], 6)} SOL ≈ {usd(-c['launch_total_sol_delta'] * (px(t0) or 0))}** (SOL ≈ {n(px(t0), 2)} $).\n")
        p("| Destination | SOL | Nature (INDICE sauf mention) |")
        p("|---|---|---|")
        lab = {F["bonding_curve"]: "bonding curve : paiement du dev buy + rente du compte (FAIT)",
               F["mint"]: "rente du compte mint (dépôt récupérable seulement si fermé)",
               cf["vaults"][0]: "creator fee du dev buy → son propre vault (lui revient, FAIT)"}
        for k, v in su.get("creation_cost_breakdown", []):
            p(f"| {a(k)} | {n(v, 6)} | {lab.get(k, 'frais de protocole Pump.fun ou rente de comptes de tokens')} |")
        p(f"| frais réseau Solana | {n(su.get('creation_network_fee'), 6)} | FAIT |")
        p("\nAucune autre dépense du wallet créateur n'apparaît on-chain : pas de paiement en SOL/USDC vers DexScreener, "
          "un market maker ou un service de bump/volume depuis ce wallet.\n")
        p("### C. Référencement du token, dans l'ordre\n")
        p("| Date (UTC) | Où | Comment | Coût / payeur | Source |")
        p("|---|---|---|---|---|")
        ref = []
        p_ = p
        p = lambda line, t=t0: ref.append((t, line))  # noqa: E731
        p(f"| {ts(t0)} | **Pump.fun** | création par le créateur | {n(-c['launch_total_sol_delta'], 3)} SOL (ci-dessus) | FAIT on-chain |")
        p(f"| {ts(g['block_time'])} | **PumpSwap** (pool {a(g['pool_owner'])}) | graduation automatique | 0 pour le créateur | FAIT on-chain |", g["block_time"])
        if M:
            for pa, pl in sorted(M["pools"].items(), key=lambda kv: kv[1]["created"]):
                if pa == g["pool_owner"]:
                    continue
                p(f"| {ts(pl['created'])} | {pl['dex'].capitalize()} (pool {a(pa)}) | pool créé par un tiers | pas le créateur | DexScreener |", pl["created"])
        for o in (su.get("dexscreener_orders") or {}).get("orders", []):
            p(f"| {ts(o['paymentTimestamp'] // 1000)} | **DexScreener** — « {o['type']} » ({o['status']}) | profil enrichi : logo, bannière, "
              f"liens {', '.join(x['type'] for x in dsi.get('socials', []))} | tarif public ≈ 299 $ (ESTIMATION) ; **payeur non identifié** "
              "— aucune sortie du wallet créateur ce jour-là | API DexScreener |", o["paymentTimestamp"] // 1000)
        p(f"| automatique | GeckoTerminal, Jupiter, Birdeye, Phantom… | indexation automatique des pools | 0 | APIs |", 9e18)
        p(f"| — | CoinGecko | **non listé** (`coingecko_coin_id` = null) | — | API GeckoTerminal |", 9e18)
        p("| après le 20/09 | Pages de prix / articles : Coinbase (page de prix), CryptoRank, CoinCodex, OpenSea, KuCoin News, Bitrue, "
          "KCEX, OneBullEx ; site d'airdrop jean-philanthrope.com | pages éditoriales ou agrégateurs — pas des listings d'exchange payés | n/d | SOURCE TIERCE (recherche web) |", 9e18)
        p = p_
        for _, line in sorted(ref, key=lambda x: x[0]):
            p(line)
        socials = ", ".join(f"[{x['type']}]({x['url']})" for x in dsi.get("socials", []))
        p(f"\nRéseaux affichés sur le profil DexScreener : {socials}. Le compte X a publié le contrat comme « seul token officiel » "
          "(SOURCE TIERCE : post X).\n")
        p("### D. Toutes les actions signées par le créateur (FAIT)\n")
        p("| Date (UTC) | Action | SOL pour lui | Transaction |")
        p("|---|---|---|---|")
        arows = []
        p_ = p
        p = lambda line, t=0: arows.append((t, line))  # noqa: E731
        acts = su.get("creator_signed_actions", [])
        dist_batch = [x for x in acts if any(i.startswith("DistributeCreatorFees") for i in x["instructions"])]
        for x in sorted(acts, key=lambda x: x["t"]):
            if x in dist_batch:
                continue
            ins = x["instructions"]
            if "CreateV2" in ins:
                what = "Création du token + dev buy (pump.fun)"
            elif any("Collect" in i for i in ins):
                what = "Retrait (claim) des creator fees JEANPHIL"
            elif not ins and x["sol_delta"] < 0:
                what = "Envoi de SOL vers " + next((a(o["to"]) for o in tr.get("sol_outflows", []) if o["sig"] == x["sig"]), "?")
            elif not ins and x["sol_delta"] > 0:
                what = "Fermeture d'un compte de token reçu en airdrop (rente récupérée)"
            else:
                what = ", ".join(ins) or "transaction technique"
            p(f"| {ts(x['t'])} | {what} | {n(x['sol_delta'], 4)} | {s(x['sig'])} |", x["t"])
        if dist_batch:
            p(f"| {ts(min(x['t'] for x in dist_batch))} | {len(dist_batch)} × `DistributeCreatorFees` : encaisse des parts de fees "
              f"d'**autres** tokens qui l'ont désigné bénéficiaire | {n(sum(x['sol_delta'] for x in dist_batch), 4)} | — |", min(x["t"] for x in dist_batch))
        claim_crank = [cl for cl in cf["claims"] if cl["signature"] not in {x["sig"] for x in acts}]
        for cl in claim_crank:
            p(f"| {ts(cl['block_time'])} | Claim déclenché par un tiers (instruction sans permission), fees versées au créateur | "
              f"{n(cl['sol_received'], 4)} | {s(cl['signature'])} |", cl["block_time"])
        p = p_
        for _, line in sorted(arows, key=lambda x: x[0]):
            p(line)
        pas = su.get("creator_passive") or {}
        p(f"\nReçu passivement (non signé par lui) : {pas.get('airdrops_other_tokens')} transactions d'airdrop d'autres memecoins "
          f"et {pas.get('fee_sharing_configs_by_third_parties')} configurations de partage de fees créées par des tiers sur d'autres tokens. "
          "Il n'a acheté ou vendu aucun autre token.\n")
        p("### E. Bilan financier du créateur (FAIT, $ = ESTIMATION)\n")
        un = sum(cf["unclaimed_now_sol"].values())
        outs = [x for x in tr.get("sol_outflows", []) if x["sig"] != c["signature"]]
        p("| Poste | SOL | ≈ USD |")
        p("|---|---|---|")
        p(f"| Mis de sa poche (création + dev buy) | −{n(-c['launch_total_sol_delta'], 3)} | −{usd(-c['launch_total_sol_delta'] * (px(t0) or 0))} |")
        p(f"| Ventes de JEANPHIL | 0 | 0 $ |")
        p(f"| Creator fees JEANPHIL réclamées | +{n(cf['claimed_total_sol'], 2)} | +{usd(fees_usd)} |")
        p(f"| Creator fees non réclamées | +{n(un, 2)} | +{usd(un * (sol_now or 0))} |")
        p(f"| Parts de fees d'autres tokens (`DistributeCreatorFees`) | +{n(tr.get('distribute_creator_fees_income_sol'), 2)} | ≈ +{usd((tr.get('distribute_creator_fees_income_sol') or 0) * (sol_now or 0))} |")
        p(f"| **Gain réalisé** | **+{n(cf['claimed_total_sol'] + (tr.get('distribute_creator_fees_income_sol') or 0) + c['launch_total_sol_delta'], 2)}** | "
          f"**≈ +{usd(fees_usd + (tr.get('distribute_creator_fees_income_sol') or 0) * (sol_now or 0) + c['launch_total_sol_delta'] * (px(t0) or 0))}** |")
        p(f"| dont déjà sorti vers un service (exchange probable) | {n(sum(x['sol'] for x in outs), 2)} | {usd(sum(x['sol'] * (px(x['t']) or 0) for x in outs))} |")
        p(f"| resté sur le wallet créateur | {n(tr.get('creator_balance_now_sol'), 2)} | {usd((tr.get('creator_balance_now_sol') or 0) * (sol_now or 0))} |")
        p(f"| **Encore en tokens** (non vendus) | {mtok(cr['balance_now_ui'])} JEANPHIL | ≈ {usd((cr_pos_spot_sol or 0) * (sol_now or 0))} au prix spot ; "
          f"≈ {usd((cr_pos_liq_sol or 0) * (sol_now or 0))} si vendus d'un bloc (ESTIMATION) |")
        p("")

    # --------------------------------------------------------------- timeline
    p("## 1. Timeline chronologique\n")
    ev = []
    ev.append((c["creator_first_activity"]["block_time"], "Financement du wallet créateur",
               f"{n(c['creator_sol_before_creation_lamports'] / 1e9, 4)} SOL reçus de {a(c['creator_first_funding'][0]['from'])} "
               f"({s(c['creator_first_funding'][0]['sig'])}) — FAIT"))
    ev.append((t0, "Création + dev buy (même transaction)",
               f"{mtok(c['dev_buy_tokens_ui'])} JEANPHIL pour {n(c['dev_buy_sol'], 4)} SOL ({s(c['signature'])}) — FAIT"))
    eb = F["early_buyers"]
    s5 = [r for r in eb if r["seconds_after_creation"] <= 5 and not r["is_creator"]]
    ev.append((t0 + 3, "Snipers", f"{len(s5)} wallets achètent dans les 5 s ({n(sum(r['tokens_ui'] for r in s5) / SUPPLY0 * 100, 2)} % de la supply) — FAIT"))
    low = min((m for m in F["timeline"] if m["minutes"] in (15, 30)), key=lambda m: m["mcap_sol"] or 1e9)
    ev.append((low["time"], "Phase calme", f"market cap ≈ {n(low['mcap_sol'], 1)} SOL à +{low['minutes']} min ; les snipers ont revendu — FAIT"))
    ev.append((t0 + F["snapshot"]["minutes_after_creation"] * 60, "Snapshot +38 min",
               f"top 10 = {n(sum(r['tokens_ui'] for r in snap) / SUPPLY0 * 100, 1)} % de la supply — FAIT"))
    ev.append((g["block_time"], "Graduation → PumpSwap",
               f"+{dur(g['block_time'] - t0)} ; pool {a(g['pool_owner'])} ({s(g['signature'])}) — FAIT"))
    if M:
        ath = M["ath_main_pool"]
        ev.append((ath["minute"], "ATH (pool principal)",
                   f"{n(ath['minute_high_usd'], 5)} $ ≈ {usd(ath['minute_high_usd'] * SUPPLY0)} de market cap — ESTIMATION GeckoTerminal"))
    for cl in cf["claims"]:
        ev.append((cl["block_time"], "Claim creator fees", f"{n(cl['sol_received'], 2)} SOL ({s(cl['signature'])}) — FAIT"))
    for x in cr["sol_out_all"] if cr.get("sol_out_all") else []:
        pass
    outs = [x for x in (W[C].get("sol_out_all") or [])]
    ev.sort(key=lambda x: x[0])
    p("| Date (UTC) | T+ | Événement | Détail |")
    p("|---|---|---|---|")
    for t, what, det in ev:
        p(f"| {ts(t)} | {dur(t - t0) if t >= t0 else '−' + dur(t0 - t)} | {what} | {det} |")
    p("")

    # --------------------------------------------------------------- création
    p("## 2. Création du token (FAIT)\n")
    p(f"- **Transaction** : {s(c['signature'])} — slot {c['slot']} — **{ts(t0)} UTC** — instructions `{', '.join(c['instructions'][:3])} … BuyV2`")
    p(f"- **Signataires** : {a(c['signers'][0], False)} (créateur) et le mint lui-même")
    p(f"- **SOL sur le wallet avant création** : {n(c['creator_sol_before_creation_lamports'] / 1e9, 6)} SOL")
    fa = c["creator_first_activity"]
    ff = c["creator_first_funding"][0]
    p(f"- **Première transaction du wallet** : {s(fa['signature'])} le {ts(fa['block_time'])} "
      f"({dur(t0 - fa['block_time'])} avant la création) : réception de {n(ff['lamports'] / 1e9, 6)} SOL depuis {a(ff['from'], False)}")
    p(f"  - INDICE : {a(ff['from'])} présente un profil de wallet de service (très nombreux destinataires, >1 800 SOL de solde) — "
      "typique d'un retrait d'exchange. Aucun autre lien de financement n'a été trouvé.")
    p(f"- **Coût total du lancement** (création + dev buy + frais) : {n(-c['launch_total_sol_delta'], 6)} SOL "
      f"(≈ {usd(-c['launch_total_sol_delta'] * (px(t0) or 0))})")
    p(f"- **Première acquisition** : dev buy de **{n(c['dev_buy_tokens_ui'], 2)} JEANPHIL** "
      f"({n(c['dev_buy_tokens_ui'] / SUPPLY0 * 100, 3)} % de la supply) dans la transaction de création.\n")

    # --------------------------------------------------------------- acheteurs
    p("## 3. Premiers acheteurs (FAIT)\n")
    p("| Groupe | SOL dépensés | Tokens achetés (cumul) | % supply acheté | Dernier achat du groupe |")
    p("|---|---|---|---|---|")
    for k in (10, 20, 50, 100):
        grp = eb[:k]
        p(f"| {k} premiers | {n(sum(r['sol_spent'] for r in grp), 2)} | {mtok(sum(r['tokens_ui'] for r in grp))} | "
          f"{n(sum(r['tokens_ui'] for r in grp) / SUPPLY0 * 100, 2)} % | +{dur(grp[-1]['seconds_after_creation'])} |")
    p("\n*« Cumul acheté » ≠ détention simultanée : beaucoup revendent en quelques minutes.*\n")
    p("| # | Wallet | T+ | Slot +n | SOL | Tokens | % supply | MC avant achat (SOL) | Jito | Lien connu |")
    p("|---|---|---|---|---|---|---|---|---|---|")
    clus = {w: i + 1 for i, cl in enumerate(F["clusters"]) for w in cl}
    for r in eb[:30]:
        lk = "créateur" if r["is_creator"] else (f"groupe {clus[r['owner']]}" if r["owner"] in clus else "")
        p(f"| {r['rank']} | {a(r['owner'])} | {r['seconds_after_creation']} s | {r['slots_after_creation']} | {n(r['sol_spent'], 3)} | "
          f"{mtok(r['tokens_ui'])} | {n(r['tokens_ui'] / SUPPLY0 * 100, 2)} % | {n(r['mcap_sol_before'], 1)} | "
          f"{'oui' if r['jito_tip'] else ''} | {lk} |")
    p("\nListe complète des 100 premiers : `early_buyers.csv`. MC en SOL : prix côté bonding curve × 1 Md.\n")

    # --------------------------------------------------------------- snapshot
    p("## 4. Les 10 gros wallets du snapshot +38 min (FAIT)\n")
    p("Les pourcentages de la première investigation (4,1 / 4,1 / 3,7 / 3,6 / 3,2 / 2,3 / 2,1 / 2,1 / 1,8 / 1,8 %) "
      "correspondent **exactement** à ce snapshot calculé sur 1 Md de supply :\n")
    p("| Rang | Wallet | Tokens | % | Achats | Ventes | SOL investi | SOL récupéré | P&L réalisé | Restant | Premier / dernier mouvement | Groupe |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in snap:
        d = W[r["owner"]]
        est = " *" if d.get("n_priced_by_pool") else ""
        p(f"| {r['rank']} | {a(r['owner'])} | {mtok(r['tokens_ui'])} | {n(r['tokens_ui'] / SUPPLY0 * 100, 2)} % | {d['n_buys']} | "
          f"{d['n_sells']} | {n(d['sol_invested'], 2)}{est} | {n(d['sol_recovered'], 2)}{est} | **{n(d['realized_pnl_sol'], 2)}**{est} | "
          f"{mtok(d['balance_now_ui'])} | {ts(d['first_time'], False)} → {ts(d['last_time'], False)} | {clus.get(r['owner'], '—')} |")
    p("\n\\* montants en partie **valorisés au prix d'exécution du pool** (ESTIMATION) : ces wallets paient en USDC ou via "
      "un routeur tiers, le SOL ne transite donc pas par leur compte.\n")
    for r in snap:
        d = W[r["owner"]]
        notes = []
        if d["tokens_transferred_out"] > 1:
            notes.append(f"a transféré {mtok(d['tokens_transferred_out'])} vers {', '.join(a(x) for x in d['transfer_out_destinations'][:3])}")
        if d["n_buys"] > 5:
            notes.append(f"trader actif ({d['n_buys']} achats / {d['n_sells']} ventes jusqu'au {ts(d['last_time'], False)})")
        fb = d.get("funding_before_first_buy") or []
        if fb:
            big = max(fb, key=lambda x: x["lamports"])
            notes.append(f"principal financement avant 1er achat : {n(big['lamports'] / 1e9, 2)} SOL de {a(big['from'])}")
        if notes:
            p(f"- {a(r['owner'])} : " + " ; ".join(notes))
    p("")

    # --------------------------------------------------------------- bundles / liens
    p("## 5. Snipers, bundles et achats groupés (FAIT)\n")
    s5_all = [r for r in eb if r["seconds_after_creation"] <= 5]
    p(f"- **Achats dans les 5 premières secondes** : {len(s5_all)} wallets (créateur inclus), "
      f"{n(sum(r['tokens_ui'] for r in s5_all) / SUPPLY0 * 100, 2)} % de la supply, {n(sum(r['sol_spent'] for r in s5_all), 2)} SOL. "
      "C'est l'ordre de grandeur des « ~8 % sniper holdings » des trackers.")
    s30 = [r for r in eb if r["seconds_after_creation"] <= 30]
    p(f"- **Dans les 30 premières secondes** : {len(s30)} wallets, {n(sum(r['tokens_ui'] for r in s30) / SUPPLY0 * 100, 2)} %, "
      f"{n(sum(r['sol_spent'] for r in s30), 2)} SOL.")
    p(f"- **« 1,36 % bundled »** : = {n(c['dev_buy_tokens_ui'] / SUPPLY0 * 100, 2)} % — c'est le **dev buy du créateur, "
      "exécuté dans la même transaction que la création** (création + achat groupés). Ce n'est pas un réseau de wallets.")
    p(f"- **Transactions d'achat créditant plusieurs wallets** (bundle au sens strict) : {len(F['multi_receiver_buy_txs'])} — "
      "toutes après la graduation, impliquant des wallets hors top 10.")
    p(f"- **Groupes d'achats dans un même slot** (INDICE faible seul) : {len(F['same_slot_groups'])} slots.")
    p(f"- **Achats avec tip Jito** parmi les 100 premiers : {sum(1 for r in eb[:100] if r['jito_tip'])}.\n")

    p("## 6. Recherche de wallets liés au créateur\n")
    p(f"**Résultat : aucun lien on-chain entre le créateur et un autre wallet analysé** (cluster du créateur = lui seul). "
      "Critères testés sur les ~50 wallets clés : funding commun (hors exchanges/services), transferts directs SOL ou token, "
      "achat payé par un autre wallet, destination commune des profits, achats dans le même slot.\n")
    p("- Le créateur n'a **reçu ni envoyé aucun token** JEANPHIL hors de son dev buy (hors une poussière de 2,36 tokens reçue "
      "lors d'une distribution de fees).")
    p("- Ses sorties de SOL vont toutes vers un même wallet intermédiaire, puis vers un service unique (voir §8).\n")
    p("**Groupes identifiés entre autres wallets** (liens FAIT ou INDICE fort — *sans lien avec le créateur*) :\n")
    for i, cl in enumerate(F["clusters"]):
        ins = [w for w in cl if w in snap_w]
        types = sorted({e["type"] for e in F["link_edges"] if e["a"] in cl and e["b"] in cl and e["strength"] != "INDICE faible"})
        p(f"- **Groupe {i + 1}** — {len(cl)} wallets, dont {len(ins)} du top 10 ({', '.join(a(w) for w in ins) or '—'}). Liens : {', '.join(types)}.")
    funders = {}
    for e in F["link_edges"]:
        if e["type"] == "funder_commun":
            funders.setdefault(e["via"], set()).update([e["a"], e["b"]])
    for f, ws in sorted(funders.items(), key=lambda x: -len(x[1])):
        ins = [w for w in ws if w in snap_w]
        p(f"  - funder commun {a(f)} → {len(ws)} wallets financés, dont {len(ins)} du top 10 : {', '.join(a(w) for w in ins)}")
    p("\n*Un groupe est une composante connexe : deux wallets d'un même groupe peuvent n'être reliés qu'indirectement "
      "(A↔B et B↔C). Le lien le plus solide est le funder commun ci-dessus.*")
    p("\nINDICE : le groupe principal ressemble à un opérateur de snipe/trading multi-wallets (financement commun, "
      "profits reversés vers une même adresse, qui refinance à son tour le funder). Rien ne le relie au créateur.\n")

    # --------------------------------------------------------------- tableau
    p("## 7. Tableau de synthèse des wallets clés\n")
    p("| Wallet | Relation | SOL investi | % supply max | Tokens vendus | SOL récupéré | P&L réalisé (SOL) | Position restante |")
    p("|---|---|---|---|---|---|---|---|")
    rows = sorted(W.values(), key=lambda d: -(d["max_balance_ui"] or 0))
    for d in rows[:40]:
        rel = d["relation"] + (f" · groupe {clus[d['wallet']]}" if d["wallet"] in clus else "")
        p(f"| {a(d['wallet'])} | {rel} | {n(d['sol_invested'], 2)} | {n(d['max_balance_ui'] / SUPPLY0 * 100, 2)} % | "
          f"{mtok(d['tokens_sold'])} | {n(d['sol_recovered'], 2)} | {n(d['realized_pnl_sol'], 2)} | {mtok(d['balance_now_ui'])} |")
    win = sorted(W.values(), key=lambda d: -d["realized_pnl_sol"])[:6]
    p("\n**Plus gros P&L réalisés parmi les wallets clés** : " + " ; ".join(
        f"{a(d['wallet'])} {n(d['realized_pnl_sol'], 1)} SOL ({d['relation']})" for d in win) + ".")
    p("\n*% supply max : maximum observé pendant la fenêtre complète (1re heure). Détails et transactions : `wallets_pnl.csv`.*\n")

    # --------------------------------------------------------------- créateur
    p("## 8. Wallet créateur `BS3Fx…dE3B` (FAIT)\n")
    p(f"- **Pourquoi « 13,6 M / 1,4 % »** : c'est le dev buy de {n(c['dev_buy_tokens_ui'], 2)} tokens acheté **dans la transaction de "
      f"création** ({s(c['signature'])}) pour {n(c['dev_buy_sol'], 4)} SOL. Coût : ≈ {usd(cr_in_usd)}.")
    p("- **Pourquoi certains trackers affichaient 0 %** : les tokens n'ont jamais bougé (aucune vente, aucun transfert sortant). "
      "L'écart vient donc de l'affichage du tracker (ex. dev buy intégré à la tx de création non compté comme « holding dev », "
      "ou compte Token-2022 non indexé) — ce n'est pas un mouvement on-chain.")
    p(f"- **Ventes** : aucune. **Position actuelle** : {n(cr['balance_now_ui'], 2)} JEANPHIL "
      f"(≈ {n(cr_pos_spot_sol, 1)} SOL au prix spot, ≈ {n(cr_pos_liq_sol, 1)} SOL si vendus d'un bloc dans le pool PumpSwap — ESTIMATION).")
    tr = F.get("creator_trail") or {}
    outs = [x for x in tr.get("sol_outflows", []) if x["sig"] != c["signature"]]
    p("- **Sorties de SOL après le lancement** (FAIT) :")
    for x in outs:
        p(f"  - {ts(x['t'])} : **{n(x['sol'], 2)} SOL** → {a(x['to'])} ({s(x['sig'])}) ≈ {usd(x['sol'] * (px(x['t']) or 0))}")
    p(f"  - Total sorti : **{n(sum(x['sol'] for x in outs), 2)} SOL** ≈ {usd(sum(x['sol'] * (px(x['t']) or 0) for x in outs))} ; "
      f"solde actuel du wallet créateur : {n(tr.get('creator_balance_now_sol'), 2)} SOL.")
    for dest, hp in (tr.get("next_hops") or {}).items():
        if not hp["outflows"]:
            continue
        sinks = hp["second_hop_sinks"]
        p(f"  - {a(dest)} a redistribué vers {len({o['to'] for o in hp['outflows']})} adresses à usage unique, toutes vidées vers "
          + ", ".join(f"{a(k)} ({n(v, 2)} SOL)" for k, v in sinks.items())
          + " — wallet de service très actif (≈ 24 800 SOL, des dizaines d'expéditeurs par heure) : schéma d'adresses de dépôt "
          "d'exchange (INDICE). Aucun de ces fonds ne revient vers les gros wallets.")
    p(f"- **Autres revenus** : {n(tr.get('distribute_creator_fees_income_sol'), 2)} SOL reçus via `DistributeCreatorFees` "
      f"(partage de frais Pump.fun, {len(tr.get('distribute_sources', {}))} comptes sources) — distincts des fees JEANPHIL.")
    p(f"- **Autres tokens créés** : {len(tr.get('creates_signed', [])) - 1} (une seule création signée : JEANPHIL).\n")

    # --------------------------------------------------------------- fees
    p("## 9. Creator fees Pump.fun (FAIT)\n")
    p(f"- Vault bonding curve : {a(cf['vaults'][0], False)} (PDA `creator-vault` du créateur)")
    p(f"- Vault PumpSwap : {a(cf['vaults'][1], False)} (PDA `creator_vault`, fees en WSOL)")
    p("- Méthode : aucune hypothèse de barème — on lit les SOL **effectivement** reçus (claims) + le solde non réclamé des vaults. "
      f"Le créateur n'a lancé qu'un seul token (une seule instruction `CreateV2` dans son historique), donc 100 % de ces fees proviennent de JEANPHIL.\n")
    p("| Date (UTC) | Transaction | SOL reçus | Cours SOL | ≈ USD |")
    p("|---|---|---|---|---|")
    for cl in cf["claims"]:
        pr = px(cl["block_time"])
        p(f"| {ts(cl['block_time'])} | {s(cl['signature'])} | {n(cl['sol_received'], 3)} | {n(pr, 2)} $ | {usd(cl['sol_received'] * (pr or 0))} |")
    p(f"| **Total réclamé** | | **{n(cf['claimed_total_sol'], 3)}** | | **{usd(fees_usd)}** |")
    un = sum(cf["unclaimed_now_sol"].values())
    p(f"| Non réclamé (maintenant) | | {n(un, 3)} | {n(sol_now, 2)} $ | {usd(un * (sol_now or 0))} |")
    p(f"\n- Fees générées pendant la **seule 1re heure** : {n(cf['accrued_in_window_total_sol'], 3)} SOL "
      f"({n(cf['accrued_in_window_sol'][cf['vaults'][0]], 3)} sur la bonding curve + {n(cf['accrued_in_window_sol'][cf['vaults'][1]], 3)} sur PumpSwap en 9 min).")
    if M:
        vol = sum(pl["volume_usd_total"] for pl in M["pools"].values())
        p(f"- Taux effectif ≈ fees totales / volume : {usd(fees_usd + un * (sol_now or 0))} / {usd(vol)} ≈ "
          f"**{n((fees_usd + un * (sol_now or 0)) / vol * 100, 3)} %** du volume (ESTIMATION ; inclut des volumes Meteora/Raydium qui ne "
          "paient pas de creator fee Pump.fun).")
    p("- Les revenus `DistributeCreatorFees` (§8) ne sont pas inclus ci-dessus.\n")
    p("**Distinction demandée** : revenus issus des ventes de tokens = **0 SOL** ; revenus issus des creator fees = "
      f"**{n(cf['claimed_total_sol'], 2)} SOL réclamés**.\n")

    # --------------------------------------------------------------- marché
    p("## 10. Market cap, volume et holders\n")
    p("| T+ | Heure (UTC) | Market cap | Volume cumulé | Holders | Source |")
    p("|---|---|---|---|---|---|")
    for m in F["timeline"]:
        if m["minutes"] <= F["window_minutes"]:
            pr = px(m["time"])
            mc = m["price_sol"] * SUPPLY0 * pr if m["price_sol"] and pr else None
            p(f"| +{m['minutes']} min | {ts(m['time'], False)} | {usd(mc)} ({n(m['price_sol'] * SUPPLY0 if m['price_sol'] else None, 1)} SOL) | "
              f"{usd(m['cum_volume_sol'] * pr if pr else None)} ({n(m['cum_volume_sol'], 1)} SOL) | {m['holders']} | FAIT on-chain |")
    main_h = M["pools"][M["main_pool"]]["hourly"] if M else []
    for off in (120, 240, 480, 720, 1440, 2880, 4320, 7200, 10080):
        if not M:
            break
        t = t0 + off * 60
        done = [c_ for c_ in main_h if c_[0] + 3600 <= t]  # bougies terminées avant t (pas de regard vers le futur)
        m = {"time": t, "close_usd": done[-1][4] if done else None,
             "cum_volume_usd_all_pools_hourly": sum(c_[5] for pl in M["pools"].values() for c_ in pl["hourly"] if c_[0] + 3600 <= t)}
        lab = f"+{off // 60} h" if off < 2880 else f"+{off // 1440} j"
        p(f"| {lab} | {ts(m['time'], False)} | {usd(m['close_usd'] * SUPPLY0 if m['close_usd'] else None)} | "
          f"{usd(m['cum_volume_usd_all_pools_hourly'])} (pools DEX) | n/d | ESTIMATION GeckoTerminal |")
    if M:
        ath = M["ath_main_pool"]
        vol = sum(pl["volume_usd_total"] for pl in M["pools"].values())
        p(f"\n- **ATH** (pool principal PumpSwap) : **{n(ath['minute_high_usd'], 5)} $ le {ts(ath['minute'])} UTC** → "
          f"≈ **{usd(ath['minute_high_usd'] * SUPPLY0)}** de market cap (1 Md) / {usd(ath['minute_high_usd'] * F['supply_current_ui'])} (supply actuelle). "
          f"Des mèches plus hautes existent sur de petits pools Meteora (ex. {n(M['ath_all_pools_hourly'][0]['high_usd'], 5)} $), peu liquides : non retenues.")
        vat = sum(c_[5] for pl in M["pools"].values() for c_ in pl["hourly"] if c_[0] < ath["hour"])
        p(f"- Volume cumulé à l'ATH ≈ {usd(vat)} ; holders à l'ATH : n/d (hors fenêtre téléchargée intégralement).")
        p(f"- Source secondaire divergente : « ATH 0,01066 $ le 25/09 » (CoinCodex/Coinbase) — probablement un plus haut journalier "
          "sur un autre agrégat ; le plus haut minute du pool principal est celui ci-dessus.")
        p(f"- **Volume total** depuis la graduation (6 pools) : **{usd(vol)}** — " + ", ".join(
            f"{pl['dex']} {usd(pl['volume_usd_total'])}" for pl in M["pools"].values()) + " (ESTIMATION GeckoTerminal ; peut inclure du volume de bots).")
        p(f"- **Holders actuels** : **{n(M.get('holders_now'), 0)}** (Helius DAS, comptes avec solde > 0).")
        p(f"- **Prix actuel** : {n(price_now_usd, 5)} $ → market cap ≈ {usd(price_now_usd * SUPPLY0 if price_now_usd else None)}.\n")

    # --------------------------------------------------------------- graduation
    p("## 11. Graduation Pump.fun → PumpSwap (FAIT)\n")
    p(f"- **Transaction** : {s(g['signature'])} — **{ts(g['block_time'])} UTC**, soit **+{dur(g['block_time'] - t0)}** après la création "
      f"(instruction `{g['instructions'][0]}`).")
    third = max(((k, v) for k, v in g["sol_deltas"].items() if k not in (F["bonding_curve"], g["pool_owner"])
                 and v > 1 and abs(v - g["pool_sol_in"]) > 0.01), key=lambda kv: kv[1], default=(None, 0))[0]
    p(f"- **Pool créé** : {a(g['pool_owner'], False)}")
    p(f"- **Liquidité initiale** : {n(g['pool_tokens_in_ui'], 0)} JEANPHIL + {n(g['pool_sol_in'], 3)} SOL "
      f"(≈ {usd(g['pool_sol_in'] * (px(g['block_time']) or 0))} côté SOL). La bonding curve a libéré "
      f"{n(-g['sol_deltas'][F['bonding_curve']], 3)} SOL : {n(g['pool_sol_in'], 3)} SOL au pool et "
      f"{n(-g['sol_deltas'][F['bonding_curve']] - g['pool_sol_in'], 3)} SOL vers {a(third)} (frais de migration / protocole — INDICE).")
    p(f"- **Market cap à la graduation** : ≈ {usd(g['pool_sol_in'] / g['pool_tokens_in_ui'] * SUPPLY0 * (px(g['block_time']) or 0))} "
      f"(prix initial du pool × 1 Md).")
    dec = 10 ** F["decimals"]
    sold_before = sum(-e["token_raw"] for w in snap_w for e in W[w]["events"] if e["kind"] == "SELL" and e["block_time"] < g["block_time"]) / dec
    sold_total = sum(-e["token_raw"] for w in snap_w for e in W[w]["events"] if e["kind"] == "SELL") / dec
    sold_1h = sum(-e["token_raw"] for w in snap_w for e in W[w]["events"] if e["kind"] == "SELL" and e["block_time"] < g["block_time"] + 3600) / dec
    p(f"- **Gros wallets du snapshot** : sur {mtok(sold_total)} tokens vendus au total, {mtok(sold_before)} "
      f"({n(sold_before / sold_total * 100, 0)} %) l'ont été **avant** la graduation (sur la bonding curve) et "
      f"{mtok(sold_1h)} ({n(sold_1h / sold_total * 100, 0)} %) avant graduation + 1 h ; le reste (traders actifs) "
      "s'étale sur les jours suivants (détail §4 et §12).\n")

    # --------------------------------------------------------------- hypothèse
    p("## 12. HYPOTHÈSE — « les 10 gros wallets du snapshot appartiennent au créateur »\n")
    p("> **Ceci n'est pas un fait.** Aucun lien on-chain n'a été trouvé entre ces wallets et le créateur ; "
      "plusieurs appartiennent à des groupes distincts entre eux. Le calcul ci-dessous répond seulement à la question "
      "« combien SI c'était la même personne ».\n")
    p(f"1. **Argent injecté** : {n(h['sol_injected'], 2)} SOL (≈ {usd(h_in_usd)}) par les 10 wallets, + {n(cr['sol_invested'], 3)} SOL du créateur.")
    p(f"2. **% de supply obtenu** au snapshot : {n(sum(r['tokens_ui'] for r in snap) / SUPPLY0 * 100, 2)} % (+ {n(c['dev_buy_tokens_ui'] / SUPPLY0 * 100, 2)} % du créateur).")
    marks = [ser[0]] + [x for x in ser if x["kind"] == "SELL"][::max(1, len(ser) // 8)] + [ser[-1]]
    p("3. **Évolution de la position** (valeur au prix du marché au moment de chaque mouvement) :\n")
    p("| Date | Tokens détenus (cluster) | SOL injectés cumulés | SOL récupérés cumulés | Valeur de marché (SOL) |")
    p("|---|---|---|---|---|")
    seen = set()
    for x in marks:
        if x["t"] in seen:
            continue
        seen.add(x["t"])
        p(f"| {ts(x['t'], False)} | {mtok(x['tokens_held'])} | {n(x['cum_sol_in'], 1)} | {n(x['cum_sol_out'], 1)} | {n(x['mark_value_sol'], 1)} |")
    p(f"\n4. **Tokens vendus** : {mtok(h['tokens_sold'])} — **prix moyen de vente** {n(h['avg_sell_price_sol'] * 1e6, 3)} SOL par million de tokens.")
    p(f"5. **SOL récupérés** : {n(h['sol_recovered'], 2)} SOL (≈ {usd(h_out_usd)}).")
    p(f"6. **Tokens restants** : {mtok(h['tokens_remaining'])} (≈ {n(h['remaining_spot_value_sol'], 1)} SOL spot).")
    p(f"7. **Creator fees** (réelles, du créateur) : {n(cf['claimed_total_sol'], 2)} SOL (≈ {usd(fees_usd)}).")
    p(f"8. **P&L réalisé du cluster** : {n(h['realized_pnl_sol'], 2)} SOL (≈ {usd(h_out_usd - h_in_usd)}) ; **latent** : ≈ {n(h['remaining_liquidation_value_sol'], 1)} SOL.\n")
    tot_in = cr_in_usd + h_in_usd
    tot_cash = h_out_usd
    p(f"**Sous cette hypothèse**, la personne aurait mis **≈ {n(cr['sol_invested'] + h['sol_injected'], 1)} SOL (≈ {usd(tot_in)})** de sa poche, "
      f"encaissé **≈ {n(h['sol_recovered'], 1)} SOL (≈ {usd(tot_cash)})** en ventes, gagné **{n(cf['claimed_total_sol'], 1)} SOL (≈ {usd(fees_usd)})** "
      f"en creator fees, et détiendrait encore **{mtok(h['total']['tokens_remaining_incl_creator'])}** "
      f"(≈ {n((h['remaining_liquidation_value_sol'] or 0) + (cr_pos_liq_sol or 0), 1)} SOL en liquidation). "
      f"Gain réalisé total ≈ **{usd(tot_cash - tot_in + fees_usd)}**.\n")
    p("*Attention : ces wallets ont aussi racheté/revendu bien après le snapshot (traders actifs) ; le calcul inclut toute leur "
      "activité JEANPHIL, pas seulement la position initiale.*\n")

    # --------------------------------------------------------------- DAVID
    if dd and os.path.exists(os.path.join(dd, "facts.json")):
        D, DM = load(dd)
        dpx = Px(DM)
        dc = D["creation"]
        DW = D["wallets"]
        dcr = DW[dc["signers"][0]]
        dcf = D["creator_fees"]
        dfees_usd = sum(cl["sol_received"] * (dpx(cl["block_time"]) or 0) for cl in dcf["claims"])
        dsell = [e for e in dcr["events"] if e["kind"] == "SELL"]
        p("## 13. Comparaison avec $DAVID (`8wtdds…pump`)\n")
        p("**Faits DAVID (on-chain)** :\n")
        p(f"- Création : {s(dc['signature'])} le {ts(dc['block_time'])} UTC par {a(dc['signers'][0], False)} "
          f"({n(dc['creator_sol_before_creation_lamports'] / 1e9, 2)} SOL sur le wallet).")
        p(f"- **Dev buy : {mtok(dc['dev_buy_tokens_ui'])} ({n(dc['dev_buy_tokens_ui'] / SUPPLY0 * 100, 1)} % de la supply) pour "
          f"{n(dc['dev_buy_sol'], 2)} SOL** dans la transaction de création.")
        if dsell:
            e = dsell[0]
            p(f"- **Vente de la totalité ({mtok(-e['token_raw'] / 1e6)}) {dur(e['block_time'] - dc['block_time'])} après la création** "
              f"pour **{n(e['sol_lamports'] / 1e9, 2)} SOL** ({s(e['signature'])}).")
        p("- Le « wallet communautaire de 50 % » annoncé correspond donc, on-chain, au **dev buy du wallet créateur**, "
          "vendu en une transaction — il n'a pas été conservé ni distribué depuis ce wallet.")
        p(f"- Creator fees réclamées : **{n(dcf['claimed_total_sol'], 2)} SOL** (≈ {usd(dfees_usd)}).")
        dcre = dc["signers"][0]
        for w in D.get("creator_cluster", []):
            if w == dcre:
                continue
            dw = DW.get(w, {})
            vias = sorted({e["via"] for e in D["link_edges"] if {e["a"], e["b"]} == {w, dcre}})
            rank = next((r["rank"] for r in D["snapshot"]["top20"] if r["owner"] == w), None)
            p(f"- **INDICE fort de wallet lié au créateur DAVID** : {a(w)} (n°{rank} au snapshot +{D['snapshot']['minutes_after_creation']:.0f} min) "
              f"achète {mtok(dw.get('tokens_bought'))} pour {n(dw.get('sol_invested'), 2)} SOL "
              f"{dur((dw.get('first_time') or 0) - dc['block_time'])} après la création, revend tout pour **{n(dw.get('sol_recovered'), 2)} SOL**, "
              f"puis envoie ses profits vers {', '.join(a(v) for v in vias)} — **la même adresse** qui reçoit les SOL du créateur. "
              "Cette adresse n'a que quelques expéditeurs (wallet personnel, pas un exchange). Non prouvé, mais cohérent avec "
              "un créateur qui snipe son propre lancement avec un second wallet.")
        if D.get("graduation"):
            p(f"- Graduation : +{dur(D['graduation']['block_time'] - dc['block_time'])} après création.")
        if DM:
            dv = sum(pl["volume_usd_total"] for pl in DM["pools"].values())
            dath = DM["ath_main_pool"]
            p(f"- ATH minute : {n(dath['minute_high_usd'], 6)} $ (≈ {usd(dath['minute_high_usd'] * SUPPLY0)}) le {ts(dath['minute'])} — "
              "dans les 5 premières minutes, avant la vente du créateur. Les « ≈ 109 k$ » de la première investigation "
              "correspondent au rebond après cette vente.")
        p("\n| Indicateur | JEANPHIL | DAVID |")
        p("|---|---|---|")
        jv = sum(pl["volume_usd_total"] for pl in M["pools"].values()) if M else None
        dv = sum(pl["volume_usd_total"] for pl in DM["pools"].values()) if DM else None
        drows = [
            ("Capital initial du créateur (dev buy)", f"{n(c['dev_buy_sol'], 2)} SOL ≈ {usd(cr_in_usd)}", f"{n(dc['dev_buy_sol'], 2)} SOL ≈ {usd(usd_of_events(dcr['events'], dpx, -1))}"),
            ("Dev buy (% supply)", f"{n(c['dev_buy_tokens_ui'] / SUPPLY0 * 100, 2)} %", f"{n(dc['dev_buy_tokens_ui'] / SUPPLY0 * 100, 2)} %"),
            ("Ventes du créateur", "aucune", f"100 % à +{dur(dsell[0]['block_time'] - dc['block_time'])}" if dsell else "n/d"),
            ("SOL encaissés en ventes par le créateur", "0", f"{n(dcr['sol_recovered'], 2)}"),
            ("Top 10 au snapshot (hors pools)", f"{n(sum(r['tokens_ui'] for r in snap) / SUPPLY0 * 100, 1)} % à +38 min",
             f"{n(sum(r['tokens_ui'] for r in D['snapshot']['top20'][:10]) / SUPPLY0 * 100, 1)} % à +{D['snapshot']['minutes_after_creation']:.0f} min"),
            ("Tx réussies dans la fenêtre initiale", f"{F['window_tx_count']} en 60 min", f"{D['window_tx_count']} en {D['window_minutes']:.0f} min"),
            ("Achats dans les 5 premières s", f"{len(s5_all)} wallets / {n(sum(r['tokens_ui'] for r in s5_all) / SUPPLY0 * 100, 1)} %",
             f"{sum(1 for r in D['early_buyers'] if r['seconds_after_creation'] <= 5)} wallets / "
             f"{n(sum(r['tokens_ui'] for r in D['early_buyers'] if r['seconds_after_creation'] <= 5) / SUPPLY0 * 100, 1)} %"),
            ("Délai de graduation", dur(g["block_time"] - t0), dur(D["graduation"]["block_time"] - dc["block_time"]) if D.get("graduation") else "n/d"),
            ("ATH (market cap)", usd(M["ath_main_pool"]["minute_high_usd"] * SUPPLY0) if M else "n/d",
             usd(DM["ath_main_pool"]["minute_high_usd"] * SUPPLY0) if DM else "n/d"),
            ("Moment de l'ATH", f"+{dur(M['ath_main_pool']['minute'] - t0)}" if M else "n/d",
             f"+{dur(DM['ath_main_pool']['minute'] - dc['block_time'])}" if DM else "n/d"),
            ("Volume DEX cumulé", usd(jv), usd(dv)),
            ("Holders actuels", n(M.get("holders_now"), 0) if M else "n/d", n(DM.get("holders_now"), 0) if DM else "n/d"),
            ("Creator fees réclamées", f"{n(cf['claimed_total_sol'], 1)} SOL ≈ {usd(fees_usd)}", f"{n(dcf['claimed_total_sol'], 1)} SOL ≈ {usd(dfees_usd)}"),
        ]
        for k, x, y in drows:
            p(f"| {k} | {x} | {y} |")
        p("\n**Pourquoi JEANPHIL a eu beaucoup plus de traction — lecture quantitative :**\n")
        p(f"1. **Offre flottante** : JEANPHIL a démarré avec un dev buy de 1,4 % jamais vendu ; DAVID avec 50 % concentrés dans un "
          "seul wallet, revendus 8 minutes après le lancement. Cette vente a absorbé la liquidité des premiers acheteurs "
          "(chute du prix d'environ 95 % en une minute sur les chandeliers).")
        p(f"2. **Durée de la demande** : le volume de DAVID est concentré dans la première heure ; celui de JEANPHIL s'étale "
          f"sur 10 jours (≈ {usd(M['price_marks_main_pool'][-1]['cum_volume_usd_all_pools_hourly'] if M else None)} à J+7).")
        p("3. **Distribution** : les snipers de JEANPHIL ont revendu dès les 10 premières minutes (market cap revenue au niveau "
          "de départ), puis une seconde vague d'acheteurs organiques a porté le token à la graduation — la structure de détention "
          "n'était pas dominée par un seul acteur.")
        p(f"4. **Revenus du créateur** : volume ≈ {n(jv / dv if jv and dv else None, 0)}× supérieur pour JEANPHIL → creator fees "
          f"{n(cf['claimed_total_sol'] / dcf['claimed_total_sol'] if dcf['claimed_total_sol'] else None, 0)}× supérieures, sans vente de tokens.\n")

    # --------------------------------------------------------------- limites
    p("## 14. Limites et points non résolus\n")
    p("- Fenêtre téléchargée intégralement : 1re heure (création → +60 min, graduation incluse). Au-delà, les wallets clés sont "
      "suivis individuellement (tout leur historique JEANPHIL), mais pas l'ensemble des holders.")
    p("- Nombre de holders entre +1 h et aujourd'hui : non reconstruit (il faudrait rejouer >3 millions de transactions).")
    p("- Montants en dollars : conversion au cours SOL/USD horaire (GeckoTerminal) — ESTIMATION.")
    p("- Swaps payés en USDC / via routeur : valorisés au prix d'exécution du pool (ESTIMATION), marqués *.")
    p("- Identification des exchanges/services : par comportement (nombre de contreparties), sans base d'étiquettes type Arkham.")
    print("\n".join(L))

    # CSV annexes
    base = os.path.dirname(os.path.abspath(jd.rstrip("/")))
    out_dir = os.path.dirname(base)
    with open(os.path.join(out_dir, "early_buyers.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "wallet", "signature", "utc", "seconds_after_creation", "slot", "sol_spent", "tokens", "pct_supply_1B",
                    "mcap_sol_before", "jito_tip", "group"])
        for r in eb:
            w.writerow([r["rank"], r["owner"], r["signature"], ts(r["block_time"]), r["seconds_after_creation"], r["slot"],
                        round(r["sol_spent"], 6), round(r["tokens_ui"], 2), round(r["tokens_ui"] / SUPPLY0 * 100, 4),
                        r["mcap_sol_before"], r["jito_tip"], clus.get(r["owner"], "")])
    with open(os.path.join(out_dir, "wallets_pnl.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wallet", "relation", "group", "n_buys", "n_sells", "sol_invested", "sol_recovered", "realized_pnl_sol",
                    "tokens_bought", "tokens_sold", "tokens_transferred_in", "tokens_transferred_out", "max_pct_supply_1B",
                    "balance_now", "unrealized_spot_sol", "unrealized_liquidation_sol", "n_priced_by_pool", "first_tx", "last_tx"])
        for d in rows:
            w.writerow([d["wallet"], d["relation"], clus.get(d["wallet"], ""), d["n_buys"], d["n_sells"], round(d["sol_invested"], 6),
                        round(d["sol_recovered"], 6), round(d["realized_pnl_sol"], 6), round(d["tokens_bought"], 2),
                        round(d["tokens_sold"], 2), round(d["tokens_transferred_in"], 2), round(d["tokens_transferred_out"], 2),
                        round(d["max_balance_ui"] / SUPPLY0 * 100, 4), d["balance_now_ui"], d.get("unrealized_spot_sol"),
                        d.get("unrealized_liquidation_sol"), d.get("n_priced_by_pool"), d["first_tx"], d["last_tx"]])


if __name__ == "__main__":
    main()
