#!/usr/bin/env python3
"""Investigation on-chain d'un token Pump.fun (JEANPHIL par défaut).

Usage :
  export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=..."   # recommandé
  python3 investigate.py --out ../data/jeanphil
  python3 investigate.py --mint 8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump --out ../data/david

Tout ce qui sort de ce script est dérivé des transactions on-chain.
Chaque résultat est étiqueté FAIT / INDICE / HYPOTHÈSE / ESTIMATION dans
report.py. Aucun wallet ni transaction n'est inventé : si une donnée manque,
le champ vaut None et le rapport l'indique.
"""
import argparse
import bisect
import csv
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import LAMPORTS, WSOL, instruction_names, parse_tx, sol_deltas_by_owner, sol_transfers, token_deltas  # noqa: E402
from rpc import Rpc  # noqa: E402

JEANPHIL_MINT = "GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump"
JEANPHIL_CREATOR = "BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B"
PUMP = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
PUMPSWAP = "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"
TIMELINE_OFFSETS = [0, 5, 15, 30, 38, 60, 120, 240, 480, 720, 1440]  # minutes
# Un "funder" qui a financé plus que ce nombre de wallets distincts dans
# son historique récent est traité comme un hub (CEX, bridge, service) :
# il ne crée PAS de lien entre wallets.
HUB_THRESHOLD = 40


def pda(seeds, program):
    try:
        from solders.pubkey import Pubkey
    except ImportError:
        return None
    return str(Pubkey.find_program_address(seeds, Pubkey.from_string(program))[0])


def b58(s):
    from solders.pubkey import Pubkey
    return bytes(Pubkey.from_string(s))


class Investigation:
    def __init__(self, rpc, mint, creator, out, snapshot_min=38, max_tx=None, wallet_scan_limit=3000, exclude=()):
        self.rpc, self.mint, self.creator, self.out = rpc, mint, creator, out
        self.snapshot_min, self.max_tx, self.wallet_scan_limit = snapshot_min, max_tx, wallet_scan_limit
        self.events, self.txs = [], {}
        self.infra = set(exclude)  # + wallets exclus (ex. wallet communautaire DAVID)
        self.facts = {"mint": mint, "creator_declared": creator, "warnings": []}
        os.makedirs(out, exist_ok=True)

    def warn(self, msg):
        print("WARN:", msg, file=sys.stderr)
        self.facts["warnings"].append(msg)

    # ------------------------------------------------------------------ 1
    def load_mint_history(self):
        sigs = self.rpc.signatures(self.mint)
        sigs = [s for s in sigs if s.get("err") is None]
        sigs.sort(key=lambda s: (s.get("slot") or 0, s.get("blockTime") or 0))
        self.facts["mint_signature_count"] = len(sigs)
        if self.max_tx and len(sigs) > self.max_tx:
            self.warn(f"{len(sigs)} signatures sur le mint ; seules les {self.max_tx} premières sont analysées "
                      "(--max-tx). ATH/ventes tardives peuvent manquer.")
            sigs = sigs[: self.max_tx]
        for i, s in enumerate(sigs):
            if i % 500 == 0:
                print(f"  tx {i}/{len(sigs)}", file=sys.stderr)
            self.txs[s["signature"]] = self.rpc.tx(s["signature"])
        self.order = [s["signature"] for s in sigs if self.txs.get(s["signature"])]

    def supply(self):
        v = self.rpc.token_supply(self.mint)["value"]
        self.decimals = v["decimals"]
        self.supply_ui = int(v["amount"]) / 10 ** self.decimals
        self.facts["supply_current_ui"] = self.supply_ui
        self.facts["decimals"] = self.decimals

    # ------------------------------------------------------------------ 2
    def creation(self):
        first = self.txs[self.order[0]]
        names = instruction_names(first)
        keys = [k["pubkey"] for k in first["transaction"]["message"]["accountKeys"]]
        signers = [k["pubkey"] for k in first["transaction"]["message"]["accountKeys"] if k.get("signer")]
        tok, _ = token_deltas(first, self.mint)
        sol = sol_deltas_by_owner(first)
        is_create = any(n.lower().startswith("create") for n in names)
        c = {
            "signature": self.order[0], "slot": first["slot"], "block_time": first["blockTime"],
            "instructions": names, "signers": signers, "fee_payer": keys[0], "is_create_instruction": is_create,
            "creator_sol_delta_lamports": sol.get(keys[0]),
            "token_deltas_raw": tok,
        }
        if not is_create:
            self.warn("La plus ancienne tx du mint ne contient pas d'instruction Create : historique incomplet ?")
        if self.creator and self.creator not in signers:
            self.warn(f"Le créateur déclaré {self.creator} n'est pas signataire de la tx de création "
                      f"(signataires : {signers}).")
        if not self.creator:
            self.creator = keys[0]
        # Achat du créateur dans la tx de création (dev buy)
        c["dev_buy_raw"] = tok.get(self.creator, 0)
        self.t0, self.slot0 = first["blockTime"], first["slot"]
        self.facts["creation"] = c
        # Infra : bonding curve (PDA dérivée, sinon plus gros receveur non signataire)
        bc = pda([b"bonding-curve", b58(self.mint)], PUMP) if self._has_solders() else None
        if bc is None:
            non_sign = {o: d for o, d in tok.items() if o not in signers}
            bc = max(non_sign, key=non_sign.get) if non_sign else None
        if bc:
            self.infra.add(bc)
        self.facts["bonding_curve"] = bc
        self.facts["pump_creator_vault"] = pda([b"creator-vault", b58(self.creator)], PUMP) if self._has_solders() else None
        self.facts["pumpswap_creator_vault_authority"] = (
            pda([b"creator_vault", b58(self.creator)], PUMPSWAP) if self._has_solders() else None)

    @staticmethod
    def _has_solders():
        import importlib.util
        return importlib.util.find_spec("solders") is not None

    # ------------------------------------------------------------------ 3
    def detect_infra(self):
        """Pools : propriétaires jamais signataires qui sont contrepartie de
        nombreux swaps. La tx de migration identifie le pool PumpSwap."""
        seen, signer_count = defaultdict(int), defaultdict(int)
        grad = None
        for sig in self.order:
            tx = self.txs[sig]
            names = instruction_names(tx)
            tok, _ = token_deltas(tx, self.mint)
            signers = {k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"] if k.get("signer")}
            for o in tok:
                seen[o] += 1
                if o in signers:
                    signer_count[o] += 1
            if grad is None and any("migrate" in n.lower() for n in names):
                grad = sig
        for o, n in seen.items():
            if n >= 50 and signer_count[o] == 0:
                self.infra.add(o)
        self.facts["infra_owners"] = sorted(self.infra)
        self.facts["graduation_signature"] = grad
        if grad:
            tx = self.txs[grad]
            tok, _ = token_deltas(tx, self.mint)
            sol = sol_deltas_by_owner(tx)
            recv = {o: d for o, d in tok.items() if d > 0}
            pool = max(recv, key=recv.get) if recv else None
            self.infra.add(pool) if pool else None
            self.facts["graduation"] = {
                "signature": grad, "block_time": tx["blockTime"], "slot": tx["slot"],
                "minutes_after_creation": (tx["blockTime"] - self.t0) / 60,
                "instructions": instruction_names(tx),
                "pool_owner": pool,
                "pool_tokens_in_ui": recv.get(pool, 0) / 10 ** self.decimals if pool else None,
                "pool_sol_in": (sol.get(pool, 0) / LAMPORTS) if pool else None,
                "token_deltas_ui": {o: d / 10 ** self.decimals for o, d in tok.items()},
                "sol_deltas": {o: d / LAMPORTS for o, d in sol.items() if abs(d) > 1_000_000},
            }
        else:
            self.warn("Aucune instruction Migrate trouvée dans l'historique analysé.")

    # ------------------------------------------------------------------ 4
    def build_events(self):
        for sig in self.order:
            self.events.extend(parse_tx(self.txs[sig], self.mint, frozenset(self.infra)))
        self.events.sort(key=lambda e: (e["slot"], e["block_time"] or 0))
        # Série de prix côté pool (lamports / unité brute -> SOL / token)
        self.price_t, self.price_v = [], []
        for e in self.events:
            p = e["pool_price_lamports_per_raw"]
            if p:
                self.price_t.append(e["block_time"])
                self.price_v.append(p * 10 ** self.decimals / LAMPORTS)

    def price_at(self, t):
        i = bisect.bisect_right(self.price_t, t) - 1
        return self.price_v[i] if i >= 0 else None

    def mcap_sol_at(self, t):
        p = self.price_at(t)
        return p * self.supply_ui if p else None

    def ui(self, raw):
        return raw / 10 ** self.decimals

    # ------------------------------------------------------------------ 5
    def replay(self):
        bal = defaultdict(int)
        max_bal = defaultdict(int)
        vol = 0
        marks = [self.t0 + m * 60 for m in TIMELINE_OFFSETS]
        timeline, mi = [], 0
        ath = {"price_sol": 0}
        snapshot = None
        snap_t = self.t0 + self.snapshot_min * 60

        def holders():
            return sum(1 for o, b in bal.items() if b > 0 and o not in self.infra)

        for e in self.events:
            while mi < len(marks) and e["block_time"] > marks[mi]:
                timeline.append(self._mark(TIMELINE_OFFSETS[mi], marks[mi], vol, holders()))
                mi += 1
            if snapshot is None and e["block_time"] > snap_t:
                snapshot = dict(bal)
            bal[e["owner"]] += e["token_raw"]
            max_bal[e["owner"]] = max(max_bal[e["owner"]], bal[e["owner"]])
            if e["kind"] in ("BUY", "SELL"):
                vol += abs(e["sol_lamports_ex_fee"]) / LAMPORTS
            p = e["pool_price_lamports_per_raw"]
            if p:
                ps = p * 10 ** self.decimals / LAMPORTS
                if ps > ath["price_sol"]:
                    ath = {"price_sol": ps, "block_time": e["block_time"], "signature": e["signature"],
                           "mcap_sol": ps * self.supply_ui, "cum_volume_sol": vol, "holders": None}
                    ath["_holders_pending"] = True
            if ath.get("_holders_pending") and ath.get("signature") == e["signature"]:
                ath["holders"] = holders()
        while mi < len(marks):
            timeline.append(self._mark(TIMELINE_OFFSETS[mi], marks[mi], vol, holders(), partial=True))
            mi += 1
        ath.pop("_holders_pending", None)
        if snapshot is None:
            snapshot = dict(bal)
        self.balances, self.max_bal = bal, max_bal
        self.facts["timeline"] = timeline
        self.facts["ath_observed"] = ath
        self.facts["total_volume_sol_observed"] = vol
        self.facts["holders_end_observed"] = holders()

        tot = 10 ** self.decimals * self.supply_ui
        top = sorted(((o, b) for o, b in snapshot.items() if b > 0 and o not in self.infra),
                     key=lambda x: -x[1])[:20]
        self.snapshot_top = [o for o, _ in top[:10]]
        self.facts["snapshot"] = {
            "minutes_after_creation": self.snapshot_min,
            "top20": [{"rank": i + 1, "owner": o, "tokens_ui": self.ui(b), "pct_supply": 100 * b / tot,
                       "is_creator": o == self.creator} for i, (o, b) in enumerate(top)],
            "top10_pct_total": sum(100 * b / tot for _, b in top[:10]),
        }

    def _mark(self, m, t, vol, holders, partial=False):
        p = self.price_at(t)
        return {"minutes": m, "time": t, "price_sol": p, "mcap_sol": p * self.supply_ui if p else None,
                "cum_volume_sol": vol, "holders": holders, "data_may_be_incomplete": partial}

    # ------------------------------------------------------------------ 6
    def early_buyers(self, n=100):
        first = {}
        for e in self.events:
            if e["kind"] not in ("BUY", "BUY_PAID_BY_OTHER"):
                continue
            o = e["owner"]
            if o not in first:
                first[o] = e
        ranked = sorted(first.values(), key=lambda e: (e["slot"], e["block_time"]))[:n]
        tot = 10 ** self.decimals * self.supply_ui
        rows = []
        for i, e in enumerate(ranked):
            rows.append({
                "rank": i + 1, "owner": e["owner"], "signature": e["signature"], "slot": e["slot"],
                "block_time": e["block_time"], "seconds_after_creation": e["block_time"] - self.t0,
                "same_slot_as_creation": e["slot"] == self.slot0, "slots_after_creation": e["slot"] - self.slot0,
                "kind": e["kind"], "sol_spent": -e["sol_lamports"] / LAMPORTS, "tokens_ui": self.ui(e["token_raw"]),
                "pct_supply": 100 * e["token_raw"] / tot,
                "mcap_sol_before": self.mcap_sol_at(e["block_time"] - 1),
                "jito_tip": e["jito_tip"], "fee_payer": e["fee_payer"],
                "paid_by": list(e["sol_payers"].keys()) if e["kind"] == "BUY_PAID_BY_OTHER" else None,
                "is_creator": e["owner"] == self.creator, "venues": e["venues"],
            })
        self.facts["early_buyers"] = rows
        # Regroupements par slot : achats dans le même bloc (indice de bundle)
        by_slot = defaultdict(list)
        for r in rows:
            by_slot[r["slot"]].append(r["owner"])
        self.facts["same_slot_groups"] = {s: o for s, o in by_slot.items() if len(o) > 1}
        # Bundles "stricts" : même signataire/payeur pour plusieurs receveurs dans une tx
        multi = defaultdict(set)
        for e in self.events:
            if e["kind"] in ("BUY", "BUY_PAID_BY_OTHER"):
                multi[e["signature"]].add(e["owner"])
        self.facts["multi_receiver_buy_txs"] = {s: sorted(o) for s, o in multi.items() if len(o) > 1}

    # ------------------------------------------------------------------ 7
    def wallet_deep_dive(self, wallets):
        """Historique complet de chaque wallet clé : swaps + transferts du token
        (y compris hors DEX), financement initial, destination des profits."""
        res = {}
        for w in wallets:
            print(f"  wallet {w}", file=sys.stderr)
            sigs = self.rpc.signatures(w, limit_total=self.wallet_scan_limit)
            truncated = len(sigs) >= self.wallet_scan_limit
            sigs = [s for s in sigs if s.get("err") is None]
            sigs.sort(key=lambda s: s.get("slot") or 0)
            evs, sol_in, sol_out, created_other = [], [], [], []
            first_activity = sigs[0] if sigs else None
            for s in sigs:
                tx = self.txs.get(s["signature"]) or self.rpc.tx(s["signature"])
                if tx is None:
                    continue
                evs.extend(e for e in parse_tx(tx, self.mint, frozenset(self.infra)) if e["owner"] == w)
                for src, dst, lam in sol_transfers(tx):
                    if dst == w and src != w:
                        sol_in.append({"from": src, "lamports": lam, "t": tx["blockTime"], "sig": s["signature"]})
                    elif src == w and dst != w:
                        sol_out.append({"to": dst, "lamports": lam, "t": tx["blockTime"], "sig": s["signature"]})
                names = instruction_names(tx)
                if any(n.lower().startswith("create") for n in names) and w in {
                        k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"] if k.get("signer")}:
                    if any(p.get("programId") == PUMP for p in tx["transaction"]["message"]["instructions"]):
                        created_other.append(s["signature"])
            evs.sort(key=lambda e: e["slot"])
            res[w] = self._pnl(w, evs)
            first_buy_t = next((e["block_time"] for e in evs if e["kind"].startswith("BUY")), None)
            res[w]["history_truncated"] = truncated
            res[w]["first_activity"] = ({"signature": first_activity["signature"],
                                         "block_time": first_activity.get("blockTime")} if first_activity else None)
            res[w]["funding_before_first_buy"] = [x for x in sol_in if first_buy_t is None or x["t"] <= first_buy_t][-10:]
            res[w]["first_funding"] = sol_in[:5]
            last_sell_t = max((e["block_time"] for e in evs if e["kind"] == "SELL"), default=None)
            res[w]["sol_out_after_first_sell"] = [x for x in sol_out if last_sell_t and x["t"] >= min(
                e["block_time"] for e in evs if e["kind"] == "SELL")][:30] if last_sell_t else []
            res[w]["pump_creates_signed"] = created_other
            res[w]["sol_in_all"] = sol_in
            res[w]["sol_out_all"] = sol_out
        return res

    def _pnl(self, w, evs):
        buys = [e for e in evs if e["kind"] == "BUY"]
        sells = [e for e in evs if e["kind"] == "SELL"]
        tin = [e for e in evs if e["kind"] in ("TRANSFER_IN", "BUY_PAID_BY_OTHER")]
        tout = [e for e in evs if e["kind"] == "TRANSFER_OUT"]
        sol_in = sum(-e["sol_lamports"] for e in buys) / LAMPORTS
        sol_out = sum(e["sol_lamports"] for e in sells) / LAMPORTS
        tok_b = self.ui(sum(e["token_raw"] for e in buys))
        tok_s = self.ui(-sum(e["token_raw"] for e in sells))
        live = self.live_balance(w)
        return {
            "wallet": w,
            "n_buys": len(buys), "n_sells": len(sells), "n_transfers_in": len(tin), "n_transfers_out": len(tout),
            "first_tx": evs[0]["signature"] if evs else None, "first_time": evs[0]["block_time"] if evs else None,
            "last_tx": evs[-1]["signature"] if evs else None, "last_time": evs[-1]["block_time"] if evs else None,
            "sol_invested": sol_in, "sol_recovered": sol_out, "realized_pnl_sol": sol_out - sol_in,
            "tokens_bought": tok_b, "tokens_sold": tok_s,
            "tokens_transferred_in": self.ui(sum(e["token_raw"] for e in tin)),
            "tokens_transferred_out": self.ui(-sum(e["token_raw"] for e in tout)),
            "transfer_in_sources": sorted({c for e in tin for c in e["counterparties"]} | {
                p for e in tin for p in e["sol_payers"]}),
            "transfer_out_destinations": sorted({c for e in tout for c in e["counterparties"]}),
            "avg_buy_price_sol": sol_in / tok_b if tok_b else None,
            "avg_sell_price_sol": sol_out / tok_s if tok_s else None,
            "max_balance_ui": self.ui(self.max_bal.get(w, 0)),
            "max_pct_supply": 100 * self.ui(self.max_bal.get(w, 0)) / self.supply_ui,
            "balance_now_ui": live,
            "events": [{k: e[k] for k in ("signature", "block_time", "kind", "token_raw", "sol_lamports",
                                          "venues", "counterparties", "jito_tip")} for e in evs],
        }

    def live_balance(self, w):
        try:
            r = self.rpc.token_accounts_by_owner(w, self.mint)
            return sum(int(a["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"])
                       for a in r["value"]) / 10 ** self.decimals
        except Exception as ex:  # noqa: BLE001
            self.warn(f"solde live indisponible pour {w}: {ex}")
            return None

    # ------------------------------------------------------------------ 8
    def pool_state(self):
        g = self.facts.get("graduation") or {}
        pool = g.get("pool_owner")
        if not pool:
            return None
        tok = self.rpc.token_accounts_by_owner(pool, self.mint)["value"]
        ws = self.rpc.token_accounts_by_owner(pool, WSOL)["value"]
        amt = lambda v: sum(int(a["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"]) for a in v)  # noqa: E731
        st = {"pool_owner": pool, "token_reserve_ui": amt(tok) / 10 ** self.decimals, "sol_reserve": amt(ws) / LAMPORTS}
        st["spot_price_sol"] = st["sol_reserve"] / st["token_reserve_ui"] if st["token_reserve_ui"] else None
        self.facts["pool_now"] = st
        return st

    @staticmethod
    def liquidation_value(tokens, pool, fee_bps):
        """SOL obtenus en vendant `tokens` d'un coup dans un pool x*y=k (avec slippage)."""
        if not pool or not tokens:
            return 0.0
        x = tokens * (1 - fee_bps / 10_000)
        return pool["sol_reserve"] * x / (pool["token_reserve_ui"] + x)

    # ------------------------------------------------------------------ 9
    def creator_fees(self):
        """Creator fees accumulées PAR CE TOKEN = somme des variations du vault
        créateur dans les trades de ce mint (le vault Pump.fun est commun à tous
        les tokens d'un même créateur, d'où ce calcul trade par trade)."""
        vaults = [v for v in (self.facts.get("pump_creator_vault"), self.facts.get("pumpswap_creator_vault_authority")) if v]
        acc = defaultdict(int)
        hits = defaultdict(int)
        for sig in self.order:
            tx = self.txs[sig]
            sd = sol_deltas_by_owner(tx)
            for v in vaults:
                if sd.get(v, 0) > 0:
                    acc[v] += sd[v]
                    hits[v] += 1
        claims = []
        for s in self.rpc.signatures(self.creator, limit_total=self.wallet_scan_limit):
            if s.get("err") is not None:
                continue
            tx = self.rpc.tx(s["signature"])
            names = [n.lower() for n in instruction_names(tx or {})]
            if any("collect" in n and "fee" in n for n in names):
                sd = sol_deltas_by_owner(tx)
                claims.append({"signature": s["signature"], "block_time": tx["blockTime"],
                               "sol_received": sd.get(self.creator, 0) / LAMPORTS, "instructions": names})
        claims.sort(key=lambda c: c["block_time"])
        self.facts["creator_fees"] = {
            "vaults": vaults,
            "accrued_from_this_token_sol": {v: acc[v] / LAMPORTS for v in vaults},
            "accrued_total_sol": sum(acc.values()) / LAMPORTS,
            "trades_crediting_vault": dict(hits),
            "claims": claims,
            "claimed_total_sol": sum(c["sol_received"] for c in claims),
            "note": ("Les claims couvrent TOUS les tokens du créateur (vault partagé) ; "
                     "accrued_total_sol est la part attribuable à ce mint."),
        }
        if not sum(hits.values()):
            self.warn("Aucun crédit vers les vaults créateur dérivés : fee sharing / changement de "
                      "destinataire des creator fees possible, à vérifier manuellement.")

    # ------------------------------------------------------------------ 10
    def links(self, deep):
        """Graphe d'indices entre wallets clés. Chaque arête garde sa preuve."""
        wallets = set(deep)
        funder_of = defaultdict(set)
        for w, d in deep.items():
            for f in d["funding_before_first_buy"] + d["first_funding"]:
                funder_of[f["from"]].add(w)
        # hubs : on vérifie combien de wallets distincts le funder finance
        hubs = set()
        for f, ws in funder_of.items():
            if len(ws) < 2:
                continue
            try:
                n = len({t for s in self.rpc.signatures(f, limit_total=300)
                         for (src, t, _) in sol_transfers(self.rpc.tx(s["signature"])) if src == f})
            except Exception:  # noqa: BLE001
                n = 0
            if n >= HUB_THRESHOLD:
                hubs.add(f)
        edges = []
        for f, ws in funder_of.items():
            if len(ws) >= 2 and f not in hubs:
                ws = sorted(ws)
                for i in range(len(ws)):
                    for j in range(i + 1, len(ws)):
                        edges.append({"a": ws[i], "b": ws[j], "type": "funder_commun", "via": f, "strength": "INDICE fort"})
            if f in wallets:
                for w in ws:
                    if w != f:
                        edges.append({"a": f, "b": w, "type": "financement_direct", "via": f, "strength": "FAIT (lien)"})
        for w, d in deep.items():
            for x in d["sol_out_all"]:
                if x["to"] in wallets and x["to"] != w:
                    edges.append({"a": w, "b": x["to"], "type": "transfert_SOL", "via": x["sig"], "strength": "FAIT (lien)"})
            for c in d["transfer_out_destinations"]:
                if c in wallets:
                    edges.append({"a": w, "b": c, "type": "transfert_token", "via": None, "strength": "FAIT (lien)"})
            for c in d["transfer_in_sources"]:
                if c in wallets and c != w:
                    edges.append({"a": c, "b": w, "type": "achat_payé_par_autre_ou_transfert", "via": None,
                                  "strength": "FAIT (lien)"})
        # destinations communes des profits
        dest = defaultdict(set)
        for w, d in deep.items():
            for x in d["sol_out_after_first_sell"]:
                dest[x["to"]].add(w)
        for t, ws in dest.items():
            if len(ws) >= 2 and t not in hubs:
                ws = sorted(ws)
                for i in range(len(ws)):
                    for j in range(i + 1, len(ws)):
                        edges.append({"a": ws[i], "b": ws[j], "type": "destination_commune_profits", "via": t,
                                      "strength": "INDICE fort"})
        # achats dans le même slot (INDICE faible seul)
        for slot, ws in self.facts.get("same_slot_groups", {}).items():
            ws = [w for w in ws if w in wallets]
            for i in range(len(ws)):
                for j in range(i + 1, len(ws)):
                    edges.append({"a": ws[i], "b": ws[j], "type": "même_slot", "via": slot, "strength": "INDICE faible"})
        # clusters par union-find sur liens FAIT / INDICE fort uniquement
        parent = {w: w for w in wallets}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for e in edges:
            if e["strength"] != "INDICE faible" and e["a"] in parent and e["b"] in parent:
                parent[find(e["a"])] = find(e["b"])
        groups = defaultdict(list)
        for w in wallets:
            groups[find(w)].append(w)
        self.facts["link_edges"] = edges
        self.facts["hubs_excluded"] = sorted(hubs)
        self.facts["clusters"] = [sorted(g) for g in groups.values() if len(g) > 1]
        self.facts["creator_cluster"] = sorted(groups[find(self.creator)]) if self.creator in parent else [self.creator]

    # ------------------------------------------------------------------ 11
    def hypothesis(self, deep, pool, fee_bps):
        """HYPOTHÈSE : les 10 plus gros wallets du snapshot appartiennent au créateur."""
        members = [w for w in self.snapshot_top if w in deep and w != self.creator]
        evs = sorted((dict(e, owner=w) for w in members for e in deep[w]["events"]), key=lambda e: e["block_time"])
        cum_in = cum_out = tok = 0.0
        series = []
        for e in evs:
            t = self.ui(e["token_raw"])
            if e["kind"] == "BUY":
                cum_in += -e["sol_lamports"] / LAMPORTS
            elif e["kind"] == "SELL":
                cum_out += e["sol_lamports"] / LAMPORTS
            # transferts internes au cluster : neutres
            if e["kind"].startswith("TRANSFER") and all(c in members for c in e["counterparties"]):
                pass
            else:
                tok += t
            p = self.price_at(e["block_time"])
            series.append({"t": e["block_time"], "wallet": e["owner"], "kind": e["kind"], "tokens_ui": t,
                           "sol": e["sol_lamports"] / LAMPORTS, "cum_sol_in": cum_in, "cum_sol_out": cum_out,
                           "tokens_held": tok, "mark_value_sol": tok * p if p else None})
        sold = sum(deep[w]["tokens_sold"] for w in members)
        remaining = sum((deep[w]["balance_now_ui"] or 0) for w in members)
        spot = (pool or {}).get("spot_price_sol")
        cf = self.facts.get("creator_fees", {})
        cr = deep.get(self.creator, {})
        h = {
            "LABEL": "HYPOTHÈSE — non démontrée on-chain",
            "members": members,
            "pct_supply_snapshot": sum(r["pct_supply"] for r in self.facts["snapshot"]["top20"][:10] if r["owner"] in members),
            "sol_injected": cum_in, "sol_recovered": cum_out, "tokens_sold": sold,
            "avg_sell_price_sol": cum_out / sold if sold else None,
            "tokens_remaining": remaining,
            "remaining_spot_value_sol": remaining * spot if spot else None,
            "remaining_liquidation_value_sol": self.liquidation_value(remaining, pool, fee_bps),
            "realized_pnl_sol": cum_out - cum_in,
            "creator_wallet": {k: cr.get(k) for k in ("sol_invested", "sol_recovered", "realized_pnl_sol", "balance_now_ui")},
            "creator_fees_accrued_sol": cf.get("accrued_total_sol"),
            "creator_fees_claimed_sol": cf.get("claimed_total_sol"),
            "series": series,
        }
        tot_in = h["sol_injected"] + (cr.get("sol_invested") or 0) + (self.facts["creation"].get("launch_cost_sol") or 0)
        tot_cash = h["sol_recovered"] + (cr.get("sol_recovered") or 0)
        h["total"] = {
            "sol_out_of_pocket": tot_in,
            "sol_cash_recovered_from_sales": tot_cash,
            "creator_fees_sol": cf.get("accrued_total_sol"),
            "realized_incl_fees_sol": tot_cash - tot_in + (cf.get("accrued_total_sol") or 0),
            "tokens_remaining_incl_creator": remaining + (cr.get("balance_now_ui") or 0),
        }
        self.facts["hypothesis_top10_is_creator"] = h

    # ------------------------------------------------------------------ run
    def run(self, fee_bps):
        print("1/9 supply", file=sys.stderr)
        self.supply()
        print("2/9 historique du mint", file=sys.stderr)
        self.load_mint_history()
        print("3/9 création", file=sys.stderr)
        self.creation()
        print("4/9 infra / graduation", file=sys.stderr)
        self.detect_infra()
        print("5/9 événements", file=sys.stderr)
        self.build_events()
        self.replay()
        self.early_buyers()
        print("6/9 wallets clés", file=sys.stderr)
        key = [self.creator] + self.snapshot_top + [r["owner"] for r in self.facts["early_buyers"][:20]]
        key += sorted((o for o in self.max_bal if o not in self.infra), key=lambda o: -self.max_bal[o])[:20]
        key = list(dict.fromkeys(key))
        deep = self.wallet_deep_dive(key)
        c = deep[self.creator]
        # Coût de lancement : variation SOL du créateur dans la tx de création, moins le dev buy
        cre = self.facts["creation"]
        dev_ev = next((e for e in c["events"] if e["signature"] == cre["signature"]), None)
        cre["launch_total_sol_delta"] = (cre["creator_sol_delta_lamports"] or 0) / LAMPORTS
        cre["dev_buy_sol"] = (-dev_ev["sol_lamports"] / LAMPORTS) if dev_ev else 0
        cre["dev_buy_tokens_ui"] = self.ui(dev_ev["token_raw"]) if dev_ev else 0
        cre["launch_cost_sol"] = None  # non séparable proprement : le dev buy et la création sont dans le même delta
        cre["creator_first_activity"] = c["first_activity"]
        cre["creator_first_funding"] = c["first_funding"]
        cre["creator_sol_before_creation_lamports"] = self._pre_balance(cre["signature"], self.creator)
        print("7/9 pool", file=sys.stderr)
        pool = self.pool_state()
        for w, d in deep.items():
            b = d["balance_now_ui"] or 0
            d["unrealized_spot_sol"] = b * pool["spot_price_sol"] if pool and pool.get("spot_price_sol") else None
            d["unrealized_liquidation_sol"] = self.liquidation_value(b, pool, fee_bps)
            d["relation"] = ("créateur" if w == self.creator else
                             "top10 snapshot" if w in self.snapshot_top else
                             "early buyer" if any(r["owner"] == w for r in self.facts["early_buyers"][:20]) else
                             "gros holder")
        print("8/9 creator fees", file=sys.stderr)
        self.creator_fees()
        print("9/9 liens + hypothèse", file=sys.stderr)
        self.links(deep)
        self.hypothesis(deep, pool, fee_bps)
        self.facts["wallets"] = deep
        self.dump()

    def _pre_balance(self, sig, acct):
        tx = self.txs[sig]
        keys = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"]]
        return tx["meta"]["preBalances"][keys.index(acct)] if acct in keys else None

    def dump(self):
        with open(os.path.join(self.out, "facts.json"), "w") as f:
            json.dump(self.facts, f, indent=1, default=str)
        with open(os.path.join(self.out, "events.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["block_time", "slot", "signature", "owner", "kind", "tokens_ui", "sol", "price_pool_sol",
                        "mcap_sol", "venues", "jito_tip"])
            for e in self.events:
                p = e["pool_price_lamports_per_raw"]
                ps = p * 10 ** self.decimals / LAMPORTS if p else None
                w.writerow([e["block_time"], e["slot"], e["signature"], e["owner"], e["kind"], self.ui(e["token_raw"]),
                            e["sol_lamports"] / LAMPORTS, ps, ps * self.supply_ui if ps else None,
                            "|".join(e["venues"]), e["jito_tip"]])
        print("écrit :", self.out, file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mint", default=JEANPHIL_MINT)
    ap.add_argument("--creator", default=None, help="défaut : créateur JEANPHIL si mint JEANPHIL, sinon signataire de la création")
    ap.add_argument("--out", required=True)
    ap.add_argument("--snapshot-min", type=float, default=38)
    ap.add_argument("--max-tx", type=int, default=None)
    ap.add_argument("--wallet-scan-limit", type=int, default=3000)
    ap.add_argument("--exclude", nargs="*", default=[], help="wallets à traiter comme infrastructure (ex. wallet communautaire/airdrop)")
    ap.add_argument("--pool-fee-bps", type=float, default=30, help="ESTIMATION des frais du pool pour la valeur de liquidation")
    a = ap.parse_args()
    creator = a.creator or (JEANPHIL_CREATOR if a.mint == JEANPHIL_MINT else None)
    rpc = Rpc(cache_dir=os.path.join(a.out, "cache"))
    Investigation(rpc, a.mint, creator, a.out, a.snapshot_min, a.max_tx, a.wallet_scan_limit, a.exclude).run(a.pool_fee_bps)


if __name__ == "__main__":
    main()
