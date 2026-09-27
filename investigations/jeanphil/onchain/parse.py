"""Extraction d'événements (achat / vente / transfert) à partir d'une transaction
Solana `jsonParsed`.

Principe : on ne décode pas les instructions de chaque DEX. On lit les
variations de soldes (pre/post) — lamports natifs + comptes SPL — par
propriétaire. C'est indépendant du DEX (Pump.fun, PumpSwap, Jupiter, Meteora,
Raydium, bots, bundles) et c'est exactement ce qui est sorti/entré dans la
poche de chaque wallet.
"""
from collections import defaultdict

WSOL = "So11111111111111111111111111111111111111112"
LAMPORTS = 1_000_000_000

PROGRAMS = {
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P": "pumpfun",
    "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA": "pumpswap",
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4": "jupiter",
    "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo": "meteora_dlmm",
    "Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB": "meteora_damm",
    "cpamdpZCGKUy5JxQXB4dcpGPiikHawvSWAd6mEn1sGG": "meteora_damm_v2",
    "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8": "raydium_amm",
    "CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C": "raydium_cpmm",
    "CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK": "raydium_clmm",
    "whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc": "orca",
    "Jito4APyf642JPZPx3hGc6WWJ8zPKtRbRs4P815Awbb": "jito_tip_router",
}
# Comptes de tip Jito : un tip dans la même tx est un indice fort de bundle.
JITO_TIP_ACCOUNTS = {
    "96gYZGLnJYVFmbjzopPSU6QiEV5fGqZNyN9nmNhvrZU5", "HFqU5x63VTqvQss8hp11i4wVV8bD44PvwucfZ2bU7gRe",
    "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLvLkY", "ADaUMid9yfUytqMBgopwjb2DTLSokTSzL1zt6iGPaS49",
    "DfXygSm4jCyNCybVYYK6DwvWqjKee8pbDmJGcLWNDXjh", "ADuUkR4vqLUMWXxW9gh6D6L8pMSawimctcNZ5pGwDcEt",
    "DttWaMuVvTiduZRnguLF7jNxTgiMBZ1hyAumKUiL2KRL", "3AVi9Tg9Uo68tJfuvoKvqKNWKkC5wPdSSdeBnizKZ6jT",
}


def _keys(tx):
    keys = tx["transaction"]["message"]["accountKeys"]
    return [k["pubkey"] if isinstance(k, dict) else k for k in keys], [
        bool(k.get("signer")) if isinstance(k, dict) else False for k in keys
    ]


def _programs(tx):
    ids = set()
    for ix in tx["transaction"]["message"].get("instructions", []):
        if ix.get("programId"):
            ids.add(ix["programId"])
    for inner in (tx.get("meta") or {}).get("innerInstructions") or []:
        for ix in inner.get("instructions", []):
            if ix.get("programId"):
                ids.add(ix["programId"])
    return ids


def instruction_names(tx):
    names = []
    for line in (tx.get("meta") or {}).get("logMessages") or []:
        if line.startswith("Program log: Instruction: "):
            names.append(line.split("Instruction: ", 1)[1].strip())
    return names


def token_deltas(tx, mint):
    """{owner: delta_en_unités_brutes} pour un mint donné, plus les décimales."""
    meta = tx.get("meta") or {}
    pre, post = defaultdict(int), defaultdict(int)
    decimals = None
    for bal, bucket in ((meta.get("preTokenBalances") or [], pre), (meta.get("postTokenBalances") or [], post)):
        for b in bal:
            if b.get("mint") != mint:
                continue
            decimals = b["uiTokenAmount"]["decimals"]
            bucket[(b.get("owner"), b["accountIndex"])] += int(b["uiTokenAmount"]["amount"])
    by_owner = defaultdict(int)
    for k in set(pre) | set(post):
        by_owner[k[0]] += post[k] - pre[k]
    return {o: d for o, d in by_owner.items() if d != 0}, decimals


def native_deltas(tx):
    meta = tx.get("meta") or {}
    keys, _ = _keys(tx)
    pre, post = meta.get("preBalances") or [], meta.get("postBalances") or []
    return {keys[i]: post[i] - pre[i] for i in range(min(len(keys), len(pre), len(post))) if post[i] != pre[i]}


def sol_deltas_by_owner(tx):
    """Lamports natifs + WSOL détenu en compte SPL, agrégés par propriétaire."""
    out = defaultdict(int)
    for acct, d in native_deltas(tx).items():
        out[acct] += d
    wsol, _ = token_deltas(tx, WSOL)
    for owner, d in wsol.items():
        out[owner] += d
    return out


def parse_tx(tx, mint, infra=frozenset(), dust_lamports=5_000):
    """Retourne une liste d'événements pour chaque propriétaire dont le solde
    du token cible a bougé, avec la contrepartie SOL correspondante.

    infra : propriétaires "techniques" (bonding curve, pools) — on calcule le
    prix d'exécution côté pool à partir d'eux, et ils ne sont pas traités
    comme des traders.
    """
    if tx is None or (tx.get("meta") or {}).get("err") is not None:
        return []
    keys, signers = _keys(tx)
    signer_set = {k for k, s in zip(keys, signers) if s}
    fee_payer = keys[0]
    fee = (tx.get("meta") or {}).get("fee", 0)
    tok, decimals = token_deltas(tx, mint)
    if not tok:
        return []
    sol = sol_deltas_by_owner(tx)
    progs = _programs(tx)
    venues = sorted({PROGRAMS[p] for p in progs if p in PROGRAMS})
    names = instruction_names(tx)
    jito = any(k in JITO_TIP_ACCOUNTS for k in keys)

    # Prix côté pool (hors frais du trader) si une infra a bougé.
    pool_price = None
    for o in infra:
        # Un swap = token et SOL varient en sens opposé côté pool. Création
        # (mint vers la curve) et migration (tout sort / tout entre) sont exclues.
        if o in tok and sol.get(o) and (tok[o] > 0) != (sol[o] > 0):
            pool_price = abs(sol[o]) / abs(tok[o])  # lamports par unité brute
            break

    # Qui a payé en SOL ? (hors infra), utile pour achats payés par un tiers.
    sol_payers = {a: d for a, d in sol.items() if d < -dust_lamports and a not in infra}

    events = []
    for owner, dtok in tok.items():
        if owner in infra:
            continue
        dsol = sol.get(owner, 0)
        dsol_ex_fee = dsol + (fee if owner == fee_payer else 0)
        if dtok > 0 and dsol_ex_fee < -dust_lamports:
            kind = "BUY"
        elif dtok < 0 and dsol_ex_fee > dust_lamports:
            kind = "SELL"
        elif dtok > 0:
            kind = "BUY_PAID_BY_OTHER" if (sol_payers and any(k in venues for k in ("pumpfun", "pumpswap", "jupiter"))
                                           and any(n.lower().startswith("buy") or "swap" in n.lower() for n in names)) else "TRANSFER_IN"
        else:
            kind = "TRANSFER_OUT"
        counterparties = [o for o, d in tok.items() if o != owner and (d > 0) != (dtok > 0)]
        events.append({
            "signature": tx["transaction"]["signatures"][0],
            "slot": tx.get("slot"),
            "block_time": tx.get("blockTime"),
            "owner": owner,
            "kind": kind,
            "token_raw": dtok,
            "decimals": decimals,
            "sol_lamports": dsol,               # flux réel (frais réseau inclus si payeur)
            "sol_lamports_ex_fee": dsol_ex_fee,
            "is_signer": owner in signer_set,
            "fee_payer": fee_payer,
            "signers": sorted(signer_set),
            "sol_payers": sol_payers,
            "counterparties": counterparties,
            "venues": venues,
            "instructions": names,
            "jito_tip": jito,
            "pool_price_lamports_per_raw": pool_price,
        })
    return events


def sol_transfers(tx, dust_lamports=1_000_000):
    """Transferts SOL (natif) d'une tx : liste (source, destination, lamports)
    à partir des instructions system.transfer parsées (y compris internes)."""
    out = []
    if tx is None or (tx.get("meta") or {}).get("err") is not None:
        return out
    ixs = list(tx["transaction"]["message"].get("instructions", []))
    for inner in (tx.get("meta") or {}).get("innerInstructions") or []:
        ixs.extend(inner.get("instructions", []))
    for ix in ixs:
        p = ix.get("parsed")
        if not isinstance(p, dict) or ix.get("program") != "system":
            continue
        if p.get("type") in ("transfer", "transferWithSeed"):
            info = p["info"]
            lam = int(info.get("lamports", 0))
            if lam >= dust_lamports:
                out.append((info.get("source"), info.get("destination"), lam))
        elif p.get("type") == "createAccount":
            pass
    return out
