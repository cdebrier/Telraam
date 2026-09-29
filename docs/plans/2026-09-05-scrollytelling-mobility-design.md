# Document de Conception : Observatoire Mobilité Telraam en Récit Visuel Immersif (Scrollytelling D3.js)

**Date :** 5 septembre 2026  
**Projet :** Observatoire Mobilité Telraam — Commune de Rixensart  
**Inspiration de référence :** Karim Douieb (*Brussels — A lovely melting-pot*, *Land doesn't vote, people do*), Aaron Williams (*America is more diverse than ever — but still segregated*, Washington Post).  

---

## 1. Contexte & Objectifs

La commune de Rixensart dispose d'un jeu de données exceptionnel de plus de **27 millions de passages** collectés sur 2 ans par les capteurs citoyens Telraam S2. Si les tableaux de bord classiques (*dashboards*) permettent de consulter des métriques, ils échouent souvent à expliquer **la dynamique humaine et physique des flux** à un public citoyen ou à des élus non spécialistes.

### Objectifs majeurs :
1. **Raconter une histoire visuelle percutante (*Data Storytelling*)** : Transformer la statistique en une expérience narrative où le lecteur comprend intuitivement les flux, les déviations et l'impact des aménagements.
2. **Expliquer le paradoxe du ressenti** : Démontrer visuellement pourquoi les usagers ressentent une saturation alors même que le volume communal global diminue (-3.8% à -13.6%).
3. **Harmonie Récit + Explorateur** : Offrir une narration scénarisée en 4 actes visuels D3.js se concluant sur un « Laboratoire Citoyen » permettant l'exploration libre de chaque rue.
4. **Ergonomie Mobile-First** : Assurer une consultation fluide et tactile à une main sur smartphone (iPhone / Android) comme sur grand écran.
5. **Autonomie Technique** : Maintenir une architecture web moderne légère sans dépendance à un serveur de build complexe.

---

## 2. Architecture Technique & Choix Technologiques

Le projet sera développé sous forme d'une **application web moderne autonome** :

* **D3.js (v7)** :
  - **Moteur Graphique Hybride Canvas / SVG** :
    - *HTML5 Canvas* pour le rendu fluide à 60 fps des nuages de points et des flux particulaires en mouvement (jusqu'à 5 000 particules sans ralentissement sur mobile).
    - *SVG* pour les tracés vectoriels nets des voiries communales, les polygones des chantiers, les contours de quartiers et les étiquettes typographiques.
  - **Transitions D3 & Force Simulation** :
    - Algorithme de morphing animant le passage des bulles de répartition globale vers les coordonnées géographiques réelles des rues.
  - **Projections cartographiques locales** :
    - Projection Mercator ou transverse centrée sur les coordonnées de Rixensart / Genval / Rosières (`lat: 50.716, lon: 4.525`).

* **Moteur de Scrollytelling (Scrollama.js / IntersectionObserver)** :
  - Détection précise des étapes narratives au fil du défilement du lecteur.
  - Déclenchement d'événements de transition D3 sans saccade (`step-enter`, `step-progress`).

* **Tailwind CSS & Typographie** :
  - Typographie éditoriale : **Montserrat** (titres audacieux, micro-capitales) + **Inter** (corps de texte).
  - Cartes narratives en verre dépoli (*glassmorphism* : `backdrop-blur-md bg-white/90 border border-slate-200/80`).

* **Données existantes** :
  - Exploitation directe de `data/rixensart_data.js` contenant les 13 capteurs, l'historique 2 ans, les chantiers et les sources officielles.

---

## 3. Scénario de l'Histoire en 5 Actes

### **Acte 1 : Le souffle communal (De l'abstrait au territoire)**
* **Narration** : Introduction à l'observatoire citoyen. *« Chaque jour, des dizaines de milliers de trajectoires sillonnent Rixensart, Genval et Rosières... »*
* **Animation D3** :
  - Des milliers de points lumineux colorés flottent et forment 4 grandes bulles de répartition modale (Bleu = Voitures, Émeraude = Vélos, Corail = Piétons, Pourpre = Poids lourds).
  - Au défilement, ces bulles s'ouvrent et les particules viennent s'aimanter sur les tracés géographiques exacts des rues de la commune.

### **Acte 2 : Le paradoxe du ressenti (*Ce qui se voit vs Ce qui ne se voit pas*)**
* **Narration** : Décryptage de l'engorgement ressenti face à la décrue statistique.
* **Animation D3** :
  - La caméra effectue un zoom sur le secteur de l'**Avenue Royale fermée pour 200 jours** : un flux continu et dense de particules s'engouffre dans l'**Avenue de Boulogne-Billancourt**, qui s'illumine en rouge d'alerte (+71% de report).
  - La caméra glisse ensuite vers le centre de Genval et la **Place Communale** : les particules ralentissent, s'espacent et virent au vert apaisé (-67% de transit grâce à la Zone 20). Le contraste entre concentration et apaisement devient évident.

### **Acte 3 : La pulsation saisonnière & l'essor des vélos**
* **Narration** : Comment la météo et les infrastructures transforment les habitudes de déplacement.
* **Animation D3** :
  - Simulation du passage de l'hiver au printemps : les points vélos et piétons triplent de volume (+194%), formant des flux continus convergeant vers le nouveau pôle multimodal de la gare RER de Rixensart.

### **Acte 4 : La vitesse sous la loupe (Zones 30 vs Vitesse réelle V85)**
* **Narration** : Analyse objective de la vitesse pratiquée par 85% des usagers.
* **Animation D3** :
  - Les tracés des rues se transforment temporairement en jauges de vitesse horizontales alignées, mettant en évidence les voiries apaisées (Place Communale à 21 km/h) et les zones de vigilance où le V85 dépasse la limitation.

### **Acte 5 : Le Laboratoire Citoyen (Mode Exploration Libre)**
* **Narration** : Transition vers l'autonomie du lecteur.
* **Interface déployée** :
  - Carte interactive vivante avec **curseur horaire 24h** pour observer le trafic respirer d'heure en heure (pointes du matin et du soir).
  - Sélection interactive de n'importe quel capteur pour afficher sa fiche analytique complète.
  - Filtres par quartier (Genval, Rixensart, Rosières) et téléchargement des données brutes (CSV, JSON).
  - Rappel du cadre méthodologique et des sources institutionnelles.

---

## 4. Ergonomie Responsive & Mobile-First

* **Sur Desktop** :
  - Mise en page scrollytelling en deux colonnes : à gauche, les cartes de texte défilent tranquillement ; à droite, le panneau visuel D3 reste fixé en plein écran (*sticky*).
  - Accès direct : Un bouton discret *« Accéder directement à l'explorateur »* permet de court-circuiter le récit si besoin.

* **Sur Mobile / Smartphone** :
  - Le canvas visuel D3 occupe la moitié supérieure ou l'arrière-plan complet.
  - Les cartes textuelles défilent verticalement au doigt avec une opacité étudiée pour ne jamais masquer complètement la dynamique visuelle.
  - Cibles tactiles $\ge 48\text{ px}$ et contrôles intuitifs au pouce.

---

## 5. Prochaines Étapes
1. Validation du présent document de conception par l'utilisateur.
2. Transition vers la phase de **planification technique détaillée** (découpage micro-tâches : mise en place de D3.js Canvas, implémentation des 5 étapes scrollytelling, développement du laboratoire explorateur).
