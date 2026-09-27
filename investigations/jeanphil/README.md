# Investigation on-chain — $JEANPHIL

Mint analysé (et uniquement celui-ci) : `GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump`
Créateur déclaré : `BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B`
Comparaison : $DAVID `8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump`

- `RAPPORT.md` : état actuel de l'investigation. Il sépare ce qui est vérifié de ce qui ne l'est pas.
- `onchain/` : outil de reconstruction forensique. Il lit les transactions via le RPC Solana et génère le rapport chiffré.

## Pourquoi l'outil n'a pas encore tourné

La politique réseau de l'environnement cloud où ce travail a été fait bloque ces hôtes (403 au niveau du proxy) :
`api.mainnet-beta.solana.com`, `mainnet.helius-rpc.com`, `solscan.io`, `pump.fun`,
`api.dexscreener.com`, `www.geckoterminal.com`, `public-api.birdeye.so`, `api.binance.com`.
Seule la recherche web a fonctionné. `RAPPORT.md` ne contient donc aucun chiffre on-chain vérifié par nous.

## Lancer la reconstruction

Il faut Python ≥ 3.10, `pip install solders` (utilisé pour dériver les PDA Pump.fun) et un RPC Solana
avec historique complet. Un RPC gratuit Helius ou Triton convient ; le RPC public limite fortement le débit.

```bash
cd investigations/jeanphil/onchain
export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=VOTRE_CLE"

python3 investigate.py --out ../data/jeanphil            # JEANPHIL (créateur pré-rempli)
python3 investigate.py --mint 8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump --out ../data/david \
    --exclude <WALLET_COMMUNAUTAIRE_DAVID>                # à identifier : le wallet public 50 %

# Prix SOL/USD horaire (CSV "unix_time,price") : optionnel. Sans lui, tout reste en SOL.
python3 report.py --data ../data/jeanphil --sol-usd-csv sol_usd.csv > ../RAPPORT_ONCHAIN.md
python3 compare.py ../data/jeanphil ../data/david >> ../RAPPORT_ONCHAIN.md

python3 -m unittest discover -s tests -v                 # test hors-ligne (faux RPC)
```

Le cache disque (`data/*/cache`) garde chaque transaction déjà lue, donc une relance ne re-télécharge rien.
Options utiles :

- `--snapshot-min 38` : instant du snapshot du top 10.
- `--max-tx N` : borne le nombre de transactions du mint analysées.
- `--wallet-scan-limit` : profondeur d'historique par wallet.
- `--pool-fee-bps` : frais du pool pour la valeur de liquidation. C'est une ESTIMATION, à vérifier.

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
6. **Creator fees.** Somme des crédits aux vaults créateur (PDA Pump.fun `creator-vault` et PumpSwap
   `creator_vault`) dans les trades de ce mint. C'est la mesure réelle, sans barème supposé. Les claims signés
   par le créateur sont listés à part : le vault Pump.fun est commun à tous les tokens d'un même créateur.
7. **P&L.** Réalisé = SOL récupérés − SOL investis (flux réels, frais réseau inclus). Le latent est donné deux fois :
   valeur spot, et valeur de liquidation avec slippage x·y=k sur les réserves actuelles du pool.
8. **Hypothèse top 10 = créateur.** Calcul séparé, étiqueté HYPOTHÈSE. Les transferts internes au groupe sont neutralisés.
