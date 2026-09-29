# Vue « Évolution dans le temps » — Plan d'implémentation

Référence : [design validé](2026-09-29-evolution-carte-design.md) (décisions D1–D10).
Principe : chaque étape laisse un `index.html` fonctionnel et commitable. On avance en tranches verticales.

## Constats préalables (vérifiés dans le code)

- Données : `window.TELRAAM_HISTORY.sensors_history[]` (10 capteurs), chacun avec `periods{nov2024, jan2025, may2025, nov2025, may2026, aug2026}.total`. `TELRAAM_HISTORY.periods[]` donne clé, libellé, début, fin et saison de chaque date.
- Coordonnées : `TELRAAM_RIXENSART[]` (`id`, `street`, `lat`, `lon`). Rapprochement par `id`.
- Chantiers : `TELRAAM_TRAVAUX[]` avec `period.start`, `period.end`, `detour_polyline` ou `work_zone_polyline`, et `impacted_sensors[].sensor_id`.
- La carte de la scène 2 (`index.html`, autour de la ligne 845) donne le modèle à suivre : fond Esri sombre, panneau `labels`, `divIcon` avec `markerSvg`. À reprendre, pas à recopier : la création du fond de carte est à extraire dans une petite fonction commune.
- Le moteur de scènes du parcours (`initStory`) ne sert pas ici : la section est autonome, initialisée avec `initFiche` et `initSources`.
- Fonctions réutilisables : `esc`, `fmt0`, `fmt1`, `fmtDelta`. À vérifier avant usage : `markerSvg` est propre au statut de vitesse, il ne convient pas au point coloré.
- `tools/check_aggregates.mjs` charge `data/rixensart_data.js` dans un contexte `vm`. On l'étend sans nouvelle dépendance.

## Fichiers

- Modifié : `index.html` (nouvelle section, styles, scripts).
- Modifié : `tools/check_aggregates.mjs` (contrôle de `buildTimeline`).
- Nouveau : `tools/reference_timeline.json` (écarts de référence, § 4.1 du design).
- Modifié : `README.md` (une ligne), `docs/METHODOLOGIE.md` (paragraphe sur l'écart à la tendance).
- Inchangés : `data/*`, `generate_dashboard.py`, `extract_*.py`.

## Étape 0 : Filet de sécurité

1. Encadrer le futur code de calcul dans `index.html` par deux commentaires repères (`// <timeline>` et `// </timeline>`) pour que le script Node puisse l'évaluer sans dupliquer la fonction.
2. Créer `tools/reference_timeline.json` avec le tableau du § 4.1 du design (10 rues × 6 dates, `null` pour La Hulpe après nov. 2025) et la médiane communale (100, 104, 143, 79, 129, 120).
3. Étendre `check_aggregates.mjs` : extraire le bloc repéré, l'évaluer dans le contexte `vm`, comparer `buildTimeline` à la référence (tolérance ±1 point) avec les options `--check` et `--write` existantes.

**Validation** : `node tools/check_aggregates.mjs --check` échoue tant que `buildTimeline` n'existe pas, puis passe une fois l'étape 1 faite. Les anciens contrôles restent verts.

## Étape 1 : Calcul des écarts (`buildTimeline`)

1. Écrire `buildTimeline(H)` entre les repères : indice = total ÷ total de nov. 2024 ; tendance = médiane des indices présents à la date (valeurs nulles ou à zéro exclues) ; écart = indice ÷ tendance − 1.
2. Renvoyer, par rue, `values[6]` (écart en % ou `null`), `suspect[6]` (écart supérieur à +100 % sur une date isolée) et `trend[6]`. Renvoyer aussi les dates et libellés lus dans `H.periods`.
3. Ne pas modifier `derive()`. `buildTimeline` reste indépendante.

**Validation** : `--check` passe. Cas vérifiés à la main : Boulogne-Billancourt à +172 % en mai 2026, Place Communale marquée suspecte en mai 2025, La Hulpe à `null` en mai 2026.

## Étape 2 : Section, carte et points colorés

1. Ajouter la section `#evolution` après `#chantiers` : kicker, titre, phrase d'introduction (coïncidence dans le temps, 0 = comme la commune), zone carte, légende, contrôles.
2. Extraire une fonction `makeBaseMap(el, opts)` (fond Esri, panneau `labels`) utilisée par la scène 2 et la nouvelle carte. Vérifier que la scène 2 est inchangée visuellement.
3. Marqueurs `divIcon` : un cercle de taille fixe, couleur d'une échelle divergente bornée à ±50 %, contour en pointillé si suspect, absent si `null`. Palette lisible sur fond sombre et pour le daltonisme (bleu ↔ orange, pas rouge ↔ vert).
4. Légende : dégradé de l'échelle avec « −50 % », « 0 = comme la commune » et « +50 % ou plus ».
5. Lancer l'initialisation seulement quand la section approche de l'écran (`IntersectionObserver`), avec `invalidateSize()` à l'affichage.

**Validation** : à 375, 768 et 1440 px, la carte s'affiche, les 10 points ont la bonne couleur pour la date par défaut (mai 2026), aucune erreur console.

## Étape 3 : Curseur et état `date`

1. État minimal `{ date }` (index 0 à 5). Curseur `<input type="range">` à 6 crans avec étiquettes de dates, boutons précédent et suivant.
2. Lecture automatique : avance toutes les 1,8 s, s'arrête à la dernière date, désactivée si `prefers-reduced-motion`.
3. Clavier : flèches gauche et droite quand le curseur a le focus, Tab pour parcourir les points.
4. Titre de la date courante (« Mai 2026 · printemps ») mis à jour à chaque changement.

**Validation** : les 6 dates s'enchaînent, la lecture s'arrête, le clavier fonctionne, `prefers-reduced-motion` désactive la lecture.

## Étape 4 : Sparklines

1. Écrire `sparkSvg(values, upTo, opts)` : SVG d'environ 60 × 24 px, tracé jusqu'à `upTo`, point plein final, dates futures grisées, trait de référence à 0.
2. Intégrer la sparkline et la valeur (« +172 % ») à côté de chaque point, avec décalage réglé par capteur (à droite, à gauche ou au-dessus) pour éviter les chevauchements, notamment Roosevelt / Rue Haute et Albert 1er / Tasnière.
3. Échelle verticale commune à toutes les sparklines (−60 % à +180 %, avec écrêtage marqué), pour qu'elles soient comparables.
4. Mobile (< 768 px) : les sparklines sont masquées sauf celle du point sélectionné, affichée dans une carte en bas de la zone.

**Validation** : les sparklines se prolongent d'une date à l'autre, restent lisibles à 1440 et 768 px, et sur mobile une seule est visible.

## Étape 5 : Chantiers sur la carte

1. À chaque date, sélectionner les chantiers dont la période contient la date (début et fin du mois de mesure) et qui ont au moins un capteur associé.
2. Tracer leur déviation en trait fin (`detour_polyline`, à défaut `work_zone_polyline`), légèrement estompé, avec un bandeau sous le titre : nom du chantier et période.
3. Ne rien tracer s'il n'y a pas de chantier actif à la date.

**Validation** : en mai 2026 la déviation de l'Avenue Royale est visible avec son bandeau ; en nov. 2024 seuls les chantiers actifs à cette date apparaissent (rue de Rosières, gare, E411).

## Étape 6 : Accessibilité et repli

1. Tableau des écarts (10 rues × 6 dates) présent dans le DOM, masqué visuellement, avec la date courante annoncée dans une zone `aria-live="polite"`.
2. Chaque marqueur porte un `aria-label` (« Boulogne-Billancourt, mai 2026 : 172 % au-dessus de la tendance communale »).
3. Repli sans Leaflet : la carte disparaît, le tableau devient visible.
4. Ajouter la section aux règles d'impression (masquée, comme `.chantiers`).

**Validation** : navigation complète au clavier ; le tableau s'affiche si Leaflet est bloqué (test en coupant le réseau vers le CDN).

## Étape 7 : Textes, méthode et cohérence

1. Phrase de méthode sous la carte : nov. 2024 comme référence, médiane des rues présentes, 0 = comme la commune, mesures suspectes signalées, coïncidence dans le temps.
2. Dans la section « Chantiers », ajouter un lien vers `#evolution`.
3. Sur la carte « Place Communale » du parcours, ajouter une note renvoyant à la vue (le −67 % mai à mai s'explique en grande partie par un mai 2025 anormal).
4. Mettre à jour `README.md` (une ligne) et `docs/METHODOLOGIE.md` (calcul de l'écart à la tendance communale et ses limites).

**Validation** : relecture des textes, les liens internes fonctionnent, `node tools/check_aggregates.mjs --check` est vert.

## Étape 8 : Vérification finale

1. Vérification visuelle à 375, 768 et 1440 px, mode clair et sombre du navigateur, avec et sans Leaflet, au clavier.
2. Vérifier que les scènes existantes n'ont pas changé (surtout la carte de la scène 2, modifiée à l'étape 2).
3. Contrôler l'absence d'erreur console et le poids de la page.

## Ordre de commit proposé

1. `chore: Add timeline check to the aggregate script` (étape 0).
2. `feat(dashboard): Compute deviations from the communal trend` (étape 1).
3. `feat(dashboard): Add the evolution map with a date slider` (étapes 2 et 3).
4. `feat(dashboard): Add sparklines and roadworks to the evolution map` (étapes 4 et 5).
5. `feat(dashboard): Make the evolution view accessible and document it` (étapes 6 et 7).

## Risques et points d'attention

- Le refactor de `makeBaseMap` touche la scène 2 : vérifier qu'elle reste identique avant de continuer.
- Les tracés de déviation sont longs (des centaines de points pour l'Avenue Royale) : simplifier au chargement si le rendu ralentit.
- Chevauchements de sparklines : si le réglage manuel ne suffit pas, envisager l'évitement de collisions (approche 3 du design), sans l'anticiper.
- Ne pas laisser la vue affirmer une cause : le bandeau de chantier reste descriptif.
