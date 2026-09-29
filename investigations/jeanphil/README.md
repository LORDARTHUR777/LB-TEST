# Investigation on-chain — $JEANPHIL

Mint analysé (et uniquement celui-ci) : `GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump`
Créateur déclaré : `BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B`
Comparaison : $DAVID `8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump`

- `RAPPORT.md` : rapport forensique complet, généré depuis les données on-chain.
- `onchain/` : outil de reconstruction forensique. Il lit les transactions via le RPC Solana et génère le rapport chiffré.

## Statut

La reconstruction a été exécutée le 29/09/2026 avec un RPC Helius. Le rapport qui en résulte est `RAPPORT.md`.
Les annexes `early_buyers.csv` et `wallets_pnl.csv` accompagnent le rapport. Les données brutes (`data/`,
plusieurs centaines de Mo) ne sont pas versionnées.

## Relancer

Prérequis : Python ≥ 3.10, `pip install solders`, et une clé Helius (l'offre gratuite suffit). L'outil utilise
la méthode Helius `getTransactionsForAddress`, qui lit l'historique dans l'ordre chronologique.

```bash
cd investigations/jeanphil/onchain
export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=VOTRE_CLE"

# 1. JEANPHIL : première heure complète + wallets clés
python3 fetch_window.py GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump 1789841756 1789845356 ../data/jeanphil/mint_0_60.jsonl
python3 market.py GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump 1789841756 ../data/jeanphil
python3 investigate.py --out ../data/jeanphil --jsonl ../data/jeanphil/mint_0_60.jsonl --window-min 60 \
    --exclude $(python3 -c "import json;print(' '.join(json.load(open('../data/jeanphil/market.json'))['pools']))")
python3 creator_trail.py ../data/jeanphil

# 2. DAVID : 9 premières minutes (le lancement a été très actif)
python3 market.py 8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump 1785615803 ../data/david
python3 investigate.py --mint 8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump --out ../data/david \
    --window-min 9 --snapshot-min 5 --exclude 5GNm6anmF9cFvhiSWrKLuSMTQJxvMex1KLvno9bBqZok

# 3. Rapport
python3 build_report.py ../data/jeanphil ../data/david > ../RAPPORT.md
python3 -m unittest discover -s tests -v
```

## Méthode

1. **Swaps.** Chaque transaction est lue par variations de soldes (lamports natifs + WSOL + token) propriétaire
   par propriétaire. Il n'y a pas de décodage propre à chaque DEX, donc Pump.fun, PumpSwap, Jupiter, Meteora,
   Raydium, bundles et bots sont tous couverts. Le prix et la market cap viennent du côté pool (bonding curve
   ou pool PumpSwap), hors frais du trader.
2. **Classification.** `BUY`, `SELL`, `TRANSFER_IN`, `TRANSFER_OUT`, et `BUY_PAID_BY_OTHER` (tokens reçus
   dans un swap payé par un autre wallet, signature typique d'un bundle multi-wallets).
3. **Snapshot.** Les soldes sont rejoués jusqu'à T+38 min, bonding curve et pools exclus.
4. **Wallets clés.** Créateur, top 10 du snapshot, 20 premiers acheteurs et 20 plus gros soldes max.
   L'historique complet de chacun est lu : financement initial, transferts du token hors DEX, destination des SOL après les ventes.
5. **Liens.** Chaque arête garde sa preuve :
   - FAIT : transfert direct SOL ou token entre deux wallets, achat payé par un autre.
   - INDICE fort : funder commun, destination commune des profits.
   - INDICE faible : même slot.
   Les funders ayant financé ≥ 40 wallets (CEX, services) sont exclus. Seuls les liens FAIT / INDICE fort forment des clusters.
6. **Creator fees.** Deux mesures, sans barème supposé :
   - les SOL reçus par le créateur lors des claims, plus le solde non réclamé des vaults (PDA Pump.fun
     `creator-vault` et PumpSwap `creator_vault`) ;
   - en contrôle, les crédits aux vaults trade par trade sur la fenêtre complète.
7. **P&L.** Réalisé = SOL récupérés − SOL investis (flux réels, frais réseau inclus). Certains swaps n'ont pas de
   SOL côté wallet (paiement en USDC, routeur) : ils sont valorisés au prix d'exécution du pool (ESTIMATION). Le latent est donné deux fois :
   valeur spot, et valeur de liquidation avec slippage x·y=k sur les réserves actuelles du pool.
8. **Hypothèse top 10 = créateur.** Calcul séparé, étiqueté HYPOTHÈSE. Les transferts internes au groupe sont neutralisés.
