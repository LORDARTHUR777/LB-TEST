# $JEANPHIL : état de l'investigation on-chain

Mint : `GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump` · Créateur déclaré : `BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B`
Rédigé le 2026-09-27.

## Ce qui a été vérifié, et ce qui ne l'a pas été

**Aucune donnée on-chain n'a pu être lue depuis l'environnement de travail.** Le proxy réseau bloque
toutes les sources de données brutes : RPC Solana, Helius, Solscan, Pump.fun, DexScreener, GeckoTerminal, Birdeye.
L'accès en lecture aux pages web de ces sites est bloqué lui aussi. Seul un moteur de recherche web a répondu.

Conséquences, pour respecter la règle « ne jamais inventer » :

- Ce rapport ne contient **aucune** adresse de holder, aucune signature de transaction et aucun montant de swap reconstitué par nous.
- Les chiffres ci-dessous viennent de **sources tierces lues dans des extraits de recherche**. Ils sont étiquetés
  `SOURCE TIERCE (non vérifiée)`. Leur horodatage est souvent imprécis.
- Les calculs faits à partir de ces chiffres sont étiquetés `ESTIMATION`.
- L'outil `onchain/` fait la reconstruction complète demandée, sections 1 à 13, dès qu'un RPC Solana est accessible
  (voir `README.md`). Il a été testé hors-ligne sur un scénario synthétique ; il n'a pas encore été exécuté sur les vraies données.

---

## 1. Données publiques recoupées (SOURCE TIERCE, non vérifiée)

| Donnée | Valeur | Date de référence | Source |
|---|---|---|---|
| Lancement | via Pump.fun, 20/09/2026 | — | résumé de recherche (KuCoin / bifu.co) |
| Supply | ≈ 969,5 M ; mint & freeze authority révoquées | — | bifu.co, KuCoin |
| Holders | 16,1 k en 24 h ; ≈ 17 623 plus tard | J+1 ; date inconnue | KuCoin, GeckoTerminal |
| Market cap / volume | 2,6 M$ ; volume 24 h 15,3 M$ | 21/09/2026 | CryptoRank / résumé |
| Market cap | 8,5 M$ | 25/09/2026 | Phantom / OpenSea |
| « En une semaine » | ≈ 8,8 M$ | ≈ 27/09/2026 | KuCoin (trends) |
| **ATH (prix)** | **0,01066 $** | **25/09/2026** | Coinbase / CoinCodex (résumé) |
| Pool PumpSwap | `4R8CiMnJWDNoes3fQi1ccPFJygPXazaHaWpHrN3rZeNj` | — | GeckoTerminal |
| État du pool (1 relevé) | prix 0,004966 $ ; FDV 4,97 M$ ; liquidité 318,52 k$ ; vol. 24 h 2,22 M$ ; 13 455 tx ; −46,8 % sur 24 h | date inconnue | GeckoTerminal |
| Tokens dans le pool | 31,92 M JEANPHIL ≈ 158 532,69 $ | date inconnue | résumé GeckoTerminal/Solscan |
| Liquidité « verrouillée » | 191,2 k$ | autre date | OneBullEx |
| Bundles | « 1,36 % des tokens achetés via bundled buys » | — | résumé (tracker non nommé) |
| Wallet créateur | libellé « JeanPhilMadame » ; le compte X @JeanPhilMadame a publié ce CA comme officiel | — | X, résumé |
| Homonymes | au moins un autre token « JEANPHIL » (autre CA) existe, effondré à ≈ 52 $ de MC | — | GeckoTerminal (résumé) |

**Cohérence de l'ATH (ESTIMATION)** : 0,01066 $ × 969,5 M ≈ **10,33 M$** de FDV. Cela concorde avec
l'ATH « autour de 10 M$ » de la première investigation. L'heure exacte de l'ATH reste à établir on-chain.

**Désaccord à conserver sur les bundles** : 1,36 % (« bundled buys ») contre ≈ 8 % (« sniper holdings »).
Les deux ne se contredisent pas forcément :

- un *bundle* est un ensemble d'achats dans une même transaction ou un même bundle Jito ;
- un *sniper* est un acheteur des N premiers blocs, lié ou non au créateur.

Les deux chiffres ont aussi pu être mesurés à des instants différents. L'outil calcule les deux définitions
séparément (sections 5 : `same_slot_groups`, `multi_receiver_buy_txs`, drapeau `jito_tip`).

## 2. Ce que les données publiques permettent déjà de chiffrer (ESTIMATION)

### Market cap ≠ argent encaissable : effet du slippage

Ce calcul utilise le relevé GeckoTerminal ci-dessus : pool ≈ 31,92 M tokens et ≈ 159 987 $ côté SOL
(318 520 − 158 533). On suppose une vente d'un seul bloc sur un pool x·y = k, avant frais du pool,
sans tenir compte des autres pools ni des acheteurs qui arrivent pendant la vente.

| Position vendue d'un bloc | Tokens | Valeur « spot » (prix × qté) | Cash réellement obtenu | Décote |
|---|---|---|---|---|
| Créateur (≈ 1,4 %) | 13,6 M | 67 545 $ | ≈ 47 799 $ | −29 % |
| « Sniper holdings » (≈ 8 %) | 77,6 M | 385 207 $ | ≈ 113 341 $ | −71 % |
| Top 10 du snapshot initial (28,9 %) | 280,2 M | 1 391 559 $ | ≈ 143 625 $ | −90 % |

Même dans l'hypothèse la plus défavorable où les 10 gros wallets appartiendraient au créateur, liquider ces
280 M tokens d'un coup à ce moment-là n'aurait rapporté qu'environ **0,14 M$**, et non 1,4 M$. Le P&L réel dépend
donc entièrement du **moment et du rythme des ventes**. Seule la reconstruction on-chain peut les donner.

### Creator fees : ordre de grandeur (analyse de sensibilité, pas une estimation)

Le barème Pump.fun / PumpSwap a changé plusieurs fois et, selon les périodes, dépend de la market cap.
Nous n'avons pas pu vérifier celui en vigueur le 20/09/2026. Le tableau suivant n'est donc qu'une grille de sensibilité,
avec des **taux illustratifs qui ne sont pas le barème officiel**.

| Volume cumulé | 0,05 % | 0,30 % | 0,95 % |
|---|---|---|---|
| 30 M$ | 15 k$ | 90 k$ | 285 k$ |
| 50 M$ | 25 k$ | 150 k$ | 475 k$ |

L'outil ne s'appuie sur aucun barème. Il **mesure** les SOL effectivement crédités au vault créateur dans
chaque trade de JEANPHIL, puis liste les transactions de claim.

## 3. Créateur : pourquoi « 0 % » puis « 13,6 M / 1,4 % » ?

Nous n'avons encore **aucun FAIT** sur ce point. Voici les hypothèses à départager, et la sortie de l'outil qui tranche chacune.

| Hypothèse | Signature on-chain attendue | Sortie de l'outil |
|---|---|---|
| H1 : achat tardif du créateur | événement `BUY` sur le wallet créateur après le snapshot initial | §7 « Chronologie des mouvements » |
| H2 : transfert depuis un autre wallet | `TRANSFER_IN` avec wallet source identifié | §7 `transfer_in_sources` + §9 lien `transfert_token` |
| H3 : dev buy vendu puis racheté | `SELL` puis `BUY` | §7 |
| H4 : écart d'affichage d'un tracker (mauvais wallet « dev », compte de tokens non-ATA, cache) | aucun mouvement ne correspond au passage de 0 à 13,6 M | §7 : solde rejoué contre le solde live |
| H5 : airdrop ou distribution entrante | `TRANSFER_IN` depuis un wallet de distribution | §7 / §9 |

## 4. Sections du livrable et état

| # | Section demandée | État | Produit par |
|---|---|---|---|
| 1 | Création : tx, heure, SOL avant, financement, coût, dev buy | outil prêt, **non exécuté** | `investigate.py` → `creation` |
| 2 | Premiers 10/20/50/100 acheteurs (+s, SOL, tokens, %, MC, payeur, Jito) | outil prêt | `early_buyers` |
| 3 | Adresses du top 10 à +38 min + P&L complet | outil prêt | `snapshot`, `wallets` |
| 4 | Liens créateur (funding commun, timing, transferts, profits) | outil prêt | `link_edges`, `clusters` |
| 5 | Bundles / snipers (nombre, tokens, %, SOL, timing) | outil prêt | `same_slot_groups`, `multi_receiver_buy_txs` |
| 6 | Swaps par wallet, tous DEX | outil prêt | `events.csv`, `wallets.*.events` |
| 7 | P&L réalisé / latent (spot et liquidation) | outil prêt | `wallets` |
| 8 | Wallet créateur (13,6 M) | outil prêt | §3 ci-dessus |
| 9 | Creator fees mesurées + claims | outil prêt | `creator_fees` |
| 10 | Timeline 24 h (MC, volume, holders) + ATH | outil prêt ; ATH ≈ 10,3 M$ (source tierce) | `timeline`, `ath_observed` |
| 11 | Graduation (tx, heure, liquidité, pool) | outil prêt | `graduation` |
| 12 | Hypothèse « 10 wallets = créateur » | outil prêt, étiquetée HYPOTHÈSE | `hypothesis_top10_is_creator` |
| 13 | Comparaison DAVID | outil prêt | `compare.py` |

## 5. $DAVID : ce qui est public (SOURCE TIERCE)

- Bon CA : `8wtdds5LPt7nu4jKifGpcxysF5AvJ1xCVti2rQ6Ppump`.
- Faux ou homonymes vus en recherche, **à exclure** : `G8atA3utCg9RyH8ztfKwvjDgKR9LwpUMhmnwwXyCpump`,
  `3pUZ9Wn7drrFXpHeL8gawoZnz2w4zTKSdt1AZBYspump`, `EwCvY771xFrWfor7qiCM7nm595uEKtoPAJuEAkGMpump`.
- Modèle annoncé (PumpList) : 50 % de la supply dans un wallet public, redistribués par airdrops quotidiens.

  Conséquence méthodologique : pour DAVID, le top 10 « brut » est dominé par ce wallet communautaire. La comparaison
  doit l'exclure (option `--exclude <adresse>`), sinon les métriques de concentration ne sont pas comparables.
- ATH ≈ 109 k$ (première investigation). En ordre de grandeur, l'ATH de JEANPHIL (≈ 10,3 M$) est **≈ 95×** celui de DAVID.
  Les volumes et les creator fees ne peuvent pas être comparés sans les données on-chain.

## 6. Réponse à la question finale (état actuel)

> *Sous l'hypothèse où les 10 wallets initiaux appartiennent au créateur, combien aurait-il mis de sa poche,
> encaissé en cash, gagné en creator fees, et combien lui resterait-il en tokens ?*

**Nous ne pouvons pas encore répondre avec des chiffres vérifiés.** Les montants investis, les ventes, les fees et
les soldes restants de ces wallets ne se lisent que on-chain, et cette lecture a été bloquée. Voici ce qui est établi
à ce stade (ESTIMATIONS) :

- Plafond du cash tiré d'une liquidation d'un seul bloc du top 10 au moment du relevé GeckoTerminal : **≈ 0,14 M$**,
  pas les ≈ 1,4 M$ de valeur « spot ». Des ventes étalées pendant la phase de montée (21–25/09) auraient pu rapporter
  bien plus. C'est précisément ce que la reconstruction mesurera.
- Creator fees : entre quelques dizaines et quelques centaines de milliers de dollars, selon le barème en vigueur
  (fourchette de sensibilité, §2). La mesure exacte se fera via les crédits au vault.

Pour obtenir la réponse chiffrée, donner à l'environnement l'accès à un RPC Solana, puis lancer les commandes du `README.md`.
Le rapport `RAPPORT_ONCHAIN.md` sera alors généré automatiquement, avec toutes les signatures cliquables.

## Sources

- [X — @JeanPhilMadame, CA officiel](https://x.com/JeanPhilMadame/status/2101759212283928877)
- [KuCoin — insight GTBx…pump](https://www.kucoin.com/news/insight/SOL/6ab7dc1074fd460007c587d5)
- [KuCoin — « Shadowboxing Frenchman becomes $8.8M memecoin in a week »](https://www.kucoin.com/news/trends/SOL/6ab764c674fd460007c57a66)
- [GeckoTerminal — pool JEANPHIL/SOL PumpSwap](https://www.geckoterminal.com/solana/pools/4R8CiMnJWDNoes3fQi1ccPFJygPXazaHaWpHrN3rZeNj)
- [bifu.co — What is Jean Phil](https://bifu.co/blog/what-is-jean-phil-jeanphil-the-viral-french-meme-coin-lighting-up-solana)
- [OneBullEx — analyse JEANPHIL](https://www.onebullex.com/explore/jean-phil-jeanphil-investment-analysis)
- [CryptoRank — Jean Phil](https://cryptorank.io/price/jean-phil)
- [Coinbase — Jean Phil](https://www.coinbase.com/price/jean-phil-solana-gtbxuiw6wjdmmkcgzgrhlyyxqu1vg4ktrpeox6ydpump-token)
- [Phantom — JEANPHIL](https://phantom.com/tokens/solana/GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump)
- [Pump.fun — page du token](https://pump.fun/coin/GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump)
- [PumpList — David Rothstein ($DAVID)](https://pumpfan.meme/project?id=cc29e8df-14cc-48af-a4f8-7860b3219000)
- [Solflare — homonyme David Rothstein (à exclure)](https://www.solflare.com/prices/david-rothstein/G8atA3utCg9RyH8ztfKwvjDgKR9LwpUMhmnwwXyCpump/)
