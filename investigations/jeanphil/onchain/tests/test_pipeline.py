"""Test hors-ligne : un faux RPC sert des transactions synthétiques pour
vérifier toute la chaîne parse → investigate → report sans réseau.

  python3 -m unittest discover -s tests -v
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from solders.keypair import Keypair  # noqa: E402
from solders.pubkey import Pubkey  # noqa: E402

import investigate  # noqa: E402
import report  # noqa: E402
from parse import WSOL, parse_tx  # noqa: E402

DEC = 6
U = 10 ** DEC
SOL = 1_000_000_000


def k():
    return str(Keypair().pubkey())


MINT, CREATOR, A, B, C, D, FUNDER, PROFIT = (k() for _ in range(8))
BC = investigate.pda([b"bonding-curve", bytes(Pubkey.from_string(MINT))], investigate.PUMP)
VAULT = investigate.pda([b"creator-vault", bytes(Pubkey.from_string(CREATOR))], investigate.PUMP)
POOL = k()


class Builder:
    """Construit une tx jsonParsed à partir de variations de soldes."""

    def __init__(self):
        self.txs, self.n = {}, 0

    def tx(self, slot, t, signers, native, tokens, names=(), programs=(), transfers=(), wsol=None):
        self.n += 1
        sig = f"SIG{self.n:04d}" + "x" * 40
        accts = list(dict.fromkeys(list(signers) + list(native) + list(tokens) + list(wsol or {}) +
                                   [s for s, _, _ in transfers] + [d for _, d, _ in transfers]))
        keys = [{"pubkey": a, "signer": a in signers, "writable": True} for a in accts]
        pre = [10 * SOL] * len(accts)
        post = [pre[i] + native.get(a, 0) for i, a in enumerate(accts)]
        ptb, qtb = [], []
        for i, (owner, d) in enumerate(tokens.items()):
            base = 500_000_000 * U
            ptb.append({"accountIndex": 100 + i, "mint": MINT, "owner": owner, "uiTokenAmount": {"amount": str(base), "decimals": DEC}})
            qtb.append({"accountIndex": 100 + i, "mint": MINT, "owner": owner, "uiTokenAmount": {"amount": str(base + d), "decimals": DEC}})
        for i, (owner, d) in enumerate((wsol or {}).items()):
            base = 1000 * SOL
            ptb.append({"accountIndex": 200 + i, "mint": WSOL, "owner": owner, "uiTokenAmount": {"amount": str(base), "decimals": 9}})
            qtb.append({"accountIndex": 200 + i, "mint": WSOL, "owner": owner, "uiTokenAmount": {"amount": str(base + d), "decimals": 9}})
        ixs = [{"programId": p} for p in programs]
        ixs += [{"program": "system", "programId": "11111111111111111111111111111111",
                 "parsed": {"type": "transfer", "info": {"source": s, "destination": d, "lamports": l}}} for s, d, l in transfers]
        self.txs[sig] = {
            "slot": slot, "blockTime": t,
            "transaction": {"signatures": [sig], "message": {"accountKeys": keys, "instructions": ixs}},
            "meta": {"err": None, "fee": 5000, "preBalances": pre, "postBalances": post,
                     "preTokenBalances": ptb, "postTokenBalances": qtb, "innerInstructions": [],
                     "logMessages": [f"Program log: Instruction: {n}" for n in names]},
        }
        return sig


class FakeRpc:
    def __init__(self, b, supply_raw):
        self.b, self.supply_raw = b, supply_raw

    def _involving(self, addr):
        out = []
        for s, tx in self.b.txs.items():
            keys = {x["pubkey"] for x in tx["transaction"]["message"]["accountKeys"]}
            owners = {x["owner"] for x in tx["meta"]["postTokenBalances"]}
            mints = {x["mint"] for x in tx["meta"]["postTokenBalances"]}
            if addr in keys or addr in owners or addr in mints:
                out.append({"signature": s, "slot": tx["slot"], "blockTime": tx["blockTime"], "err": None})
        return sorted(out, key=lambda x: -x["slot"])

    def signatures(self, address, until_time=None, since_time=None, limit_total=None):
        return self._involving(address)[:limit_total]

    def tx(self, s):
        return self.b.txs.get(s)

    def txs_for_address(self, address, start=None, end=None, order="asc", limit_total=None, token_accounts=False):
        sigs = sorted(self._involving(address), key=lambda x: x["slot"], reverse=(order == "desc"))
        out = [self.b.txs[s["signature"]] for s in sigs
               if (start is None or s["blockTime"] >= start) and (end is None or s["blockTime"] <= end)]
        return out[:limit_total] if limit_total else out

    def account_info(self, address):
        return {"value": {"owner": "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"}}

    def balance(self, address):
        return {"value": 890_880 + (int(0.2 * SOL) if address == VAULT else 0)}

    def token_supply(self, mint):
        return {"value": {"amount": str(self.supply_raw), "decimals": DEC}}

    def token_accounts_by_owner(self, owner, mint):
        bal = 0
        if mint == WSOL:
            bal = 80 * SOL if owner == POOL else 0
        else:
            for tx in self.b.txs.values():
                for pre, post in zip(tx["meta"]["preTokenBalances"], tx["meta"]["postTokenBalances"]):
                    if post["owner"] == owner and post["mint"] == MINT:
                        bal += int(post["uiTokenAmount"]["amount"]) - int(pre["uiTokenAmount"]["amount"])
            if owner == POOL:
                bal = 200_000_000 * U
        return {"value": [{"pubkey": owner, "account": {"data": {"parsed": {"info": {"tokenAmount": {"amount": str(max(bal, 0))}}}}}}]}


def scenario():
    b = Builder()
    T0 = 1_790_000_000
    P = [investigate.PUMP]
    # financement du créateur et de A, B par le même FUNDER (non hub)
    b.tx(90, T0 - 3600, [FUNDER], {FUNDER: -5 * SOL, CREATOR: 5 * SOL}, {}, transfers=[(FUNDER, CREATOR, 5 * SOL)])
    b.tx(91, T0 - 3500, [FUNDER], {FUNDER: -3 * SOL, A: 3 * SOL}, {}, transfers=[(FUNDER, A, 3 * SOL)])
    b.tx(92, T0 - 3400, [FUNDER], {FUNDER: -3 * SOL, B: 3 * SOL}, {}, transfers=[(FUNDER, B, 3 * SOL)])
    # création + dev buy (créateur reçoit 10M)
    b.tx(100, T0, [CREATOR], {CREATOR: -int(0.3 * SOL), BC: int(0.28 * SOL), VAULT: 1_000_000},
         {BC: 990_000_000 * U, CREATOR: 10_000_000 * U}, names=["Create", "Buy"], programs=P)
    # A et B achètent dans le même slot
    for i, w in enumerate((A, B)):
        b.tx(100, T0 + 1, [w], {w: -2 * SOL, BC: int(1.98 * SOL), VAULT: 2_000_000},
             {BC: -40_000_000 * U, w: 40_000_000 * U}, names=["Buy"], programs=P)
    # bundle strict : C paie pour C et D
    b.tx(101, T0 + 2, [C], {C: -4 * SOL, BC: int(3.96 * SOL), VAULT: 4_000_000},
         {BC: -60_000_000 * U, C: 30_000_000 * U, D: 30_000_000 * U}, names=["Buy", "Buy"], programs=P)
    # A transfère au créateur 5M (explique un créateur "à 0" puis à 1,4 %)
    b.tx(150, T0 + 3000, [A], {}, {A: -5_000_000 * U, CREATOR: 5_000_000 * U}, names=["TransferChecked"])
    # migration
    b.tx(200, T0 + 3600, [k()], {BC: -80 * SOL, POOL: 0}, {BC: -800_000_000 * U, POOL: 800_000_000 * U},
         names=["Migrate"], programs=P, wsol={POOL: 80 * SOL})
    # ventes PumpSwap : A et B vendent, envoient les profits à PROFIT
    for w in (A, B):
        b.tx(300, T0 + 7200, [w], {w: 6 * SOL}, {w: -30_000_000 * U, POOL: 30_000_000 * U},
             names=["Sell"], programs=[investigate.PUMPSWAP], wsol={POOL: -6 * SOL})
        b.tx(301, T0 + 7300, [w], {w: -5 * SOL, PROFIT: 5 * SOL}, {}, transfers=[(w, PROFIT, 5 * SOL)])
    # claim des creator fees
    b.tx(400, T0 + 9000, [CREATOR], {CREATOR: int(0.5 * SOL), VAULT: -int(0.5 * SOL)}, {},
         names=["CollectCreatorFee"], programs=P)
    return b, T0


class PipelineTest(unittest.TestCase):
    def test_parse_classification(self):
        b, _ = scenario()
        kinds = {}
        for s, tx in b.txs.items():
            for e in parse_tx(tx, MINT, frozenset({BC, POOL})):
                kinds.setdefault(e["owner"], []).append(e["kind"])
        self.assertEqual(kinds[CREATOR], ["BUY", "TRANSFER_IN"])
        self.assertEqual(kinds[A], ["BUY", "TRANSFER_OUT", "SELL"])
        self.assertIn("BUY_PAID_BY_OTHER", kinds[D])

    def test_full_run_and_report(self):
        b, T0 = scenario()
        with tempfile.TemporaryDirectory() as out:
            inv = investigate.Investigation(FakeRpc(b, 1_000_000_000 * U), MINT, CREATOR, out, snapshot_min=38)
            inv.run(fee_bps=30)
            with open(os.path.join(out, "facts.json")) as fh:
                F = json.load(fh)
            self.assertIsNone(F["timeline"][0]["mcap_sol"])  # la tx de création ne fixe pas de prix
            self.assertEqual(F["creation"]["block_time"], T0)
            self.assertAlmostEqual(F["creation"]["dev_buy_tokens_ui"], 10_000_000)
            self.assertEqual(F["graduation"]["pool_owner"], POOL)
            top = [r["owner"] for r in F["snapshot"]["top20"][:5]]
            self.assertEqual(set(top), {A, B, C, D, CREATOR})
            self.assertTrue(F["same_slot_groups"])
            self.assertEqual(len(F["multi_receiver_buy_txs"]), 1)
            wa = F["wallets"][A]
            self.assertAlmostEqual(wa["sol_invested"], 2)
            self.assertAlmostEqual(wa["sol_recovered"], 6)
            self.assertAlmostEqual(F["wallets"][CREATOR]["tokens_transferred_in"], 5_000_000)
            self.assertIn(A, F["wallets"][CREATOR]["transfer_in_sources"])
            self.assertGreater(F["creator_fees"]["accrued_total_sol"], 0)
            self.assertAlmostEqual(F["creator_fees"]["claimed_total_sol"], 0.5)
            types = {e["type"] for e in F["link_edges"]}
            self.assertIn("funder_commun", types)
            self.assertIn("destination_commune_profits", types)
            self.assertIn(A, F["creator_cluster"])
            h = F["hypothesis_top10_is_creator"]
            self.assertAlmostEqual(h["sol_recovered"], 12)
            buf = io.StringIO()
            sys.argv = ["report.py", "--data", out]
            with redirect_stdout(buf):
                report.main()
            self.assertIn("HYPOTHÈSE", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
