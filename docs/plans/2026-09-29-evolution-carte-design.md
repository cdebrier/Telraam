# Vue « Évolution dans le temps » — Design

Date : 2026-09-29 · Statut : validé (brainstorming), implémentation non démarrée

## 1. Résumé de la compréhension

- **Quoi** : une scène cartographique avec un curseur sur les 6 dates de mesure (nov. 2024, janv. 2025, mai 2025, nov. 2025, mai 2026, août 2026). Chaque capteur est un point dont la couleur donne son écart à la tendance communale. Une sparkline placée à côté du point se prolonge à chaque nouvelle date. La déviation du chantier actif à la date courante s'allume sur la carte.
- **Pourquoi** : rendre visible le lien entre chantiers et hausses ou baisses locales, sans que la saison brouille le message (en mai presque toutes les rues montent, en novembre elles baissent).
- **Pour qui** : habitants, élus et presse qui lisent la page ; les personnes qui veulent contrôler les chiffres passent par le tableau équivalent.
- **Mesure** : écart de la rue à la médiane communale, nov. 2024 = 0. La valeur 0 signifie « comme la commune ».
- **Hors périmètre** : séries quotidiennes (les données n'en contiennent pas), nouvelle collecte, affirmation de causalité. Même logique que la section « Chantiers à garder en tête » : coïncidence dans le temps.

## 2. Hypothèses

1. **Tendance communale** : médiane des indices des rues présentes à la date (robuste aux extrêmes comme Boulogne-Billancourt).
2. **Référence** : nov. 2024, seule date où les 10 capteurs sont présents. Indice de chaque rue = total du mois ÷ total de nov. 2024.
3. **Chaussée de La Hulpe** : disparaît après nov. 2025 (pas de valeur, jamais comptée comme une baisse), règle déjà appliquée dans la page.
4. **Mesures suspectes** : un écart supérieur à +100 % sur une date isolée (Place Communale en mai 2025, +134 %) est tracé avec un contour en pointillé et une mention « à prendre avec prudence », sans être corrigé.
5. **Technique** : Leaflet et D3 déjà chargés, pas de build ni de dépendance nouvelle, données lues depuis `TELRAAM_HISTORY` et `TELRAAM_TRAVAUX`, calcul fait au chargement (aucun fichier de données modifié).
6. **Performance** : 10 capteurs et 6 dates, rendu instantané. Première vue non bloquante si la scène est hors écran.
7. **Confidentialité** : rien de nouveau (données agrégées et anonymes).
8. **Maintenance** : un seul propriétaire, code dans `index.html` dans le style existant.
9. **Accessibilité** : tableau équivalent pour les lecteurs d'écran, navigation au clavier, `prefers-reduced-motion` respecté.

## 3. Décision log

| # | Décision | Alternatives écartées | Raison |
|---|---|---|---|
| D1 | Vue principale : carte avec curseur temporel | Petites courbes seules, graphique unique en spaghetti | Rend visible le report géographique ; le spaghetti est illisible avec 6 points |
| D2 | Ajouter une sparkline à côté de chaque point, qui se prolonge avec les dates | Panneau latéral de courbes | Demande explicite de l'utilisateur |
| D3 | Mesure = écart à la tendance communale à chaque date | Variation à la même saison un an plus tôt ; variation brute depuis la première mesure | La saison n'est plus un biais ; l'iso-période ne couvre que 2 dates sur 6 ; le brut est biaisé |
| D4 | Tendance = médiane | Moyenne pondérée | Robuste aux valeurs extrêmes (Boulogne-Billancourt) |
| D5 | Marqueurs Leaflet `divIcon` avec sparkline SVG intégrée | Panneau latéral ; calque D3 avec évitement de collisions | Le plus simple, suit le zoom ; l'évitement de collisions reste en réserve si des chevauchements gênent |
| D6 | Mobile : sparkline du seul capteur sélectionné, dans une carte en bas | Toutes les sparklines | Lisibilité sur petit écran |
| D7 | Section autonome après « Chantiers à garder en tête » | Scène dans le parcours défilant | Avancement au curseur, indépendant du défilement |
| D8 | Chantiers affichés seulement s'ils sont actifs à la date et associés à un capteur | Tous les chantiers | Carte lisible |
| D9 | Échelle divergente centrée sur 0, bornée à ±50 %, valeur exacte au-delà | Échelle non bornée | Éviter que Boulogne sature toute la palette |
| D10 | Corriger d'abord la section « Chantiers » | Corriger avec l'implémentation | L'écart entre le texte et les données était déjà publié (commit `c68df5f`) |

## 4. Conception

### 4.1 Données

`buildTimeline(H)` (fonction pure) prend `TELRAAM_HISTORY` et renvoie, pour chaque rue, 6 écarts à la médiane communale (`null` si le capteur est absent) et un drapeau « suspect » par date. Aucun fichier de données n'est ajouté.

Valeurs de référence calculées à la main (écart en %, nov. 2024 = 0) :

| Rue | nov. 24 | janv. 25 | mai 25 | nov. 25 | mai 26 | août 26 |
|---|---|---|---|---|---|---|
| Rue de Genval | 0 | +59 | +16 | −25 | +67 | +33 |
| Chaussée de La Hulpe | 0 | +26 | +7 | −2 | – | – |
| Avenue Franklin Roosevelt | 0 | −5 | −4 | +13 | 0 | +2 |
| Rue de l'Institut | 0 | −8 | −6 | −4 | +18 | +11 |
| Rue de la Tasnière | 0 | −25 | +2 | +1 | −16 | −27 |
| Rue Haute | 0 | +4 | −2 | +16 | −9 | −15 |
| Place Communale | 0 | 0 | +134 | −1 | −15 | −26 |
| Avenue Albert 1er | 0 | 0 | −9 | +13 | −4 | −9 |
| Av. de Boulogne-Billancourt | 0 | +6 | +43 | +73 | +172 | +127 |
| Rue de la Gare | 0 | −18 | −20 | −13 | +41 | 0 |

Médiane communale (indice, nov. 2024 = 100) : 100, 104, 143, 79, 129, 120.

### 4.2 Interface

- **Ordinateur** : carte pleine largeur. Au-dessus, la date courante et sa saison. Sous la carte, un curseur à 6 crans avec précédent, suivant et lecture.
- **Point** : cercle de taille fixe, coloré selon l'écart. La taille n'encode rien.
- **Sparkline** : 60 × 24 px environ à côté du point, tracée jusqu'à la date courante, point plein final et valeur numérique (par exemple « +172 % »). Dates futures grisées, sans tracé.
- **Chantiers** : le tracé de déviation du chantier actif s'allume en trait fin, un bandeau donne son nom et sa période (« Avenue Royale fermée depuis le 16 février »).
- **Mobile** : seul le capteur touché affiche sa sparkline, dans une carte fixée en bas de l'écran. Les autres restent des points colorés.
- **Mesures suspectes** : contour en pointillé, mention dans l'infobulle.
- **Clavier** : flèches gauche et droite pour changer de date, Tab pour parcourir les capteurs.

### 4.3 Structure technique

- `buildTimeline(H)` : calcul des écarts et des drapeaux.
- `sparkSvg(values, upTo)` : SVG d'une sparkline jusqu'à la date courante, sans bibliothèque.
- Scène `evolution` : section HTML autonome avec sa propre carte Leaflet, des `divIcon` et un état minimal `{ date }`.
- Contrôles : curseur, boutons et lecture automatique ne changent que `date`. Chaque changement met à jour les marqueurs, le bandeau de chantier et le tableau d'accessibilité.
- Flux : `TELRAAM_HISTORY` → `buildTimeline` → `{date}` → marqueurs, sparklines, déviations (lues dans `TELRAAM_TRAVAUX` selon la période du chantier) et bandeau.

### 4.4 Erreurs et cas limites

- Leaflet indisponible : la scène se replie sur le tableau des écarts par rue et par date, comme les autres scènes.
- Capteur sans donnée à une date : pas de point, la sparkline s'arrête.
- Lecture automatique : s'arrête sur la dernière date, désactivée avec `prefers-reduced-motion`.
- Médiane calculée sur moins de 5 capteurs : message d'avertissement (aucune date concernée aujourd'hui).
- Écart supérieur à ±50 % : couleur plafonnée, valeur exacte affichée.

### 4.5 Tests

- Étendre `tools/check_aggregates.mjs` pour contrôler `buildTimeline` contre le tableau du § 4.1 (par exemple Boulogne-Billancourt à +172 % en mai 2026).
- Vérification visuelle sur ordinateur, tablette et mobile, au clavier et sans Leaflet.

## 5. Risques

- **Lecture causale** : une carte animée peut suggérer une cause. Le bandeau de chantier et une phrase de méthode répètent qu'il s'agit d'une coïncidence dans le temps.
- **Base de référence** : nov. 2024 est unique et peut être atypique. La méthode le dit et le tableau montre les valeurs.
- **Chevauchements** : les paires Roosevelt / Rue Haute et Albert 1er / Tasnière sont proches. Si le placement manuel ne suffit pas, on passera à un calque avec évitement de collisions (approche écartée pour l'instant).
- **Cohérence avec le reste de la page** : la carte « Place Communale » du parcours affiche toujours le −67 % mai à mai. Ajouter une note renvoyant à cette vue.
