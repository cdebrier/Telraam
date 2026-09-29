# Observatoire Mobilité Telraam (Scrollytelling & Visual Storytelling D3.js) Implementation Plan

Ce plan détaille l'implémentation progressive, étape par étape, de l'expérience de data-journalisme et de scrollytelling D3.js inspirée de **Karim Douieb** (*Brussels — A lovely melting-pot*, *Land doesn't vote, people do*) et **Aaron Williams** (*Washington Post*), intégrant une narration en 5 actes suivie d'un laboratoire citoyen d'exploration libre.

---

## Architecture des Fichiers & Composants

- **Fichier principal :** [`index.html`](file:///Users/charlesdebrier/Development/Telraam/index.html)
- **Données consolidées :** [`data/rixensart_data.js`](file:///Users/charlesdebrier/Development/Telraam/data/rixensart_data.js) (capteurs, géométries, chantiers, historique 2 ans, sources)
- **Sauvegarde de sécurité :** [`index.html.bak`](file:///Users/charlesdebrier/Development/Telraam/index.html.bak)

---

## Découpage des Tâches d'Exécution

### Tâche 1 : Mise en place du socle D3.js & Moteur Scrollytelling
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - Intégration de la bibliothèque **D3.js v7** (`<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>`).
  - Mise en place du conteneur scrollytelling en deux panneaux :
    - Panneau graphique fixe (*Sticky visual viewport*, `position: sticky; top: 0; height: 100vh`) composé d'un `<canvas>` haute performance superposé à un calque `<svg>`.
    - Colonne narrative défilante composée de cartes d'étapes (`.step` avec `min-height: 85vh` et style *glassmorphism*).
  - Implémentation du moteur d'intersection (`IntersectionObserver` haute précision) qui détecte l'entrée, la progression et la sortie de chaque étape (`data-step="1"` à `data-step="5"`).
  - Ajout du bouton d'en-tête et flottant *« Passer directement à l'explorateur »*.
- **Méthode de test :**
  - Vérifier au défilement que chaque carte déclenche l'événement console correspondant sans saccade.

---

### Tâche 2 : Moteur Géographique & Particulaire D3 (Canvas + SVG)
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - Définition d'une projection D3 locale Mercator ajustée aux coordonnées de la commune (`lat: 50.716, lon: 4.525`) adaptée à la taille du canvas.
  - Tracé vectoriel SVG net des voiries équipées et des limites communales à partir des coordonnées de `window.TELRAAM_RIXENSART`.
  - Initialisation d'une boucle d'animation particulaire D3 (`d3.timer` / `requestAnimationFrame`) générant 2 000 à 4 000 points lumineux circulant de manière fluide le long des axes selon les volumes réels.
  - Attachement des couleurs modales identitaires :
    - Bleu Telraam (`#3E9CBA`) : Voitures
    - Émeraude (`#10B981`) : Vélos
    - Corail (`#F2845C`) : Piétons
    - Pourpre (`#8B5CF6`) : Poids lourds
- **Méthode de test :**
  - Vérifier que les particules s'animent de manière fluide (60 fps) le long des tracés réels des rues.

---

### Tâche 3 : Acte 1 — Le souffle communal (Des bulles vers le territoire)
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - **État A (Haut de page)** : Les 27 000 points sont rassemblés au centre de l'écran en 4 bulles compactes représentant les volumes totaux cumulés sur 2 ans.
  - **Transition D3 (Morphing à la Karim Douieb)** : Au défilement vers la première carte narrative, application d'une force d'attraction (`d3.forceSimulation` avec interpolation) qui disperse les points et les fait atterrir précisément sur chaque rue selon sa fréquentation réelle.
  - Révélation du volume quotidien communal moyen (32 000 véh./jour).
- **Méthode de test :**
  - Vérifier l'effet de transition fluide entre la vue en bulles abstraites et la carte territoriale lors du scroll.

---

### Tâche 4 : Acte 2 — Le paradoxe du ressenti (*Ce qui se voit vs Ce qui ne se voit pas*)
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - **Transition Caméra & Zoom D3** :
    - Zoom ciblé sur le quartier de l'Avenue Royale fermée pour 200 jours : mise en surbrillance rouge/orange intense du flux dévié sur l'Avenue de Boulogne-Billancourt (+70.7%) et la Rue de la Gare (+58.9%).
    - Glissement vers la Place Communale de Genval : réduction spectaculaire de la densité de points et coloration vert apaisé illustrant l'évaporation du trafic en Zone 20 (-66.9%).
  - Cartes explicatives synchronisées mettant en contraste *Ce qui se voit* (goulets de déviation saturés) et *Ce qui ne se voit pas* (apaisement diffus des quartiers résidentiels).
- **Méthode de test :**
  - Vérifier que le zoom cartographique et la modification d'intensité des particules réagissent immédiatement au passage de l'étape.

---

### Tâche 5 : Acte 3 — La pulsation saisonnière & l'essor du vélo
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - Animation de l'effet saisonnier : multiplication dynamique par 3 des points émeraude (vélos) et corail (piétons) pour simuler le passage de l'hiver au printemps (+194%).
  - Convergence visuelle des flux actifs vers le pôle multimodal de la nouvelle gare RER de Rixensart inaugurée fin nov. 2024.
- **Méthode de test :**
  - Vérifier l'apparition progressive et la convergence des particules cyclistes vers la gare.

---

### Tâche 6 : Acte 4 — La vitesse sous la loupe (Zones 30 vs V85 réel)
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - Transition morphologique des tracés en un graphique comparatif D3 interactif :
    - Chaque rue devient une ligne horizontale avec repère de vitesse limite légale (30 ou 50 km/h) et barre animée du V85 réel (vitesse sous laquelle roulent 85% des usagers).
    - Mise en valeur des rues modèles (Place Communale 21 km/h, École de Rosières 31 km/h) et des axes de vigilance.
- **Méthode de test :**
  - Vérifier l'alignement et la clarté des jauges comparatives V85.

---

### Tâche 7 : Acte 5 — Le Laboratoire Citoyen d'Exploration Libre
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - Déploiement du module interactif complet une fois le récit achevé (ou sur clic du bouton d'accès direct) :
    - **Curseur interactif 24h** : permet à l'utilisateur de glisser d'heure en heure (0h à 23h) pour observer la commune respirer et voir les pointes de 8h et 17h.
    - **Sélection tactile/clic de rue** : panneau latéral ou tiroir mobile détaillant le capteur sélectionné (part modale, vitesses, chantiers associés).
    - **Filtres par quartier** : Rixensart, Genval, Rosières.
    - **Boutons de téléchargement direct** : CSV et JSON.
    - **Cadre méthodologique & Répertoire des 5 sources citées**.
- **Méthode de test :**
  - Tester l'interaction avec le slider 24h et la mise à jour instantanée des flux et de la fiche détaillée.

---

### Tâche 8 : Optimisation Mobile-First, Performance & Finitions
- **Fichiers modifiés :** `index.html`
- **Détails de l'implémentation :**
  - Optimisation tactile sur écran mobile :
    - Visualiseur D3 épinglé en haut (environ 42vh) avec cartes de texte défilant doucement au pouce en dessous.
    - Cibles tactiles $\ge 48\text{ px}$.
    - Ajustement automatique de la densité de particules sur mobile (1 500 particules max) pour préserver la batterie et garantir 60 fps constants.
  - Gestion du redimensionnement dynamique de fenêtre (`window.onresize`) pour adapter les échelles D3.
- **Méthode de test :**
  - Vérifier sur émulateur mobile (375px à 430px) la fluidité du scroll et l'absence de débordement horizontal.
