# $JEANPHIL — investigation forensique on-chain

Mint : `GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump` · Créateur : `BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B` · Rapport généré le 29/09/2026 13:13 UTC

**Légende.** **FAIT** = lu directement dans les transactions Solana (signature fournie). **INDICE** = élément compatible avec un lien, non probant seul. **HYPOTHÈSE** = supposition explicite. **ESTIMATION** = calcul dépendant d'une donnée externe (cours SOL/USD, chandeliers GeckoTerminal, valorisation au prix du pool).

**Sources.** RPC Solana Helius (transactions complètes, `getTransactionsForAddress`), GeckoTerminal (chandeliers, cours SOL/USD horaire du pool Raydium SOL/USDC), DexScreener (liste des pools), Helius DAS (holders actuels). Toutes les signatures sont cliquables (Solscan).

**Conventions.** Les % de supply sont calculés sur la supply initiale de 1 000 000 000 (base des trackers au lancement ; supply actuelle 969 485 803 après burns). Les montants en $ sont convertis au cours SOL/USD de l'heure de chaque transaction (ESTIMATION). La market cap n'est jamais de l'argent encaissable.

## Réponse courte

| | Créateur officiel (FAIT) | Top 10 du snapshot +38 min (HYPOTHÈSE « même personne ») | Total hypothétique |
|---|---|---|---|
| Mis de sa poche | **0,401 SOL** (≈ 45 $) | 434,44 SOL (≈ 49 214 $) | 434,84 SOL (≈ 49 258 $) |
| Encaissé en ventes de tokens | **0 SOL** (n'a jamais vendu) | 1 584,45 SOL (≈ 176 872 $) | 1 584,45 SOL (≈ 176 872 $) |
| Creator fees réclamées | **1 850,96 SOL** (≈ 218 846 $) + 1,31 SOL non réclamés | — | 1 850,96 SOL |
| P&L réalisé | **1 850,56 SOL** (≈ 218 802 $) | 1 150,01 SOL (≈ 127 658 $) | 3 000,58 SOL (≈ 346 460 $) |
| Tokens restants | **13,63 M** (1,36 %) — spot 476,1 SOL, liquidation ≈ 343,4 SOL | 1,15 M — spot 40,2 SOL | 14,79 M |

**Lecture.** Le gain du créateur ne vient pas de la vente de tokens : il vient à ~100 % des **creator fees** générées par le volume. Dans l'hypothèse où les 10 gros wallets initiaux lui appartiendraient, les ventes de ces wallets ajouteraient un P&L réalisé du même ordre de grandeur que les fees — mais **aucun lien on-chain n'a été trouvé entre le créateur et ces wallets** (voir §6), et plusieurs d'entre eux appartiennent à des groupes distincts. L'hypothèse est donc présentée uniquement comme un calcul.

## Ce que le créateur a mis en place, dans l'ordre (réglages, coûts, référencement, gains)

### A. Réglages du memecoin (FAIT, lus sur le compte du mint)

| Réglage | Valeur | Ce que ça implique |
|---|---|---|
| Plateforme | Pump.fun (programme `6EF8…F6P`, instruction `CreateV2`) | lancement « fair launch » sur bonding curve, graduation automatique |
| Nom / ticker | Jean Phil / JEANPHIL | |
| Description | « Official Jean Phil, oui madame ! » | |
| Site déclaré dans les métadonnées | https://linktr.ee/JeanPhilanthrope | aucun X/Telegram dans les métadonnées on-chain |
| Image | IPFS `bafybeicswknzjbbpuuj…` | |
| Standard | Token-2022 (`Tokenz…`), 6 décimales, supply initiale 1 000 000 000 | |
| Mint authority | **désactivée** | impossible de créer de nouveaux tokens |
| Freeze authority | **désactivée** | impossible de geler un wallet |
| Update authority des métadonnées | **aucune** | nom/logo/lien non modifiables |
| Dev buy | 13,63 M (1,36 %) | seul achat du créateur, jamais revendu |
| Destinataire des creator fees | le créateur lui-même (vaults PDA dérivés de son adresse) | aucun partage de fees configuré par lui sur JEANPHIL |
| Contrôle Jupiter | mint/freeze désactivés : True/True ; dev = 1,41 % ; tokens créés par ce dev : 1 ; score organique 84/100 (high) ; tags ['unknown', 'token-2022'] | source : API Jupiter |

### B. Coût du lancement — où est parti chaque lamport (FAIT)

Transaction [`4wi3ZcYa…`](https://solscan.io/tx/4wi3ZcYaGunjZx7Z9JoA2fa1CNY9zMs5xSa4BNwUjJzfBG5NRHtHiMQ1CB1e4j4iQJ2BTzL3xLksdmbGjLEqLYNB), signée depuis le wallet créateur sur **pump.fun**. Total débité : **0,400988 SOL ≈ 45 $** (SOL ≈ 110,99 $).

| Destination | SOL | Nature (INDICE sauf mention) |
|---|---|---|
| [`9JGQ76…Xsg5`](https://solscan.io/account/9JGQ767qGY9ya2PpuXgDMiQL8YNYH3Jms2fyhrBPXsg5) | 0,387395 | bonding curve : paiement du dev buy + rente du compte (FAIT) |
| [`GTBxUi…pump`](https://solscan.io/account/GTBxUiw6wJdmmkCGZgRHLyYxqu1vG4KtRpeox6yDpump) | 0,002692 | rente du compte mint (dépôt récupérable seulement si fermé) |
| [`9rPYyA…hJUz`](https://solscan.io/account/9rPYyANsfQZw3DnDmKE3YCQF5E8oD89UXoHn9JFEhJUz) | 0,001834 | frais de protocole Pump.fun ou rente de comptes de tokens |
| [`5cjcW9…XUW6`](https://solscan.io/account/5cjcW9wExnJJiqgLjq7DEG75Pm6JBgE1hNv4B2vHXUW6) | 0,001834 | frais de protocole Pump.fun ou rente de comptes de tokens |
| [`D8W7WX…RWvR`](https://solscan.io/account/D8W7WXU3pNLdLeUQFt9t72Nsym9RxUWBfJbGBcybRWvR) | 0,001809 | creator fee du dev buy → son propre vault (lui revient, FAIT) |
| [`4q7y2V…Sk4B`](https://solscan.io/account/4q7y2VkJBAt1N61hKFdWZQhY512G1ymLYvPi9mjRSk4B) | 0,001514 | frais de protocole Pump.fun ou rente de comptes de tokens |
| [`AZhueJ…jPNy`](https://solscan.io/account/AZhueJotniE3WYy8PQmN3iuctzVmfZeEMcwDFVkXjPNy) | 0,001514 | frais de protocole Pump.fun ou rente de comptes de tokens |
| [`4kCMhn…PN4V`](https://solscan.io/account/4kCMhnW7rzFVYqftn7iG3WqwcgvfyvWyavd7CZTdPN4V) | 0,001346 | frais de protocole Pump.fun ou rente de comptes de tokens |
| [`pfnP85…b3bq`](https://solscan.io/account/pfnP85qobXv2wETniKjXBhxKvgivpfT8EGAcS8sb3bq) | 0,001000 | frais de protocole Pump.fun ou rente de comptes de tokens |
| frais réseau Solana | 0,000050 | FAIT |

Aucune autre dépense du wallet créateur n'apparaît on-chain : pas de paiement en SOL/USDC vers DexScreener, un market maker ou un service de bump/volume depuis ce wallet.

### C. Référencement du token, dans l'ordre

| Date (UTC) | Où | Comment | Coût / payeur | Source |
|---|---|---|---|---|
| 19/09/2026 18:15:56 | **Pump.fun** | création par le créateur | 0,401 SOL (ci-dessus) | FAIT on-chain |
| 19/09/2026 19:06:59 | **PumpSwap** (pool [`4R8CiM…ZeNj`](https://solscan.io/account/4R8CiMnJWDNoes3fQi1ccPFJygPXazaHaWpHrN3rZeNj)) | graduation automatique | 0 pour le créateur | FAIT on-chain |
| 19/09/2026 20:12:09 | Meteora (pool [`CzVhSw…MJTS`](https://solscan.io/account/CzVhSwrx9VQmBJTP2BdHgWiRPEcbWBNEAmPCPH1BMJTS)) | pool créé par un tiers | pas le créateur | DexScreener |
| 19/09/2026 20:25:41 | **DexScreener** — « tokenProfile » (approved) | profil enrichi : logo, bannière, liens twitter, tiktok, instagram | tarif public ≈ 299 $ (ESTIMATION) ; **payeur non identifié** — aucune sortie du wallet créateur ce jour-là | API DexScreener |
| 19/09/2026 20:44:31 | Meteora (pool [`CJab6R…LPh9`](https://solscan.io/account/CJab6RE2KNdhCLdY9sBxpijxpFegduaFg83UtEehLPh9)) | pool créé par un tiers | pas le créateur | DexScreener |
| 20/09/2026 02:42:24 | Meteora (pool [`5u7PMs…iANq`](https://solscan.io/account/5u7PMsDxbaALbV9viti9Y4pEBVJqWSSp69uEsXGtiANq)) | pool créé par un tiers | pas le créateur | DexScreener |
| 20/09/2026 13:34:58 | Meteora (pool [`5zPSHD…N82d`](https://solscan.io/account/5zPSHDVj5ZBY9WS5XFY4GqDU3pX7xycKY4Tgbu8kN82d)) | pool créé par un tiers | pas le créateur | DexScreener |
| 20/09/2026 15:34:55 | Raydium (pool [`j4qvNW…A1kG`](https://solscan.io/account/j4qvNWSZLPy18jSWfkCa5VbPnD9PqEGBC3LAjjzA1kG)) | pool créé par un tiers | pas le créateur | DexScreener |
| automatique | GeckoTerminal, Jupiter, Birdeye, Phantom… | indexation automatique des pools | 0 | APIs |
| — | CoinGecko | **non listé** (`coingecko_coin_id` = null) | — | API GeckoTerminal |
| après le 20/09 | Pages de prix / articles : Coinbase (page de prix), CryptoRank, CoinCodex, OpenSea, KuCoin News, Bitrue, KCEX, OneBullEx ; site d'airdrop jean-philanthrope.com | pages éditoriales ou agrégateurs — pas des listings d'exchange payés | n/d | SOURCE TIERCE (recherche web) |

Réseaux affichés sur le profil DexScreener : [twitter](https://x.com/JeanPhilMadame), [tiktok](https://www.tiktok.com/@jean_philanthrope), [instagram](https://www.instagram.com/jean_philanthrope/). Le compte X a publié le contrat comme « seul token officiel » (SOURCE TIERCE : post X).

### D. Toutes les actions signées par le créateur (FAIT)

| Date (UTC) | Action | SOL pour lui | Transaction |
|---|---|---|---|
| 19/09/2026 18:15:56 | Création du token + dev buy (pump.fun) | -0,4010 | [`4wi3ZcYa…`](https://solscan.io/tx/4wi3ZcYaGunjZx7Z9JoA2fa1CNY9zMs5xSa4BNwUjJzfBG5NRHtHiMQ1CB1e4j4iQJ2BTzL3xLksdmbGjLEqLYNB) |
| 22/09/2026 21:49:26 | Retrait (claim) des creator fees JEANPHIL | 1 360,7238 | [`24gJWiZe…`](https://solscan.io/tx/24gJWiZet5rfPh7EPJwor4i61nhXvcCscQD4SADQx75ro4MrXBrCSzks62HUzQocEr32KByckornskYu5UyVjjEP) |
| 22/09/2026 21:56:28 | Envoi de SOL vers [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) | -0,1000 | [`5jrdehEy…`](https://solscan.io/tx/5jrdehEyerH5Nay8q465qK77ScaaV48LV6JHXCx3TUgWkw1LnnD2hwKjRo8WNVfLvpYBMLxST7zFP5op1AxnNajd) |
| 22/09/2026 22:01:20 | Envoi de SOL vers [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) | -50,0000 | [`4dubGtQt…`](https://solscan.io/tx/4dubGtQtaM8vy8JjBJKkjUEbDEhzf2cx6yWd6iSMDC36WBQZqMbRMw5Toyy8Lzr6iLsisQFgmA9wp1tqECF3QF2b) |
| 22/09/2026 22:02:15 | Envoi de SOL vers [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) | -450,0000 | [`2Tq4G6xw…`](https://solscan.io/tx/2Tq4G6xwVvKP2wLBL2jmsbGV1fHjFuCLMvaudMRZ7V1ebfTyaHfo98Tt318ZN6mMs76LQWyBn23FYKntswYyfhYG) |
| 25/09/2026 09:31:55 | Envoi de SOL vers [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) | -500,0000 | [`2gndqhkk…`](https://solscan.io/tx/2gndqhkkfUeipTCVmeAvV6CPoyX2BXXq8suGopDZPfZmdqnbC5W2rCFdEf5ov5JdykA2w5Jh47rk4swZMGQmKhyB) |
| 28/09/2026 19:40:06 | Fermeture d'un compte de token reçu en airdrop (rente récupérée) | 0,0015 | [`2uYimtbw…`](https://solscan.io/tx/2uYimtbwiycwfvKPDpdCsiBn3kCqHiiYyk7JjTfd851sfRRYhV32uBCBrRsXC4q59AtsfncgCFLxzV1w19xzswWY) |
| 28/09/2026 19:40:06 | Retrait (claim) des creator fees JEANPHIL | 452,2444 | [`3qA9BaMu…`](https://solscan.io/tx/3qA9BaMutMeWjrcQ3aLRyqxNS1sAPWMT3jMUezs3YFHDciFtb72n27ghxpLtmN1ugsepJF5ckeinbkqXp6qtsPrT) |
| 28/09/2026 19:40:06 | 15 × `DistributeCreatorFees` : encaisse des parts de fees d'**autres** tokens qui l'ont désigné bénéficiaire | 3,7551 | — |
| 28/09/2026 19:43:55 | Envoi de SOL vers [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) | -425,0000 | [`4noB6XWv…`](https://solscan.io/tx/4noB6XWvDDwNfiurhQUKceZcYnvVswiDMna9fJwn9cKfY65UGo7CN3DomGySndANp4TgKqSA4HTvuLuir8nkCUBs) |
| 29/09/2026 12:09:48 | Claim déclenché par un tiers (instruction sans permission), fees versées au créateur | 37,9953 | [`f4XQt5wT…`](https://solscan.io/tx/f4XQt5wTbU7TALKNrAsmvZEg7zjgDcDoRe8Bhuwa6Tt5fK3yxgoZe5MhWcHyyS7emECg8LGN2EuF9pjjiid8Bny) |

Reçu passivement (non signé par lui) : 64 transactions d'airdrop d'autres memecoins et 2 configurations de partage de fees créées par des tiers sur d'autres tokens. Il n'a acheté ou vendu aucun autre token.

### E. Bilan financier du créateur (FAIT, $ = ESTIMATION)

| Poste | SOL | ≈ USD |
|---|---|---|
| Mis de sa poche (création + dev buy) | −0,401 | −45 $ |
| Ventes de JEANPHIL | 0 | 0 $ |
| Creator fees JEANPHIL réclamées | +1 850,96 | +218 846 $ |
| Creator fees non réclamées | +1,31 | +158 $ |
| Parts de fees d'autres tokens (`DistributeCreatorFees`) | +9,72 | ≈ +1 172 $ |
| **Gain réalisé** | **+1 860,28** | **≈ +219 974 $** |
| dont déjà sorti vers un service (exchange probable) | 1 425,10 | 168 768 $ |
| resté sur le wallet créateur | 435,62 | 52 532 $ |
| **Encore en tokens** (non vendus) | 13,63 M JEANPHIL | ≈ 57 417 $ au prix spot ; ≈ 41 415 $ si vendus d'un bloc (ESTIMATION) |

## 1. Timeline chronologique

| Date (UTC) | T+ | Événement | Détail |
|---|---|---|---|
| 19/09/2026 18:11:05 | −4 min 51 s | Financement du wallet créateur | 0,4369 SOL reçus de [`5F1seM…xUq1`](https://solscan.io/account/5F1seMKUqSNhv45f6FhB2cFmgJbk8U1avJw7M6TexUq1) ([`3fWaekeb…`](https://solscan.io/tx/3fWaekebgqb7xS8xyU1P1JV53VKQeXs3a5zR2uFWWimHBNBYqEunVc7idbAKXW939h6fzJrYtXEMRtrSru6wmEBJ)) — FAIT |
| 19/09/2026 18:15:56 | 0 s | Création + dev buy (même transaction) | 13,63 M JEANPHIL pour 0,4010 SOL ([`4wi3ZcYa…`](https://solscan.io/tx/4wi3ZcYaGunjZx7Z9JoA2fa1CNY9zMs5xSa4BNwUjJzfBG5NRHtHiMQ1CB1e4j4iQJ2BTzL3xLksdmbGjLEqLYNB)) — FAIT |
| 19/09/2026 18:15:59 | 3 s | Snipers | 2 wallets achètent dans les 5 s (6,41 % de la supply) — FAIT |
| 19/09/2026 18:30:56 | 15 min 00 s | Phase calme | market cap ≈ 35,4 SOL à +15 min ; les snipers ont revendu — FAIT |
| 19/09/2026 18:53:56 | 38 min 00 s | Snapshot +38 min | top 10 = 28,9 % de la supply — FAIT |
| 19/09/2026 19:06:59 | 51 min 03 s | Graduation → PumpSwap | +51 min 03 s ; pool [`4R8CiM…ZeNj`](https://solscan.io/account/4R8CiMnJWDNoes3fQi1ccPFJygPXazaHaWpHrN3rZeNj) ([`2pAfa2Cd…`](https://solscan.io/tx/2pAfa2CdK8SpJguaMjngHr8si1XjvyHMxUYr8PQ9738piJUL9T9ZaKXb1H1AoruNgQeLPuCqxiEG2w8QE2dXuneE)) — FAIT |
| 20/09/2026 17:02:00 | 22 h 46 | ATH (pool principal) | 0,01158 $ ≈ 11 580 066 $ de market cap — ESTIMATION GeckoTerminal |
| 22/09/2026 21:49:26 | 75 h 33 | Claim creator fees | 1 360,72 SOL ([`24gJWiZe…`](https://solscan.io/tx/24gJWiZet5rfPh7EPJwor4i61nhXvcCscQD4SADQx75ro4MrXBrCSzks62HUzQocEr32KByckornskYu5UyVjjEP)) — FAIT |
| 28/09/2026 19:40:06 | 217 h 24 | Claim creator fees | 452,24 SOL ([`3qA9BaMu…`](https://solscan.io/tx/3qA9BaMutMeWjrcQ3aLRyqxNS1sAPWMT3jMUezs3YFHDciFtb72n27ghxpLtmN1ugsepJF5ckeinbkqXp6qtsPrT)) — FAIT |
| 29/09/2026 12:09:48 | 233 h 53 | Claim creator fees | 38,00 SOL ([`f4XQt5wT…`](https://solscan.io/tx/f4XQt5wTbU7TALKNrAsmvZEg7zjgDcDoRe8Bhuwa6Tt5fK3yxgoZe5MhWcHyyS7emECg8LGN2EuF9pjjiid8Bny)) — FAIT |

## 2. Création du token (FAIT)

- **Transaction** : [`4wi3ZcYa…`](https://solscan.io/tx/4wi3ZcYaGunjZx7Z9JoA2fa1CNY9zMs5xSa4BNwUjJzfBG5NRHtHiMQ1CB1e4j4iQJ2BTzL3xLksdmbGjLEqLYNB) — slot 448485736 — **19/09/2026 18:15:56 UTC** — instructions `CreateV2, InitializeMint2, GetAccountDataSize … BuyV2`
- **Signataires** : [`BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B`](https://solscan.io/account/BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B) (créateur) et le mint lui-même
- **SOL sur le wallet avant création** : 0,436906 SOL
- **Première transaction du wallet** : [`3fWaekeb…`](https://solscan.io/tx/3fWaekebgqb7xS8xyU1P1JV53VKQeXs3a5zR2uFWWimHBNBYqEunVc7idbAKXW939h6fzJrYtXEMRtrSru6wmEBJ) le 19/09/2026 18:11:05 (4 min 51 s avant la création) : réception de 0,436906 SOL depuis [`5F1seMKUqSNhv45f6FhB2cFmgJbk8U1avJw7M6TexUq1`](https://solscan.io/account/5F1seMKUqSNhv45f6FhB2cFmgJbk8U1avJw7M6TexUq1)
  - INDICE : [`5F1seM…xUq1`](https://solscan.io/account/5F1seMKUqSNhv45f6FhB2cFmgJbk8U1avJw7M6TexUq1) présente un profil de wallet de service (très nombreux destinataires, >1 800 SOL de solde) — typique d'un retrait d'exchange. Aucun autre lien de financement n'a été trouvé.
- **Coût total du lancement** (création + dev buy + frais) : 0,400988 SOL (≈ 45 $)
- **Première acquisition** : dev buy de **13 634 393,23 JEANPHIL** (1,363 % de la supply) dans la transaction de création.

## 3. Premiers acheteurs (FAIT)

| Groupe | SOL dépensés | Tokens achetés (cumul) | % supply acheté | Dernier achat du groupe |
|---|---|---|---|---|
| 10 premiers | 7,21 | 202,15 M | 20,22 % | +11 s |
| 20 premiers | 15,91 | 424,87 M | 42,49 % | +10 min 27 s |
| 50 premiers | 27,28 | 645,12 M | 64,51 % | +10 min 38 s |
| 100 premiers | 43,96 | 1 013,84 M | 101,38 % | +13 min 39 s |

*« Cumul acheté » ≠ détention simultanée : beaucoup revendent en quelques minutes.*

| # | Wallet | T+ | Slot +n | SOL | Tokens | % supply | MC avant achat (SOL) | Jito | Lien connu |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [`BS3FxZ…dE3B`](https://solscan.io/account/BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B) | 0 s | 0 | 0,401 | 13,63 M | 1,36 % | n/d |  | créateur |
| 2 | [`BMkHjN…gXWJ`](https://solscan.io/account/BMkHjN2N8K2PdCqeC92YYjUovn9ecW4GvFpH6yDggXWJ) | 3 s | 14 | 1,078 | 35,08 M | 3,51 % | n/d |  | groupe 1 |
| 3 | [`2sapux…Dpz7`](https://solscan.io/account/2sapuxSmfbKAziDJKTwJWtqfZoukBLKX5zeBCVdPDpz7) | 3 s | 14 | 0,949 | 28,97 M | 2,90 % | n/d |  | groupe 1 |
| 4 | [`27xjYF…2QUG`](https://solscan.io/account/27xjYFf3pQuHTLnNogacXii3rKzEyjD5nWkFdjvs2QUG) | 9 s | 33 | 1,011 | 29,15 M | 2,91 % | 30,6 |  | groupe 1 |
| 5 | [`FeS5hu…T2q3`](https://solscan.io/account/FeS5huVYxZGEP4peg9bGiViSbesfCjyrD564s3ibT2q3) | 9 s | 33 | 1,016 | 27,60 M | 2,76 % | 30,6 |  | groupe 1 |
| 6 | [`985sqa…hVdZ`](https://solscan.io/account/985sqazousgFWXYTMnoLHBsdUfWJfHoCcPCYhkYBhVdZ) | 11 s | 44 | 0,515 | 13,43 M | 1,34 % | 34,4 |  | groupe 2 |
| 7 | [`7vZu6H…1uQP`](https://solscan.io/account/7vZu6HQakBZmvYjD2GWKLRcdm4vVtaS5qxxrY3bZ1uQP) | 11 s | 44 | 0,524 | 13,28 M | 1,33 % | 34,4 |  | groupe 2 |
| 8 | [`J2ztQn…2911`](https://solscan.io/account/J2ztQnZijWHQZeF18o6wvcKFttovvBoUjUvHPB4w2911) | 11 s | 44 | 0,487 | 11,99 M | 1,20 % | 34,4 |  | groupe 2 |
| 9 | [`2WAezA…GouL`](https://solscan.io/account/2WAezAawFNVUttsXdy4GTymV9aEMvM7fpGq1ZFHuGouL) | 11 s | 44 | 0,497 | 11,92 M | 1,19 % | 34,4 |  | groupe 2 |
| 10 | [`ojiyUR…pk67`](https://solscan.io/account/ojiyURrcv3kvTaqdFN1gPYQ56GeyQbR6z9iN3JCpk67) | 11 s | 44 | 0,732 | 17,08 M | 1,71 % | 34,4 |  | groupe 1 |
| 11 | [`Gsjt6k…NPqB`](https://solscan.io/account/Gsjt6kLdidphL7FbzZyS4W1WohqEQoLoZa3h9782NPqB) | 12 s | 47 | 0,209 | 4,58 M | 0,46 % | 40,4 |  | groupe 1 |
| 12 | [`5FihbC…uks4`](https://solscan.io/account/5FihbCbCqXdz6yHcVWyyJbn1G2cpoarJ38RyAGFquks4) | 15 s | 58 | 0,053 | 1,19 M | 0,12 % | 40,8 |  | groupe 1 |
| 13 | [`H3dMhU…d4Fw`](https://solscan.io/account/H3dMhUXA153HdEVkG9KLURpBQwpwvQdt4B6nEvgod4Fw) | 27 s | 103 | 0,009 | 0,22 M | 0,02 % | 40,0 |  |  |
| 14 | [`Hh2yn3…2PzL`](https://solscan.io/account/Hh2yn37jiXuwCM4nkvAZPbc8CjL6j32Ho38giC1y2PzL) | 79 s | 298 | 0,453 | 9,47 M | 0,95 % | 43,8 |  | groupe 1 |
| 15 | [`FSz6mp…4BZX`](https://solscan.io/account/FSz6mptAxKrjDjaJYQiGiCGGwsxL4WgWjsh9sGhw4BZX) | 79 s | 298 | 0,303 | 6,18 M | 0,62 % | 43,8 |  | groupe 1 |
| 16 | [`CiueJw…urDC`](https://solscan.io/account/CiueJwuBw1cZVz4YzY4TpPtyaEQJEpmYZmxkLAuXurDC) | 79 s | 298 | 1,003 | 19,94 M | 1,99 % | 43,8 |  | groupe 1 |
| 17 | [`4WxE3G…dzhP`](https://solscan.io/account/4WxE3GAiFG6EofdSF4N3DWXg5na9V3BQJJN5LuE5dzhP) | 79 s | 299 | 1,503 | 28,15 M | 2,81 % | 43,8 |  | groupe 1 |
| 18 | [`CKB1XY…uN5d`](https://solscan.io/account/CKB1XYgbEmfEE3FJev7gFwEVtoqEvmsX6GhnbuFvuN5d) | 627 s | 2347 | 2,660 | 85,27 M | 8,53 % | 28,6 |  | groupe 1 |
| 19 | [`HGxBHp…G9AV`](https://solscan.io/account/HGxBHpUsFbN9Mnf78pCNBMkYnYdEQqcensEiBvX3G9AV) | 627 s | 2347 | 1,009 | 28,27 M | 2,83 % | 28,6 |  | groupe 1 |
| 20 | [`5e8DjV…EA5W`](https://solscan.io/account/5e8DjVTq2NxESfa3RtMeGyhifiDyuwo4zmRHj8JNEA5W) | 627 s | 2348 | 1,503 | 39,45 M | 3,95 % | 28,6 |  | groupe 1 |
| 21 | [`AmwJTo…Bf89`](https://solscan.io/account/AmwJToZR4YkawNquDbiUHbZnC2Myq1CLRRryUQ9FBf89) | 627 s | 2348 | 0,368 | 9,12 M | 0,91 % | 28,6 |  |  |
| 22 | [`4wbrLx…gpVq`](https://solscan.io/account/4wbrLxXe4pwZe1u4g56BcKBN8uWi8xNoqwwN5tktgpVq) | 627 s | 2348 | 0,061 | 1,47 M | 0,15 % | 28,6 |  |  |
| 23 | [`ELxcKr…1SCC`](https://solscan.io/account/ELxcKrDwPRKcKJNEMkqdUgHRtXhMtQsbT8KbtRh51SCC) | 627 s | 2348 | 0,083 | 2,00 M | 0,20 % | 28,6 |  |  |
| 24 | [`5SeKj8…hj1M`](https://solscan.io/account/5SeKj8h71kgTXNtTKtyBLesKC5X8vDeuuP8wjn5Uhj1M) | 627 s | 2348 | 1,002 | 23,24 M | 2,32 % | 28,6 |  |  |
| 25 | [`CapEWd…scWN`](https://solscan.io/account/CapEWd5ZrmywCoKB4J79rmip5tnz9fsUaxaSGgvMscWN) | 627 s | 2348 | 0,052 | 1,14 M | 0,11 % | 28,6 |  |  |
| 26 | [`jmemeh…wtru`](https://solscan.io/account/jmemehQbZXX7QqNE7Eyi81MdTZw6cEAT6TU4Kinwtru) | 627 s | 2348 | 1,645 | 35,89 M | 3,59 % | 28,6 |  | groupe 1 |
| 27 | [`EwMndg…FVsh`](https://solscan.io/account/EwMndgvbgdXuTCvT7bRGX8wPKVevyq7QZNVqWvFqFVsh) | 628 s | 2349 | 0,506 | 10,34 M | 1,03 % | 43,8 |  |  |
| 28 | [`FhF2n2…SNaV`](https://solscan.io/account/FhF2n25dWHMoh6TXfkZ51pSrDcNLptvGFKVYCzAqSNaV) | 628 s | 2349 | 0,509 | 10,09 M | 1,01 % | 43,8 |  |  |
| 29 | [`7W8SEZ…NRr8`](https://solscan.io/account/7W8SEZv79hk4445o56Fd6RzhbUsozkzGXi8vkc7vNRr8) | 628 s | 2349 | 0,429 | 8,40 M | 0,84 % | 43,8 |  |  |
| 30 | [`8dtx2t…1MEF`](https://solscan.io/account/8dtx2tr4TuJsYpri2suggFu1pg3DVjFLBBVmhtDy1MEF) | 628 s | 2349 | 0,828 | 15,77 M | 1,58 % | 43,8 |  |  |

Liste complète des 100 premiers : `early_buyers.csv`. MC en SOL : prix côté bonding curve × 1 Md.

## 4. Les 10 gros wallets du snapshot +38 min (FAIT)

Les pourcentages de la première investigation (4,1 / 4,1 / 3,7 / 3,6 / 3,2 / 2,3 / 2,1 / 2,1 / 1,8 / 1,8 %) correspondent **exactement** à ce snapshot calculé sur 1 Md de supply :

| Rang | Wallet | Tokens | % | Achats | Ventes | SOL investi | SOL récupéré | P&L réalisé | Restant | Premier / dernier mouvement | Groupe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [`CzpwuN…t11K`](https://solscan.io/account/CzpwuNRsLLcYS6pqtUokVsf8MsVA771CPkT2pcZWt11K) | 41,13 M | 4,11 % | 6 | 27 | 158,32 * | 1 013,59 * | **855,26** * | 0,00 M | 19/09 18:53 → 21/09 12:38 | — |
| 2 | [`Aveszu…BZc5`](https://solscan.io/account/AveszuoheU2tD8LDLGGUHmWQzfRus4bmvB1dt7KvBZc5) | 40,74 M | 4,07 % | 1 | 23 | 2,00 | 55,90 | **53,90** | 0,00 M | 19/09 18:52 → 21/09 00:22 | 1 |
| 3 | [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v) | 36,96 M | 3,70 % | 1 | 21 | 2,00 | 21,65 | **19,65** | 0,00 M | 19/09 18:52 → 19/09 20:11 | 1 |
| 4 | [`jmemeh…wtru`](https://solscan.io/account/jmemehQbZXX7QqNE7Eyi81MdTZw6cEAT6TU4Kinwtru) | 35,89 M | 3,59 % | 1 | 10 | 1,64 | 13,10 | **11,46** | 0,00 M | 19/09 18:26 → 19/09 19:08 | 1 |
| 5 | [`HbX6u6…qw8k`](https://solscan.io/account/HbX6u6QdUiXAD7r2QL9QBBc3NhoDjq2WbDxypK9dqw8k) | 32,41 M | 3,24 % | 2 | 5 | 4,00 | 15,51 | **11,51** | 0,00 M | 19/09 18:53 → 19/09 19:10 | 1 |
| 6 | [`4C8J6N…gio6`](https://solscan.io/account/4C8J6NdWviAscujksXZHXiHCmcJwUqNK3sYj4Gccgio6) | 22,90 M | 2,29 % | 2 | 2 | 0,90 * | 2,74 * | **1,84** * | 0,00 M | 19/09 18:49 → 19/09 18:58 | — |
| 7 | [`3SfQKT…iy7j`](https://solscan.io/account/3SfQKT4BKxrd6C2x4haVdQ8spY1Kf8ALv7CSNrTSiy7j) | 21,15 M | 2,12 % | 1 | 1 | 0,89 | 1,25 | **0,35** | 0,00 M | 19/09 18:28 → 19/09 19:04 | 1 |
| 8 | [`9bfwuA…mVZB`](https://solscan.io/account/9bfwuANwuEEaxuhY49Mk7hn8dr6sHPzbPKF7k3dhmVZB) | 21,03 M | 2,10 % | 96 | 36 | 90,74 | 106,38 | **15,64** | 0,96 M | 19/09 18:45 → 29/09 03:05 | 1 |
| 9 | [`7QtDFg…xKLL`](https://solscan.io/account/7QtDFgZhLycDiC5RspB2tPyoV6EkbLwetDSKCiWJxKLL) | 18,21 M | 1,82 % | 31 | 67 | 161,93 * | 337,47 * | **175,55** * | 0,19 M | 19/09 18:53 → 29/09 08:20 | — |
| 10 | [`8PoVFs…g5GU`](https://solscan.io/account/8PoVFsKZWXJcosU8b6XqJDrAKDkLnwq68wM5V1edg5GU) | 18,19 M | 1,82 % | 2 | 8 | 12,00 * | 16,86 * | **4,85** * | 0,00 M | 19/09 18:51 → 21/09 13:56 | 1 |

\* montants en partie **valorisés au prix d'exécution du pool** (ESTIMATION) : ces wallets paient en USDC ou via un routeur tiers, le SOL ne transite donc pas par leur compte.

- [`CzpwuN…t11K`](https://solscan.io/account/CzpwuNRsLLcYS6pqtUokVsf8MsVA771CPkT2pcZWt11K) : trader actif (6 achats / 27 ventes jusqu'au 21/09 12:38) ; principal financement avant 1er achat : 0,01 SOL de [`8zrWGh…W3fa`](https://solscan.io/account/8zrWGhEqts4J6wW1uWq19Uoh8DW3LHAhYnXYfDLWW3fa)
- [`Aveszu…BZc5`](https://solscan.io/account/AveszuoheU2tD8LDLGGUHmWQzfRus4bmvB1dt7KvBZc5) : principal financement avant 1er achat : 0,11 SOL de [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v)
- [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v) : principal financement avant 1er achat : 1,88 SOL de [`F7p3dF…gmNe`](https://solscan.io/account/F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe)
- [`jmemeh…wtru`](https://solscan.io/account/jmemehQbZXX7QqNE7Eyi81MdTZw6cEAT6TU4Kinwtru) : principal financement avant 1er achat : 0,01 SOL de [`9eM8ht…d35D`](https://solscan.io/account/9eM8htGuk7GSKFT1GP4hBrjpQTF7S5VbdrtuU3kmd35D)
- [`4C8J6N…gio6`](https://solscan.io/account/4C8J6NdWviAscujksXZHXiHCmcJwUqNK3sYj4Gccgio6) : principal financement avant 1er achat : 0,01 SOL de [`8zrWGh…W3fa`](https://solscan.io/account/8zrWGhEqts4J6wW1uWq19Uoh8DW3LHAhYnXYfDLWW3fa)
- [`3SfQKT…iy7j`](https://solscan.io/account/3SfQKT4BKxrd6C2x4haVdQ8spY1Kf8ALv7CSNrTSiy7j) : a transféré 10,58 M vers [`HPyj58…oZ29`](https://solscan.io/account/HPyj58oj68B4a9yW17oJYroGT7397h7zEvevjPe2oZ29) ; principal financement avant 1er achat : 1,43 SOL de [`ARu4n5…5SZn`](https://solscan.io/account/ARu4n5mFdZogZAravu7CcizaojWnS6oqka37gdLT5SZn)
- [`9bfwuA…mVZB`](https://solscan.io/account/9bfwuANwuEEaxuhY49Mk7hn8dr6sHPzbPKF7k3dhmVZB) : trader actif (96 achats / 36 ventes jusqu'au 29/09 03:05) ; principal financement avant 1er achat : 2,17 SOL de [`F7p3dF…gmNe`](https://solscan.io/account/F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe)
- [`7QtDFg…xKLL`](https://solscan.io/account/7QtDFgZhLycDiC5RspB2tPyoV6EkbLwetDSKCiWJxKLL) : a transféré 0,17 M vers [`5zPSHD…N82d`](https://solscan.io/account/5zPSHDVj5ZBY9WS5XFY4GqDU3pX7xycKY4Tgbu8kN82d), [`ExEPsN…RRde`](https://solscan.io/account/ExEPsNHPaRLErSnr1zUu119YePuKV21LDD1SRC9yRRde) ; trader actif (31 achats / 67 ventes jusqu'au 29/09 08:20) ; principal financement avant 1er achat : 0,00 SOL de [`8zrWGh…W3fa`](https://solscan.io/account/8zrWGhEqts4J6wW1uWq19Uoh8DW3LHAhYnXYfDLWW3fa)
- [`8PoVFs…g5GU`](https://solscan.io/account/8PoVFsKZWXJcosU8b6XqJDrAKDkLnwq68wM5V1edg5GU) : principal financement avant 1er achat : 0,47 SOL de [`F7p3dF…gmNe`](https://solscan.io/account/F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe)

## 5. Snipers, bundles et achats groupés (FAIT)

- **Achats dans les 5 premières secondes** : 3 wallets (créateur inclus), 7,77 % de la supply, 2,43 SOL. C'est l'ordre de grandeur des « ~8 % sniper holdings » des trackers.
- **Dans les 30 premières secondes** : 13 wallets, 20,81 %, 7,48 SOL.
- **« 1,36 % bundled »** : = 1,36 % — c'est le **dev buy du créateur, exécuté dans la même transaction que la création** (création + achat groupés). Ce n'est pas un réseau de wallets.
- **Transactions d'achat créditant plusieurs wallets** (bundle au sens strict) : 7 — toutes après la graduation, impliquant des wallets hors top 10.
- **Groupes d'achats dans un même slot** (INDICE faible seul) : 17 slots.
- **Achats avec tip Jito** parmi les 100 premiers : 18.

## 6. Recherche de wallets liés au créateur

**Résultat : aucun lien on-chain entre le créateur et un autre wallet analysé** (cluster du créateur = lui seul). Critères testés sur les ~50 wallets clés : funding commun (hors exchanges/services), transferts directs SOL ou token, achat payé par un autre wallet, destination commune des profits, achats dans le même slot.

- Le créateur n'a **reçu ni envoyé aucun token** JEANPHIL hors de son dev buy (hors une poussière de 2,36 tokens reçue lors d'une distribution de fees).
- Ses sorties de SOL vont toutes vers un même wallet intermédiaire, puis vers un service unique (voir §8).

**Groupes identifiés entre autres wallets** (liens FAIT ou INDICE fort — *sans lien avec le créateur*) :

- **Groupe 1** — 28 wallets, dont 7 du top 10 ([`3SfQKT…iy7j`](https://solscan.io/account/3SfQKT4BKxrd6C2x4haVdQ8spY1Kf8ALv7CSNrTSiy7j), [`8PoVFs…g5GU`](https://solscan.io/account/8PoVFsKZWXJcosU8b6XqJDrAKDkLnwq68wM5V1edg5GU), [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v), [`9bfwuA…mVZB`](https://solscan.io/account/9bfwuANwuEEaxuhY49Mk7hn8dr6sHPzbPKF7k3dhmVZB), [`Aveszu…BZc5`](https://solscan.io/account/AveszuoheU2tD8LDLGGUHmWQzfRus4bmvB1dt7KvBZc5), [`HbX6u6…qw8k`](https://solscan.io/account/HbX6u6QdUiXAD7r2QL9QBBc3NhoDjq2WbDxypK9dqw8k), [`jmemeh…wtru`](https://solscan.io/account/jmemehQbZXX7QqNE7Eyi81MdTZw6cEAT6TU4Kinwtru)). Liens : destination_commune_profits, financement_direct, funder_commun, transfert_SOL.
- **Groupe 2** — 4 wallets, dont 0 du top 10 (—). Liens : destination_commune_profits.
  - funder commun [`F7p3dF…gmNe`](https://solscan.io/account/F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe) → 8 wallets financés, dont 5 du top 10 : [`9bfwuA…mVZB`](https://solscan.io/account/9bfwuANwuEEaxuhY49Mk7hn8dr6sHPzbPKF7k3dhmVZB), [`8PoVFs…g5GU`](https://solscan.io/account/8PoVFsKZWXJcosU8b6XqJDrAKDkLnwq68wM5V1edg5GU), [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v), [`Aveszu…BZc5`](https://solscan.io/account/AveszuoheU2tD8LDLGGUHmWQzfRus4bmvB1dt7KvBZc5), [`HbX6u6…qw8k`](https://solscan.io/account/HbX6u6QdUiXAD7r2QL9QBBc3NhoDjq2WbDxypK9dqw8k)
  - funder commun [`ARu4n5…5SZn`](https://solscan.io/account/ARu4n5mFdZogZAravu7CcizaojWnS6oqka37gdLT5SZn) → 3 wallets financés, dont 1 du top 10 : [`3SfQKT…iy7j`](https://solscan.io/account/3SfQKT4BKxrd6C2x4haVdQ8spY1Kf8ALv7CSNrTSiy7j)
  - funder commun [`7jJRu7…o2Wo`](https://solscan.io/account/7jJRu7GWwUhRyfjjXKHZQKYpSnSXjGxVYnEryXsKo2Wo) → 2 wallets financés, dont 2 du top 10 : [`Aveszu…BZc5`](https://solscan.io/account/AveszuoheU2tD8LDLGGUHmWQzfRus4bmvB1dt7KvBZc5), [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v)

*Un groupe est une composante connexe : deux wallets d'un même groupe peuvent n'être reliés qu'indirectement (A↔B et B↔C). Le lien le plus solide est le funder commun ci-dessus.*

INDICE : le groupe principal ressemble à un opérateur de snipe/trading multi-wallets (financement commun, profits reversés vers une même adresse, qui refinance à son tour le funder). Rien ne le relie au créateur.

## 7. Tableau de synthèse des wallets clés

| Wallet | Relation | SOL investi | % supply max | Tokens vendus | SOL récupéré | P&L réalisé (SOL) | Position restante |
|---|---|---|---|---|---|---|---|
| [`CKB1XY…uN5d`](https://solscan.io/account/CKB1XYgbEmfEE3FJev7gFwEVtoqEvmsX6GhnbuFvuN5d) | early buyer · groupe 1 | 2,68 | 8,53 % | 85,27 M | 4,83 | 2,15 | 0,00 M |
| [`8PoVFs…g5GU`](https://solscan.io/account/8PoVFsKZWXJcosU8b6XqJDrAKDkLnwq68wM5V1edg5GU) | top10 snapshot · groupe 1 | 12,00 | 4,74 % | 47,48 M | 16,86 | 4,85 | 0,00 M |
| [`CzpwuN…t11K`](https://solscan.io/account/CzpwuNRsLLcYS6pqtUokVsf8MsVA771CPkT2pcZWt11K) | top10 snapshot | 158,32 | 4,11 % | 44,47 M | 1 013,59 | 855,26 | 0,00 M |
| [`Aveszu…BZc5`](https://solscan.io/account/AveszuoheU2tD8LDLGGUHmWQzfRus4bmvB1dt7KvBZc5) | top10 snapshot · groupe 1 | 2,00 | 4,07 % | 40,74 M | 55,90 | 53,90 | 0,00 M |
| [`5e8DjV…EA5W`](https://solscan.io/account/5e8DjVTq2NxESfa3RtMeGyhifiDyuwo4zmRHj8JNEA5W) | early buyer · groupe 1 | 3,01 | 3,95 % | 53,08 M | 4,14 | 1,13 | 0,00 M |
| [`ApMDvX…Ewq1`](https://solscan.io/account/ApMDvXrCztsLqmo3g8DbGawkaKSMEwQBNKSutAuWEwq1) | gros holder · groupe 1 | 5,00 | 3,81 % | 38,05 M | 10,74 | 5,74 | 0,00 M |
| [`9Bge8w…YY7v`](https://solscan.io/account/9Bge8wSj8D9yghaNjSJoCJFhUTP8q4KssuE6MmjDYY7v) | top10 snapshot · groupe 1 | 2,00 | 3,70 % | 36,96 M | 21,65 | 19,65 | 0,00 M |
| [`jmemeh…wtru`](https://solscan.io/account/jmemehQbZXX7QqNE7Eyi81MdTZw6cEAT6TU4Kinwtru) | top10 snapshot · groupe 1 | 1,64 | 3,59 % | 35,89 M | 13,10 | 11,46 | 0,00 M |
| [`DSQeAa…ixa6`](https://solscan.io/account/DSQeAaPEdWsqAYBG6wmQE3oxoCGTUVb8Xu2ouRmzixa6) | gros holder · groupe 1 | 21,36 | 3,58 % | 25,74 M | 466,91 | 445,55 | 3,76 M |
| [`GeyTZy…AyUw`](https://solscan.io/account/GeyTZyQTzzsUyceWAkdaHwgrRLmsWq1T7x3VFmLAyUw) | gros holder · groupe 1 | 0,00 | 3,58 % | 35,77 M | 1,43 | 1,43 | 0,00 M |
| [`9keCU8…KQSp`](https://solscan.io/account/9keCU8mgA23XV8LCgSCJEo4Lspmo9fRBA3MyxJmZKQSp) | gros holder · groupe 1 | 2,00 | 3,54 % | 35,44 M | 1,90 | -0,11 | 0,00 M |
| [`BMkHjN…gXWJ`](https://solscan.io/account/BMkHjN2N8K2PdCqeC92YYjUovn9ecW4GvFpH6yDggXWJ) | early buyer · groupe 1 | 1,08 | 3,51 % | 35,08 M | 1,08 | -0,00 | 0,00 M |
| [`4bgyVZ…QQta`](https://solscan.io/account/4bgyVZgsau9wkim1H2bhhuGBj41ZXgqMzAUYjkDGQQta) | gros holder | 7,00 | 3,50 % | 45,09 M | 604,76 | 597,76 | 0,00 M |
| [`2DsuQt…yQ3r`](https://solscan.io/account/2DsuQtNNP1xWGot7gAfzVc2GpGpyWAvP4iFETs6qyQ3r) | gros holder · groupe 1 | 0,00 | 3,49 % | 34,85 M | 1,62 | 1,61 | 0,00 M |
| [`7Y6S3F…oQrM`](https://solscan.io/account/7Y6S3F9Y6z4No9Nsy1UG2gpSsmAMaduijZ8Ymt4soQrM) | gros holder | 7,35 | 3,39 % | 34,26 M | 393,96 | 386,61 | 0,00 M |
| [`HbX6u6…qw8k`](https://solscan.io/account/HbX6u6QdUiXAD7r2QL9QBBc3NhoDjq2WbDxypK9dqw8k) | top10 snapshot · groupe 1 | 4,00 | 3,24 % | 32,41 M | 15,51 | 11,51 | 0,00 M |
| [`CcJX97…DBcf`](https://solscan.io/account/CcJX975YTw8owyuRwyC1m9pyC3ZhRp89VM12pfUfDBcf) | gros holder · groupe 1 | 1,77 | 3,20 % | 32,04 M | 1,79 | 0,02 | 0,00 M |
| [`BQEQ48…NnTC`](https://solscan.io/account/BQEQ48NS9R9TLycSiEKjnaLErGfXxhMszbiA2SYmNnTC) | gros holder · groupe 1 | 1,82 | 3,19 % | 31,85 M | 1,21 | -0,61 | 0,00 M |
| [`2WAezA…GouL`](https://solscan.io/account/2WAezAawFNVUttsXdy4GTymV9aEMvM7fpGq1ZFHuGouL) | early buyer · groupe 2 | 1,73 | 3,17 % | 43,64 M | 1,78 | 0,05 | 0,00 M |
| [`7rnTq4…q1xg`](https://solscan.io/account/7rnTq4E9bgkYTqMx62142zAFXnyifkDdJgGZc8jNq1xg) | gros holder | 6,70 | 3,08 % | 30,80 M | 180,61 | 173,91 | 0,00 M |
| [`27xjYF…2QUG`](https://solscan.io/account/27xjYFf3pQuHTLnNogacXii3rKzEyjD5nWkFdjvs2QUG) | early buyer · groupe 1 | 1,01 | 2,91 % | 29,15 M | 1,06 | 0,04 | 0,00 M |
| [`2sapux…Dpz7`](https://solscan.io/account/2sapuxSmfbKAziDJKTwJWtqfZoukBLKX5zeBCVdPDpz7) | early buyer · groupe 1 | 0,95 | 2,90 % | 28,97 M | 0,83 | -0,11 | 0,00 M |
| [`HGxBHp…G9AV`](https://solscan.io/account/HGxBHpUsFbN9Mnf78pCNBMkYnYdEQqcensEiBvX3G9AV) | early buyer · groupe 1 | 1,01 | 2,83 % | 28,27 M | 1,50 | 0,50 | 0,00 M |
| [`4WxE3G…dzhP`](https://solscan.io/account/4WxE3GAiFG6EofdSF4N3DWXg5na9V3BQJJN5LuE5dzhP) | early buyer · groupe 1 | 2,51 | 2,81 % | 31,80 M | 2,45 | -0,05 | 0,00 M |
| [`FeS5hu…T2q3`](https://solscan.io/account/FeS5huVYxZGEP4peg9bGiViSbesfCjyrD564s3ibT2q3) | early buyer · groupe 1 | 1,02 | 2,76 % | 27,60 M | 1,03 | 0,02 | 0,00 M |
| [`CiueJw…urDC`](https://solscan.io/account/CiueJwuBw1cZVz4YzY4TpPtyaEQJEpmYZmxkLAuXurDC) | early buyer · groupe 1 | 3,51 | 2,63 % | 66,30 M | 3,58 | 0,07 | 0,00 M |
| [`985sqa…hVdZ`](https://solscan.io/account/985sqazousgFWXYTMnoLHBsdUfWJfHoCcPCYhkYBhVdZ) | early buyer · groupe 2 | 1,63 | 2,55 % | 38,96 M | 1,53 | -0,10 | 0,00 M |
| [`7vZu6H…1uQP`](https://solscan.io/account/7vZu6HQakBZmvYjD2GWKLRcdm4vVtaS5qxxrY3bZ1uQP) | early buyer · groupe 2 | 1,67 | 2,48 % | 38,05 M | 1,41 | -0,26 | 0,00 M |
| [`J2ztQn…2911`](https://solscan.io/account/J2ztQnZijWHQZeF18o6wvcKFttovvBoUjUvHPB4w2911) | early buyer · groupe 2 | 1,51 | 2,47 % | 36,69 M | 1,30 | -0,21 | 0,00 M |
| [`4C8J6N…gio6`](https://solscan.io/account/4C8J6NdWviAscujksXZHXiHCmcJwUqNK3sYj4Gccgio6) | top10 snapshot | 0,90 | 2,29 % | 22,99 M | 2,74 | 1,84 | 0,00 M |
| [`3SfQKT…iy7j`](https://solscan.io/account/3SfQKT4BKxrd6C2x4haVdQ8spY1Kf8ALv7CSNrTSiy7j) | top10 snapshot · groupe 1 | 0,89 | 2,12 % | 10,58 M | 1,25 | 0,35 | 0,00 M |
| [`9bfwuA…mVZB`](https://solscan.io/account/9bfwuANwuEEaxuhY49Mk7hn8dr6sHPzbPKF7k3dhmVZB) | top10 snapshot · groupe 1 | 90,74 | 2,10 % | 23,82 M | 106,38 | 15,64 | 0,96 M |
| [`7QtDFg…xKLL`](https://solscan.io/account/7QtDFgZhLycDiC5RspB2tPyoV6EkbLwetDSKCiWJxKLL) | top10 snapshot | 161,93 | 1,82 % | 23,65 M | 337,47 | 175,55 | 0,19 M |
| [`ojiyUR…pk67`](https://solscan.io/account/ojiyURrcv3kvTaqdFN1gPYQ56GeyQbR6z9iN3JCpk67) | early buyer · groupe 1 | 0,73 | 1,71 % | 17,08 M | 0,71 | -0,02 | 0,00 M |
| [`BS3FxZ…dE3B`](https://solscan.io/account/BS3FxZoEnDjt76iR3WhEkQZhLqLARVCDFu4dc4Z9dE3B) | créateur | 0,40 | 1,36 % | 0,00 M | 0,00 | -0,40 | 13,63 M |
| [`Hh2yn3…2PzL`](https://solscan.io/account/Hh2yn37jiXuwCM4nkvAZPbc8CjL6j32Ho38giC1y2PzL) | early buyer · groupe 1 | 0,45 | 0,95 % | 9,47 M | 0,50 | 0,05 | 0,00 M |
| [`FSz6mp…4BZX`](https://solscan.io/account/FSz6mptAxKrjDjaJYQiGiCGGwsxL4WgWjsh9sGhw4BZX) | early buyer · groupe 1 | 2,12 | 0,79 % | 29,83 M | 2,40 | 0,28 | 0,00 M |
| [`Gsjt6k…NPqB`](https://solscan.io/account/Gsjt6kLdidphL7FbzZyS4W1WohqEQoLoZa3h9782NPqB) | early buyer · groupe 1 | 0,21 | 0,46 % | 4,58 M | 0,16 | -0,05 | 0,00 M |
| [`5FihbC…uks4`](https://solscan.io/account/5FihbCbCqXdz6yHcVWyyJbn1G2cpoarJ38RyAGFquks4) | early buyer · groupe 1 | 0,05 | 0,12 % | 1,19 M | 0,06 | 0,00 | 0,00 M |
| [`H3dMhU…d4Fw`](https://solscan.io/account/H3dMhUXA153HdEVkG9KLURpBQwpwvQdt4B6nEvgod4Fw) | early buyer | 0,04 | 0,02 % | 0,22 M | 0,01 | -0,03 | 0,00 M |

**Plus gros P&L réalisés parmi les wallets clés** : [`CzpwuN…t11K`](https://solscan.io/account/CzpwuNRsLLcYS6pqtUokVsf8MsVA771CPkT2pcZWt11K) 855,3 SOL (top10 snapshot) ; [`4bgyVZ…QQta`](https://solscan.io/account/4bgyVZgsau9wkim1H2bhhuGBj41ZXgqMzAUYjkDGQQta) 597,8 SOL (gros holder) ; [`DSQeAa…ixa6`](https://solscan.io/account/DSQeAaPEdWsqAYBG6wmQE3oxoCGTUVb8Xu2ouRmzixa6) 445,5 SOL (gros holder) ; [`7Y6S3F…oQrM`](https://solscan.io/account/7Y6S3F9Y6z4No9Nsy1UG2gpSsmAMaduijZ8Ymt4soQrM) 386,6 SOL (gros holder) ; [`7QtDFg…xKLL`](https://solscan.io/account/7QtDFgZhLycDiC5RspB2tPyoV6EkbLwetDSKCiWJxKLL) 175,5 SOL (top10 snapshot) ; [`7rnTq4…q1xg`](https://solscan.io/account/7rnTq4E9bgkYTqMx62142zAFXnyifkDdJgGZc8jNq1xg) 173,9 SOL (gros holder).

*% supply max : maximum observé pendant la fenêtre complète (1re heure). Détails et transactions : `wallets_pnl.csv`.*

## 8. Wallet créateur `BS3Fx…dE3B` (FAIT)

- **Pourquoi « 13,6 M / 1,4 % »** : c'est le dev buy de 13 634 393,23 tokens acheté **dans la transaction de création** ([`4wi3ZcYa…`](https://solscan.io/tx/4wi3ZcYaGunjZx7Z9JoA2fa1CNY9zMs5xSa4BNwUjJzfBG5NRHtHiMQ1CB1e4j4iQJ2BTzL3xLksdmbGjLEqLYNB)) pour 0,4010 SOL. Coût : ≈ 45 $.
- **Pourquoi certains trackers affichaient 0 %** : les tokens n'ont jamais bougé (aucune vente, aucun transfert sortant). L'écart vient donc de l'affichage du tracker (ex. dev buy intégré à la tx de création non compté comme « holding dev », ou compte Token-2022 non indexé) — ce n'est pas un mouvement on-chain.
- **Ventes** : aucune. **Position actuelle** : 13 634 395,59 JEANPHIL (≈ 476,1 SOL au prix spot, ≈ 343,4 SOL si vendus d'un bloc dans le pool PumpSwap — ESTIMATION).
- **Sorties de SOL après le lancement** (FAIT) :
  - 22/09/2026 21:56:28 : **0,10 SOL** → [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) ([`5jrdehEy…`](https://solscan.io/tx/5jrdehEyerH5Nay8q465qK77ScaaV48LV6JHXCx3TUgWkw1LnnD2hwKjRo8WNVfLvpYBMLxST7zFP5op1AxnNajd)) ≈ 12 $
  - 22/09/2026 22:01:20 : **50,00 SOL** → [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) ([`4dubGtQt…`](https://solscan.io/tx/4dubGtQtaM8vy8JjBJKkjUEbDEhzf2cx6yWd6iSMDC36WBQZqMbRMw5Toyy8Lzr6iLsisQFgmA9wp1tqECF3QF2b)) ≈ 5 939 $
  - 22/09/2026 22:02:15 : **450,00 SOL** → [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) ([`2Tq4G6xw…`](https://solscan.io/tx/2Tq4G6xwVvKP2wLBL2jmsbGV1fHjFuCLMvaudMRZ7V1ebfTyaHfo98Tt318ZN6mMs76LQWyBn23FYKntswYyfhYG)) ≈ 53 447 $
  - 25/09/2026 09:31:55 : **500,00 SOL** → [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) ([`2gndqhkk…`](https://solscan.io/tx/2gndqhkkfUeipTCVmeAvV6CPoyX2BXXq8suGopDZPfZmdqnbC5W2rCFdEf5ov5JdykA2w5Jh47rk4swZMGQmKhyB)) ≈ 59 132 $
  - 28/09/2026 19:43:55 : **425,00 SOL** → [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) ([`4noB6XWv…`](https://solscan.io/tx/4noB6XWvDDwNfiurhQUKceZcYnvVswiDMna9fJwn9cKfY65UGo7CN3DomGySndANp4TgKqSA4HTvuLuir8nkCUBs)) ≈ 50 239 $
  - Total sorti : **1 425,10 SOL** ≈ 168 768 $ ; solde actuel du wallet créateur : 435,62 SOL.
  - [`EBBpe3…JqGo`](https://solscan.io/account/EBBpe3rnTEhPm5AmjQnY6arMx2k3quZicJyRVSfeJqGo) a redistribué vers 7 adresses à usage unique, toutes vidées vers [`6tckHF…LoDQ`](https://solscan.io/account/6tckHFBpiJ8YgYN8FUskvtvTpXQZ55g5LHeo1kvELoDQ) (1 425,10 SOL) — wallet de service très actif (≈ 24 800 SOL, des dizaines d'expéditeurs par heure) : schéma d'adresses de dépôt d'exchange (INDICE). Aucun de ces fonds ne revient vers les gros wallets.
- **Autres revenus** : 9,72 SOL reçus via `DistributeCreatorFees` (partage de frais Pump.fun, 13 comptes sources) — distincts des fees JEANPHIL.
- **Autres tokens créés** : 0 (une seule création signée : JEANPHIL).

## 9. Creator fees Pump.fun (FAIT)

- Vault bonding curve : [`D8W7WXU3pNLdLeUQFt9t72Nsym9RxUWBfJbGBcybRWvR`](https://solscan.io/account/D8W7WXU3pNLdLeUQFt9t72Nsym9RxUWBfJbGBcybRWvR) (PDA `creator-vault` du créateur)
- Vault PumpSwap : [`8VEL436KcmKcJJaab9as4PmK1myTpzNsjt8HQ4tZJXfU`](https://solscan.io/account/8VEL436KcmKcJJaab9as4PmK1myTpzNsjt8HQ4tZJXfU) (PDA `creator_vault`, fees en WSOL)
- Méthode : aucune hypothèse de barème — on lit les SOL **effectivement** reçus (claims) + le solde non réclamé des vaults. Le créateur n'a lancé qu'un seul token (une seule instruction `CreateV2` dans son historique), donc 100 % de ces fees proviennent de JEANPHIL.

| Date (UTC) | Transaction | SOL reçus | Cours SOL | ≈ USD |
|---|---|---|---|---|
| 22/09/2026 21:49:26 | [`24gJWiZe…`](https://solscan.io/tx/24gJWiZet5rfPh7EPJwor4i61nhXvcCscQD4SADQx75ro4MrXBrCSzks62HUzQocEr32KByckornskYu5UyVjjEP) | 1 360,724 | 118,18 $ | 160 805 $ |
| 28/09/2026 19:40:06 | [`3qA9BaMu…`](https://solscan.io/tx/3qA9BaMutMeWjrcQ3aLRyqxNS1sAPWMT3jMUezs3YFHDciFtb72n27ghxpLtmN1ugsepJF5ckeinbkqXp6qtsPrT) | 452,244 | 118,21 $ | 53 460 $ |
| 29/09/2026 12:09:48 | [`f4XQt5wT…`](https://solscan.io/tx/f4XQt5wTbU7TALKNrAsmvZEg7zjgDcDoRe8Bhuwa6Tt5fK3yxgoZe5MhWcHyyS7emECg8LGN2EuF9pjjiid8Bny) | 37,995 | 120,59 $ | 4 582 $ |
| **Total réclamé** | | **1 850,964** | | **218 846 $** |
| Non réclamé (maintenant) | | 1,311 | 120,59 $ | 158 $ |

- Fees générées pendant la **seule 1re heure** : 7,801 SOL (1,315 sur la bonding curve + 6,486 sur PumpSwap en 9 min).
- Taux effectif ≈ fees totales / volume : 219 005 $ / 77 711 808 $ ≈ **0,282 %** du volume (ESTIMATION ; inclut des volumes Meteora/Raydium qui ne paient pas de creator fee Pump.fun).
- Les revenus `DistributeCreatorFees` (§8) ne sont pas inclus ci-dessus.

**Distinction demandée** : revenus issus des ventes de tokens = **0 SOL** ; revenus issus des creator fees = **1 850,96 SOL réclamés**.

## 10. Market cap, volume et holders

| T+ | Heure (UTC) | Market cap | Volume cumulé | Holders | Source |
|---|---|---|---|---|---|
| +0 min | 19/09 18:15 | n/d (n/d SOL) | 44 $ (0,4 SOL) | 1 | FAIT on-chain |
| +5 min | 19/09 18:20 | 3 273 $ (29,5 SOL) | 3 259 $ (29,4 SOL) | 1 | FAIT on-chain |
| +15 min | 19/09 18:30 | 4 053 $ (36,5 SOL) | 11 723 $ (105,6 SOL) | 16 | FAIT on-chain |
| +30 min | 19/09 18:45 | 4 135 $ (37,3 SOL) | 12 015 $ (108,3 SOL) | 13 | FAIT on-chain |
| +38 min | 19/09 18:53 | 15 052 $ (135,6 SOL) | 16 570 $ (149,3 SOL) | 82 | FAIT on-chain |
| +60 min | 19/09 19:15 | 110 104 $ (992,5 SOL) | 129 984 $ (1 171,6 SOL) | 392 | FAIT on-chain |
| +2 h | 19/09 20:15 | 313 657 $ | 294 743 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +4 h | 19/09 22:15 | 2 560 700 $ | 3 845 065 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +8 h | 20/09 02:15 | 4 512 074 $ | 11 444 510 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +12 h | 20/09 06:15 | 2 965 615 $ | 13 485 645 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +24 h | 20/09 18:15 | 8 469 598 $ | 28 289 777 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +2 j | 21/09 18:15 | 1 592 116 $ | 42 896 097 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +3 j | 22/09 18:15 | 3 007 688 $ | 47 399 602 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +5 j | 24/09 18:15 | 5 120 440 $ | 62 787 445 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |
| +7 j | 26/09 18:15 | 4 810 944 $ | 71 848 702 $ (pools DEX) | n/d | ESTIMATION GeckoTerminal |

- **ATH** (pool principal PumpSwap) : **0,01158 $ le 20/09/2026 17:02:00 UTC** → ≈ **11 580 066 $** de market cap (1 Md) / 11 226 709 $ (supply actuelle). Des mèches plus hautes existent sur de petits pools Meteora (ex. 0,01322 $), peu liquides : non retenues.
- Volume cumulé à l'ATH ≈ 25 279 830 $ ; holders à l'ATH : n/d (hors fenêtre téléchargée intégralement).
- Source secondaire divergente : « ATH 0,01066 $ le 25/09 » (CoinCodex/Coinbase) — probablement un plus haut journalier sur un autre agrégat ; le plus haut minute du pool principal est celui ci-dessus.
- **Volume total** depuis la graduation (6 pools) : **77 711 808 $** — pumpswap 53 819 775 $, meteora 13 149 702 $, meteora 6 025 280 $, meteora 551 423 $, meteora 3 378 706 $, raydium 786 922 $ (ESTIMATION GeckoTerminal ; peut inclure du volume de bots).
- **Holders actuels** : **16 854** (Helius DAS, comptes avec solde > 0).
- **Prix actuel** : 0,00421 $ → market cap ≈ 4 211 165 $.

## 11. Graduation Pump.fun → PumpSwap (FAIT)

- **Transaction** : [`2pAfa2Cd…`](https://solscan.io/tx/2pAfa2CdK8SpJguaMjngHr8si1XjvyHMxUYr8PQ9738piJUL9T9ZaKXb1H1AoruNgQeLPuCqxiEG2w8QE2dXuneE) — **19/09/2026 19:06:59 UTC**, soit **+51 min 03 s** après la création (instruction `MigrateV2`).
- **Pool créé** : [`4R8CiMnJWDNoes3fQi1ccPFJygPXazaHaWpHrN3rZeNj`](https://solscan.io/account/4R8CiMnJWDNoes3fQi1ccPFJygPXazaHaWpHrN3rZeNj)
- **Liquidité initiale** : 206 900 000 JEANPHIL + 67,408 SOL (≈ 7 478 $ côté SOL). La bonding curve a libéré 85,005 SOL : 67,408 SOL au pool et 17,597 SOL vers [`82JmGH…jGYM`](https://solscan.io/account/82JmGHFueekV8KGFim7BHd1TieAtDBcR5oeHj5ECjGYM) (frais de migration / protocole — INDICE).
- **Market cap à la graduation** : ≈ 36 145 $ (prix initial du pool × 1 Md).
- **Gros wallets du snapshot** : sur 319,01 M tokens vendus au total, 165,50 M (52 %) l'ont été **avant** la graduation (sur la bonding curve) et 264,96 M (83 %) avant graduation + 1 h ; le reste (traders actifs) s'étale sur les jours suivants (détail §4 et §12).

## 12. HYPOTHÈSE — « les 10 gros wallets du snapshot appartiennent au créateur »

> **Ceci n'est pas un fait.** Aucun lien on-chain n'a été trouvé entre ces wallets et le créateur ; plusieurs appartiennent à des groupes distincts entre eux. Le calcul ci-dessous répond seulement à la question « combien SI c'était la même personne ».

1. **Argent injecté** : 434,44 SOL (≈ 49 214 $) par les 10 wallets, + 0,401 SOL du créateur.
2. **% de supply obtenu** au snapshot : 28,86 % (+ 1,36 % du créateur).
3. **Évolution de la position** (valeur au prix du marché au moment de chaque mouvement) :

| Date | Tokens détenus (cluster) | SOL injectés cumulés | SOL récupérés cumulés | Valeur de marché (SOL) |
|---|---|---|---|---|
| 19/09 18:26 | 35,89 M | 1,6 | 0,0 | 1,6 |
| 19/09 18:51 | 136,71 M | 6,1 | 0,5 | 6,7 |
| 19/09 19:31 | 61,67 M | 17,9 | 78,9 | 61,2 |
| 19/09 20:13 | 35,93 M | 18,3 | 167,7 | 35,7 |
| 19/09 22:26 | 18,92 M | 29,4 | 449,3 | 18,8 |
| 21/09 13:56 | 1,31 M | 317,6 | 1 451,9 | 1,3 |
| 29/09 08:20 | 1,15 M | 434,4 | 1 584,5 | 1,1 |

4. **Tokens vendus** : 319,01 M — **prix moyen de vente** 4,967 SOL par million de tokens.
5. **SOL récupérés** : 1 584,45 SOL (≈ 176 872 $).
6. **Tokens restants** : 1,15 M (≈ 40,2 SOL spot).
7. **Creator fees** (réelles, du créateur) : 1 850,96 SOL (≈ 218 846 $).
8. **P&L réalisé du cluster** : 1 150,01 SOL (≈ 127 658 $) ; **latent** : ≈ 38,8 SOL.

**Sous cette hypothèse**, la personne aurait mis **≈ 434,8 SOL (≈ 49 258 $)** de sa poche, encaissé **≈ 1 584,5 SOL (≈ 176 872 $)** en ventes, gagné **1 851,0 SOL (≈ 218 846 $)** en creator fees, et détiendrait encore **14,79 M** (≈ 382,3 SOL en liquidation). Gain réalisé total ≈ **346 460 $**.

*Attention : ces wallets ont aussi racheté/revendu bien après le snapshot (traders actifs) ; le calcul inclut toute leur activité JEANPHIL, pas seulement la position initiale.*

## 13. Comparaison avec $DAVID (`8wtdds…pump`)

**Faits DAVID (on-chain)** :

- Création : [`4EiAcspX…`](https://solscan.io/tx/4EiAcspXx4BhpFXNQwyUCAuABLyuXP6RMPKD6NfMQMJcmFvTh41LhZmYgvnqq7kT2xNSYYxLWLJSwc3s5a6kpfnQ) le 01/08/2026 20:23:23 UTC par [`J2quY8x5xaUi4LwWoNngV7JjUsyporhNiZGU4ZsxkbFh`](https://solscan.io/account/J2quY8x5xaUi4LwWoNngV7JjUsyporhNiZGU4ZsxkbFh) (31,95 SOL sur le wallet).
- **Dev buy : 500,00 M (50,0 % de la supply) pour 26,52 SOL** dans la transaction de création.
- **Vente de la totalité (500,00 M) 8 min 10 s après la création** pour **331,27 SOL** ([`3G3fYw6u…`](https://solscan.io/tx/3G3fYw6uk2tCYCq2J9UxuoW81mq1rJpcH3mgvGEsDyAWJvun97WVBcULsndFFx7ucuiRWQ4vRbg4Pe9rBSpRRUnf)).
- Le « wallet communautaire de 50 % » annoncé correspond donc, on-chain, au **dev buy du wallet créateur**, vendu en une transaction — il n'a pas été conservé ni distribué depuis ce wallet.
- Creator fees réclamées : **176,70 SOL** (≈ 12 646 $).
- **INDICE fort de wallet lié au créateur DAVID** : [`AecDkA…3Ucn`](https://solscan.io/account/AecDkAhE8GrYM1FRRcXnZejMkG58uYg8TnJU2Ww93Ucn) (n°3 au snapshot +5 min) achète 42,51 M pour 6,26 SOL 8 s après la création, revend tout pour **218,42 SOL**, puis envoie ses profits vers [`5cMKyZ…o2jb`](https://solscan.io/account/5cMKyZ58Z3nCMPenf1HiANGkbBfZE8GCtPD1kzZwo2jb) — **la même adresse** qui reçoit les SOL du créateur. Cette adresse n'a que quelques expéditeurs (wallet personnel, pas un exchange). Non prouvé, mais cohérent avec un créateur qui snipe son propre lancement avec un second wallet.
- Graduation : +55 s après création.
- ATH minute : 0,001459 $ (≈ 1 459 042 $) le 01/08/2026 20:27:00 — dans les 5 premières minutes, avant la vente du créateur. Les « ≈ 109 k$ » de la première investigation correspondent au rebond après cette vente.

| Indicateur | JEANPHIL | DAVID |
|---|---|---|
| Capital initial du créateur (dev buy) | 0,40 SOL ≈ 45 $ | 26,52 SOL ≈ 1 897 $ |
| Dev buy (% supply) | 1,36 % | 50,00 % |
| Ventes du créateur | aucune | 100 % à +8 min 10 s |
| SOL encaissés en ventes par le créateur | 0 | 331,27 |
| Top 10 au snapshot (hors pools) | 28,9 % à +38 min | 65,9 % à +5 min |
| Tx réussies dans la fenêtre initiale | 4819 en 60 min | 35576 en 9 min |
| Achats dans les 5 premières s | 3 wallets / 7,8 % | 18 wallets / 57,4 % |
| Délai de graduation | 51 min 03 s | 55 s |
| ATH (market cap) | 11 580 066 $ | 1 459 042 $ |
| Moment de l'ATH | +22 h 46 | +3 min 37 s |
| Volume DEX cumulé | 77 711 808 $ | 1 630 257 $ |
| Holders actuels | 16 854 | 1 010 |
| Creator fees réclamées | 1 851,0 SOL ≈ 218 846 $ | 176,7 SOL ≈ 12 646 $ |

**Pourquoi JEANPHIL a eu beaucoup plus de traction — lecture quantitative :**

1. **Offre flottante** : JEANPHIL a démarré avec un dev buy de 1,4 % jamais vendu ; DAVID avec 50 % concentrés dans un seul wallet, revendus 8 minutes après le lancement. Cette vente a absorbé la liquidité des premiers acheteurs (chute du prix d'environ 95 % en une minute sur les chandeliers).
2. **Durée de la demande** : le volume de DAVID est concentré dans la première heure ; celui de JEANPHIL s'étale sur 10 jours (≈ 71 958 706 $ à J+7).
3. **Distribution** : les snipers de JEANPHIL ont revendu dès les 10 premières minutes (market cap revenue au niveau de départ), puis une seconde vague d'acheteurs organiques a porté le token à la graduation — la structure de détention n'était pas dominée par un seul acteur.
4. **Revenus du créateur** : volume ≈ 48× supérieur pour JEANPHIL → creator fees 10× supérieures, sans vente de tokens.

## 14. Limites et points non résolus

- Fenêtre téléchargée intégralement : 1re heure (création → +60 min, graduation incluse). Au-delà, les wallets clés sont suivis individuellement (tout leur historique JEANPHIL), mais pas l'ensemble des holders.
- Nombre de holders entre +1 h et aujourd'hui : non reconstruit (il faudrait rejouer >3 millions de transactions).
- Montants en dollars : conversion au cours SOL/USD horaire (GeckoTerminal) — ESTIMATION.
- Swaps payés en USDC / via routeur : valorisés au prix d'exécution du pool (ESTIMATION), marqués *.
- Identification des exchanges/services : par comportement (nombre de contreparties), sans base d'étiquettes type Arkham.
