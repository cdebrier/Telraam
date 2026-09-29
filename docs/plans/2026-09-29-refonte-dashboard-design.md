# Refonte du dashboard — Design

Date : 2026-09-29 · Statut : validé (brainstorming), implémentation non démarrée

## 1. Résumé de la compréhension

- **Quoi** : refonte visuelle et d'interaction de `index.html`. Thème sombre moderne, mêlant l'esprit de la v2 (ridgeplot 24h, cartes-chiffres) et le côté outillé de la première version (filtres, comparaisons).
- **Pourquoi** : la version actuelle (style journal papier, fond crème, serif) est jugée trop sobre. Référence d'impact visuel : https://www.karim.news.
- **Pour qui** : grand public et presse d'abord. L'exploration reste accessible mais secondaire.
- **Contenu** : tout est conservé (vitesses, usagers, effet du printemps, 3 études de cas, fiche d'action imprimable). Seule la forme change.
- **Données** : `data/rixensart_data.js` et la méthodologie (V85, iso-période, périmètre constant à 9 capteurs) restent inchangés.
- **Ton** : factuel, sans noms pompeux. Nom : « Mobilité à Rixensart », sous-titre « Comptages Telraam, 2024–2026 ».
- **Hors périmètre** : nouvelles analyses ou données, changement de méthode statistique, backend.

## 2. Hypothèses

1. Site statique sans build : HTML, Tailwind CDN, Leaflet, Chart.js, D3 en CDN limité au ridgeplot.
2. Performance : première vue interactive en moins de 3 s sur ordinateur portable.
3. Mobile de première classe. Thème sombre unique. La fiche imprimée reste claire.
4. Confidentialité : rien de nouveau (données agrégées et anonymes, sans traceurs).
5. Maintenance : un seul propriétaire, un seul fichier `index.html` lisible, sans dépendance à `generate_*.py`.
6. Parcours continu, sans bascule Récit / Labo.

## 3. Decision log

| # | Décision | Alternatives écartées | Raison |
|---|---|---|---|
| D1 | Repartir d'un mélange v2 (récit visuel) + première version (dashboard) | v2 seule, scrollytelling seul, première version seule, aucune référence | Choix explicite de l'utilisateur |
| D2 | Public prioritaire : grand public / presse | Élus et services, les deux à parité | Choix explicite de l'utilisateur ; l'outil devient secondaire |
| D3 | Tout garder, repenser la forme | Recentrer sur 2–3 visuels, ajouter du nouveau | Aucune analyse perdue ; pas de périmètre supplémentaire (YAGNI) |
| D4 | Parcours continu | Bascule Récit / Labo (v2) | Choix explicite de l'utilisateur |
| D5 | Identité simple, ton factuel | Nom éditorial ou de marque | Choix explicite de l'utilisateur |
| D6 | **Approche C : scrollytelling à visuel fixe** | A (page en scroll, recommandée par l'assistant), B (grille de cartes) | Choix de l'utilisateur, contre la recommandation. Risques (mobile, complexité) acceptés et atténués (voir §5) |
| D7 | Scrollytelling sans bibliothèque (`IntersectionObserver`, ~40 lignes) | Scrollama, GSAP ScrollTrigger | Pas de dépendance ; cohérent avec « sans bundler » |
| D8 | D3 en CDN, limité à la scène ridgeplot | Chart.js seul, canvas sur mesure | Chart.js ne rend pas bien un ridgeplot |
| D9 | Calcul unique via `derive()`, logique reprise de l'`index.html` actuel | Recalcul par scène, réécriture | Zéro écart de chiffres, moins de bugs |
| D10 | Fiche d'action hors du cadre épinglé, en pleine largeur, imprimable en clair | Fiche dans le cadre épinglé | L'impression doit fonctionner |
| D11 | Vérification par script de comparaison des agrégats plus contrôle visuel manuel | Framework de test | Le projet n'a pas d'outillage de test |
| D12 | Répartition par mode calculée sur toutes les périodes (≈ 88 % voitures, 3 % piétons, 3 % vélos, 6 % poids lourds) et libellée avec sa période | Garder 85/8/5/2 (sans source dans les données), dernière période seule (biais saisonnier) | Étape 0 : les valeurs 85/8/5/2 de la page actuelle ne correspondent à aucune période des données. Choix de l'utilisateur |
| D13 | Le +70,7 % de l'avenue de Boulogne-Billancourt est libellé « total des passages » | « Trafic motorisé » (formulation des données de chantier) | Le +70,7 % porte sur le total ; les voitures seules sont à +57,1 % |
| D14 | Scène « rues » : les 3 rues au meilleur indice de vigilance (Gare, Tilleul, Place Communale) puis Boulogne-Billancourt en « cas chantier », soit 4 sous-étapes | Garder Gare/Tilleul/Boulogne comme l'ancienne page, ou les 3 premières seulement | Étape 3 : l'ancienne page présentait Boulogne comme une priorité calculée, alors qu'elle est 4e selon l'indice de la méthodologie §6.1. Choix de l'utilisateur |
| D15 | Plusieurs étapes peuvent partager une scène (`data-focus`) ; `enter`/`leave` ne sont appelés qu'au changement de scène | Une scène par étape | Permet les sous-étapes sans recréer le visuel |
| D16 | Les chiffres des étapes et des fiches sont calculés depuis les données (rang, texte, valeurs), plus aucun chiffre en dur | Reprendre les chiffres écrits dans l'ancien HTML | Cohérence avec les données ; le classement suit les données si elles changent |
| D17 | Fiche par rue et bloc « Méthode et limites » en sections pleine largeur après le parcours, avec un segment de navigation dédié ; impression en clair (seule la fiche) | Fiche dans le cadre épinglé | L'impression et la lecture d'un formulaire exigent une page normale (D10) |
| D18 | Fiche : « passages par jour » (et non « véhicules ») ; « Pistes à étudier » avec mention « à valider par une étude locale » ; formulations adoucies (« plus exposées » au lieu de « périlleuses ») | Reprendre les textes de l'ancienne page tels quels | Ton factuel demandé ; le trafic compte aussi vélos et piétons ; les pistes sont générales, pas issues des données |
| D19 | Méthode : les seuils de couleur (2 et 5 km/h) sont présentés comme des repères de lecture, l'incertitude de ±10 % valant environ ±5 km/h à 50 km/h | Laisser entendre que les écarts sous 2 km/h sont dans la marge | Cohérence avec l'incertitude réelle |

## 4. Design

### 4.1 Architecture
- Un seul `index.html`, HTML/CSS/JS à la main et commentés.
- Desktop : colonne de texte à gauche (~38 %) avec les étapes ; cadre visuel épinglé à droite (`position: sticky`, hauteur d'écran) ; barre de progression fine.
- Un `IntersectionObserver` détecte l'étape active et appelle `scene.enter(id)`. Chaque scène est un module `{ enter(), leave() }` qui transforme le même cadre.
- Style : fond `#0B0F14`, Inter seule, chiffres en grand. Vert / ambre / rouge pour la vitesse, bleu pour le vélo.

### 4.2 Scènes

| # | Scène | Visuel | Message |
|---|---|---|---|
| 0 | Intro | Compteur animé, 13 capteurs sur carte | 27 millions de détections, 2024–2026 |
| 1 | Journée type | Ridgeplot 24h par rue (D3) | Pics de 8 h et 17 h |
| 2 | Vitesse réelle | Carte Leaflet sombre, marqueurs colorés par V85 | Dépassements de limite |
| 3 | Thermomètre des voiries | Barres V85 avec la limite légale | Classement, marge ±10 % |
| 4 | Qui passe dans nos rues | 100 pictogrammes par mode | Voiture, poids lourd, vélo, piéton |
| 5 | Effet du printemps | Mai 2025 / mai 2026, 9 capteurs constants | Hausse des modes actifs |
| 6 | Trois rues, trois histoires | Rue de la Gare, Rue du Tilleul, Av. Boulogne-Billancourt | Mini-fiche chiffrée par rue |
| 7 | Fiche d'action | Sélection d'une rue, fiche imprimable | Outil de fin de parcours |

Chaque scène affiche en pied : période, nombre de capteurs, lien vers `METHODOLOGIE.md`. Un bloc « Méthode et limites » clôt la page (précision 90–95 % motorisé, 80–85 % modes actifs).

### 4.3 Données
- `data/rixensart_data.js` est la source unique, chargée d'un bloc.
- `derive()` calcule une fois les agrégats (V85, parts par mode, séries 24h, iso-période). Les scènes ne lisent que ces agrégats.

### 4.4 Erreurs et cas limites
- Données absentes : message clair dans le cadre, texte toujours lisible.
- Capteur arrêté (ex. Chaussée de La Hulpe, 12/2025) : grisé, mention explicite, exclu des comparaisons (périmètre constant).
- Échec d'un CDN : tableau de chiffres de repli pour la scène.
- Sans JS : le texte des étapes reste visible.
- Accessibilité : contrastes AA, description textuelle et tableau de données par visuel, navigation clavier.

### 4.5 Tests
- Script de comparaison des agrégats avec l'`index.html` actuel : zéro écart attendu.
- Contrôle visuel à 375, 768 et 1440 px.
- Test d'impression de la fiche d'action.
- Test avec `prefers-reduced-motion`.

## 5. Risques

| Risque | Atténuation |
|---|---|
| Scrollytelling fragile sur mobile | Visuel réduit à une bande épinglée (~45 % de hauteur) ; repli statique empilé avec `prefers-reduced-motion` |
| Complexité de l'approche C (l'ancien générateur pesait 151 Ko) | Scènes modulaires `{ enter, leave }`, sans bibliothèque, un seul fichier |
| Ridgeplot D3 lourd à écrire | Limité à une scène ; tableau de repli |
| Régression des chiffres | Script de comparaison des agrégats |
| Modifications non commitées en cours | Les commiter avant de démarrer |

## 6. Statut
Implémenté en 6 étapes (voir [le plan](2026-09-29-refonte-dashboard-impl.md)). Écarts avec ce design : pas de Tailwind ni de Chart.js (CSS écrit à la main, D3 et Leaflet seuls) ; breakpoint à deux colonnes à 720 px ; scène « rues » à 4 sous-étapes (D14) ; fiche et méthode en sections pleines largeur (D17).
