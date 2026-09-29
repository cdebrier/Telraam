# Ondes Urbaines (Ridge Plot 24h D3.js) Implementation Plan

Ce plan détaille l'implémentation de la visualisation des **Ondes Urbaines (Ridge Plot / Joyplot 24h)** dans le visualiseur scrollytelling D3 de l'Observatoire Telraam Rixensart, remplaçant l'affichage cartographique par une fresque temporelle des 13 rues.

---

## 1. Architecture des Fichiers & Composants
- **Fichier principal :** [`index.html`](file:///Users/charlesdebrier/Development/Telraam/index.html)
- **Données sources :** `data/rixensart_data.js` (profils 24h `carsWeekdays`, `bikeWeekdays`, `pedestrianWeekdays`)
- **Sauvegarde :** `index.html.bak`

---

## 2. Découpage en Micro-Tâches Exécutables

### Tâche 1 : Préparation & Normalisation des Données 24h
- **Fichiers :** `index.html`
- **Détails :**
  - Ordonnancement des 13 capteurs par volume décroissant :
    1. Av. Franklin Roosevelt (7 538 véh./j)
    2. Av. Albert 1er (6 424)
    3. Chaussée de La Hulpe (5 673)
    4. Rue Haute (4 939)
    5. Rue de l'Institut (2 674)
    6. Rue de la Gare (2 172)
    7. Rue de la Tasnière (1 958)
    8. Rue de Genval (1 427)
    9. Place Communale (1 389)
    10. Av. de Boulogne-Billancourt (1 323)
    11. Rue du Tilleul (673)
    12. Rue Mahiermont (672)
    13. Rue des Bergères (École Rosières)
  - Construction des tableaux 24h pour chaque mode (`cars`, `bikes`, `peds`, `total`) avec extrapolation douce pour les heures de nuit.
- **Vérification :** Contrôle en console que les 13 séries contiennent 24 points cohérents.

---

### Tâche 2 : Moteur Graphique D3 Ridge Plot (Échelles & Générateurs d'Aires)
- **Fichiers :** `index.html`
- **Détails :**
  - Définition des échelles D3 :
    - Échelle X (`xScale`) : linéaire de 0 à 23 heures, mappée sur la largeur utile du visualiseur.
    - Échelle Y d'étagement (`yScale`) : bande ordonnée répartissant les 13 couches verticalement avec un chevauchement élégant (*overlap factor* de 1.8 à 2.2).
    - Échelle d'amplitude locale (`zScale`) : hauteur maximale de chaque crête en pixels selon le volume horaire.
  - Générateur d'aire D3 (`d3.area()`) et de ligne de crête (`d3.line()`) avec lissage monotone (`d3.curveMonotoneX`) pour des courbes soyeuses.
- **Vérification :** Les 13 vagues se dessinent nettement dans le visualiseur sans déborder du conteneur.

---

### Tâche 3 : Esthétique & Gradients Lumineux (Style Karim Douieb / Data-Art)
- **Fichiers :** `index.html`
- **Détails :**
  - Définition des dégradés SVG (`<defs>`) :
    - Dégradé standard : bleu nuit en base $\rightarrow$ cyan électrique (`#38bdf8`) $\rightarrow$ ambre lumineux au sommet (`#fbbf24`).
    - Dégradé d'alerte / déviation : ambre en base $\rightarrow$ rouge flamboyant (`#ef4444`) au sommet.
    - Dégradé apaisé / vélo : vert sapin en base $\rightarrow$ vert émeraude éclatant (`#10b981`) au sommet.
  - Trait de crête lumineux supérieur (*stroke*) avec halo subtil (`stroke-width: 2px`).
  - Colonne d'étiquettes typographiques à gauche : Nom de la rue en Montserrat gras (`text-xs`), statut, et volume journalier.
  - Axe temporel horizontal inférieur : repères à 0h, 4h, 8h (Pointe), 12h, 17h (Pointe), 20h, 23h.
- **Vérification :** Le rendu graphique est immersif, très lisible et raffiné sur fond sombre.

---

### Tâche 4 : Synchronisation Scrollytelling Dynamique
- **Fichiers :** `index.html`
- **Détails :**
  - Interconnexion avec l'`IntersectionObserver` des cartes narratives :
    - **Étape 0/1 (Le souffle communal)** : Les 13 ondes se déploient en cascade animée de bas en haut ; les crêtes des 4 axes majeurs ressortent avec force.
    - **Étape 2 (Le paradoxe du ressenti)** : La crête de l'Avenue de Boulogne-Billancourt s'élève de +71% et s'illumine en rouge ardent (`#ef4444`) pour matérialiser la surcharge de la déviation.
    - **Étape 3 (L'apaisement en Zone 20)** : La courbe de la Place Communale s'affaisse en une onde basse et douce vert émeraude (-67%).
    - **Étape 4 (L'essor du vélo)** : Les courbes motorisées s'effacent doucement pour laisser place aux courbes de flux cyclistes (+194% au printemps), avec les deux pics marqués de 8h et 17h.
    - **Étape 5 (La vitesse au microscope)** : Des repères de vitesse V85 apparaissent à l'apex de chaque crête.
- **Vérification :** Faire défiler les cartes et observer les métamorphoses fluides et instantanées des ondes.

---

### Tâche 5 : Interactivité Directe & Ligne Temporelle Tactile
- **Fichiers :** `index.html`
- **Détails :**
  - Ajout d'une ligne de visée verticale interactive qui suit le pointeur de la souris ou le doigt sur mobile.
  - Affichage instantané d'une infobulle flottante indiquant pour l'heure survolée :
    *« 08h15 • Pointe du matin : 850 autos/h sur Av. Roosevelt, 120 vélos/h sur Rue de la Gare »*.
  - Mini-boutons de sélection du mode de transport dans le visualiseur (*Tous*, *Autos*, *Vélos*).
- **Vérification :** Tester le glissement tactile sur mobile et le survol sur grand écran.

---

### Tâche 6 : Vérification Globale & Finitions
- **Fichiers :** `index.html`
- **Détails :**
  - Vérification de la syntaxe JavaScript avec Node.js.
  - Vérification du bon fonctionnement continu du Laboratoire Citoyen (carte Leaflet, 4 graphiques, tableau) en dessous du récit.
  - Vérification de l'affichage mobile (375px à 430px) : étiquettes raccourcies si besoin et hauteur de crête adaptée.
- **Vérification :** Zéro erreur console, défilement impeccable.
