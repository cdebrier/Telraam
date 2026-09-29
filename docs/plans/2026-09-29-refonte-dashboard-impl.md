# Refonte du dashboard — Plan d'implémentation

Référence : [design validé](2026-09-29-refonte-dashboard-design.md) (décisions D1–D11).
Principe : chaque étape laisse un `index.html` fonctionnel et commitable. On avance en tranches verticales, pas en gros bloc.

## Constats préalables (vérifiés dans le code)

- Données : `window.TELRAAM_RIXENSART` (13 capteurs), `TELRAAM_HISTORY`, `TELRAAM_TRAVAUX`, `TELRAAM_SOURCES`, chargées via `data/rixensart_data.js`.
- Par capteur : `history_periods` (nov2024, jan2025, may2025, nov2025, may2026, aug2026), `nov2024` et `recent2026` (avec `speed.avg_v85`, `speed.hourly_v85[24]`, `hourly.cars_weekday[25]`, `bikes_weekday`, `peds_weekday`, `cars_weekend`, pics matin et soir), `associated_travaux`.
- `TELRAAM_HISTORY.yoy_analysis` contient les comparaisons automne (nov 2024 / nov 2025, 10 capteurs) et printemps (mai 2025 / mai 2026, périmètre constant 9 capteurs).
- Dans l'`index.html` actuel, seuls les tableaux 1 (vitesses) et 4 (fiche d'action) sont calculés en JS. Les chiffres des tableaux 2 et 3 sont **écrits en dur** dans le HTML.
- Fonctions à reprendre telles quelles : `speedStatus`, `markerSvg`, `fmt1`, `fmtDelta`, `esc`, `initHeroFigure`, `initSpeedBars`, `initSpeedMap`, `initActionCard`, `renderStreetCard`.

## Fichiers

- Nouveau : `index.html` (remplace l'actuel, sauvegardé par git).
- Nouveau : `tools/check_aggregates.mjs` (script Node de contrôle des chiffres, sans dépendance).
- Inchangés : `data/*`, `docs/METHODOLOGIE.md`, `analyze.py`, `extract_*.py`.
- Hors périmètre : suppression des `*.bak`, `index_test.html`, `temp_inspect.html`, `debug_overflow.html` et de `generate_*.py`, seulement sur demande.

## Étape 0 : Filet de sécurité (avant de coder)

1. Écrire `tools/check_aggregates.mjs`. Il charge `data/rixensart_data.js` dans un contexte `window` simulé et exporte les agrégats de référence de l'ancienne page : V85 par rue (nov 2024), statut de vitesse, parts par mode, comparaison automne et printemps, chiffres de la fiche d'action pour les 13 rues.
2. Lister chaque chiffre écrit en dur dans les tableaux 2 et 3 de l'`index.html` actuel et le rattacher à sa source (`yoy_analysis`, `history_periods`). Tout écart entre le HTML actuel et les données est signalé à l'utilisateur, pas corrigé en silence.
3. Sauvegarder la sortie de référence dans `tools/reference_aggregates.json`.

**Validation** : le script tourne et produit un JSON stable ; la liste des écarts éventuels est remise à l'utilisateur.

## Étape 1 : Squelette scrollytelling

1. Nouveau `index.html` : `<head>` (Inter, Tailwind CDN, Leaflet, Chart.js, D3, données), variables CSS du thème sombre, en-tête « Mobilité à Rixensart · Comptages Telraam, 2024–2026 ».
2. Mise en page : colonne d'étapes (~38 %) et cadre épinglé `position: sticky; height: 100vh`, barre de progression, ancres par étape.
3. Moteur de scènes (~40 lignes) : `IntersectionObserver` sur `[data-step]`, registre `scenes[id] = { enter, leave }`, transitions d'opacité courtes. Une scène factice suffit pour tester.
4. Mobile : cadre réduit à une bande épinglée (~45 % de hauteur), cartes de texte semi-opaques en dessous. Repli statique empilé si `prefers-reduced-motion`.
5. Module `derive(data)` : agrégats calculés une fois, exposés à toutes les scènes. Bloc d'erreur « Données indisponibles » si `TELRAAM_RIXENSART` est absent.

**Validation** : à 375, 768 et 1440 px, le cadre reste épinglé, l'étape active change au scroll, aucune erreur console, texte lisible sans JS.

## Étape 2 : Scènes 0 à 3 (vitesse)

- Scène 0 : compteur animé (27 millions, 13 capteurs) et points des capteurs.
- Scène 2 : carte Leaflet en fond sombre, marqueurs `markerSvg` par statut, popup de rue (logique de `initSpeedMap` reprise).
- Scène 3 : barres V85 et limite légale, ±10 % visible (logique de `initSpeedBars`).
- Scène 1 : ridgeplot D3 24h par rue à partir de `hourly.*_weekday`. Repli : tableau des pics matin et soir si D3 est indisponible.

**Validation** : `check_aggregates.mjs` sans écart pour V85 et statuts ; capteur arrêté (Chaussée de La Hulpe) grisé avec mention « arrêté en 12/2025 ».

## Étape 3 : Scènes 4 à 6 (usagers, printemps, études de cas)

- Scène 4 : 100 pictogrammes répartis par mode, depuis les `*_pct` du réseau.
- Scène 5 : comparaison mai 2025 / mai 2026 lue **directement dans `yoy_analysis.spring`**, périmètre constant 9 capteurs. Note de méthode et lien vers `METHODOLOGIE.md`.
- Scène 6 : trois sous-étapes (Rue de la Gare, Rue du Tilleul, Av. Boulogne-Billancourt), mini-fiches chiffrées lues dans les données plutôt qu'en dur.

**Validation** : les chiffres affichés correspondent à ceux de la liste d'écarts de l'étape 0 ; l'utilisateur tranche les écarts.

## Étape 4 : Scène 7, méthode et finitions

- Scène 7 : fiche d'action pleine largeur (hors cadre épinglé), sélecteur de rue et impression en style clair (`@media print`), logique de `initActionCard` et `renderStreetCard` reprise.
- Bloc « Méthode et limites » : précision 90–95 % motorisé, 80–85 % modes actifs, définition de la V85, périmètre constant, liens vers les sources.
- Accessibilité : contrastes AA, description textuelle et tableau de données par visuel, navigation clavier entre étapes, `aria-current` sur la progression.
- Repli CDN : tableau de chiffres pour chaque scène si Leaflet, D3 ou Chart.js échouent.

**Validation** : impression d'une fiche (aperçu), navigation clavier complète, test avec réseau bloqué sur les CDN.

## Étape 5 : Vérification finale et livraison

1. `node tools/check_aggregates.mjs` : zéro écart avec la référence.
2. Contrôle visuel dans le navigateur à 375, 768 et 1440 px, en thème sombre, avec et sans `prefers-reduced-motion`.
3. Vérifier le poids de la page et le temps de première vue (< 3 s en local).
4. Mettre à jour `README.md` (structure et description) et la ligne « Prochaine étape » du design.
5. Commits par étape, au format du projet, sur `main` (choix de l'utilisateur).

## Points de décision à soumettre à l'utilisateur pendant le chantier

- Écarts éventuels entre chiffres en dur et données (étape 0).
- Suppression des anciens fichiers `*.bak`, tests et `generate_*.py` (après livraison).
- Si le scrollytelling mobile s'avère trop fragile à l'étape 1 : bascule vers un rendu empilé sur petits écrans (à valider avant de continuer).

## Estimation de risque par étape

| Étape | Risque | Pourquoi |
|---|---|---|
| 0 | Faible | Lecture et script Node |
| 1 | Moyen | Épinglage et mobile, cœur de l'approche C |
| 2 | Moyen | Ridgeplot D3 |
| 3 | Faible | Données déjà agrégées |
| 4 | Moyen | Impression et accessibilité |
| 5 | Faible | Contrôles |
