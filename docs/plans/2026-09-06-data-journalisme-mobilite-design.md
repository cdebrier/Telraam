# Document de Conception : Récit Data Journalisme Mobilité — Rixensart

**Date :** 6 septembre 2026  
**Projet :** Observatoire Citoyen de la Mobilité — Commune de Rixensart  
**Inspiration éditoriale :** *Le Monde (Les Décodeurs)*, *The Financial Times Data*, *The Pudding*, *Karim Douieb*.  
**Statut :** En attente de validation

---

## 1. Contexte & Thèse Éditoriale

### Contexte
La commune de Rixensart dispose d'un historique de plus de **27 millions de détections** issues de 13 capteurs citoyens Telraam S2. 
Les dashboards analytiques classiques ou les visualisations trop chargées (particules en mouvement, thèmes sombres néon, diagrammes complexes) rendent la lecture confuse pour le grand public et ne permettent pas aux élus d'en tirer un plan d'action rapide.

### L'Angle Majeur
> **« La promesse d'une commune apaisée et cyclable à l'épreuve de la vitesse réelle. »**

Le récit confronte deux réalités quotidiennes :
1. **L'essor des mobilités douces** : les habitants veulent marcher et rouler à vélo (explosion de +194 % des vélos aux beaux jours).
2. **Le respect des limites de vitesse** : la Zone 30 est-elle une réalité protectrice ou un vœu pieux sur le terrain ?
3. **Le point de bascule** : identifier précisément les axes où la vitesse automobile met en danger les usagers vulnérables pour guider les investissements d'aménagement.

### Publics Cibles & Double Niveau de Lecture
* **Niveau 1 — Grand Public & Familles (2 minutes de lecture sur smartphone)** : Un récit visuel limpide, sans jargon technique, articulé autour de repères humains concrets.
* **Niveau 2 — Élus, Services Travaux & Comités de Quartier** : Un outil de diagnostic objectif rue par rue délivrant des recommandations d'aménagements physiques ciblés et des fiches d'action imprimables.

---

## 2. Identité Visuelle & Principes Graphiques (« Style Grand Quotidien »)

* **Fond & Atmosphère :** Fond papier journal lumineux et chaleureux (`bg-stone-50` / `#FBFBFA`), texte principal en gris anthracite profond (`text-stone-900` / `#1C1917`), bordures fines discrètes (`border-stone-200`).
* **Typographie :**
  - *Titres & Chapitres :* Police avec empattement éditoriale de grand quotidien (ex. **Newsreader** ou **Playfair Display** / serif noble).
  - *Données & Corps de texte :* **Inter** ou **Source Sans** pour une lisibilité parfaite des chiffres et des étiquettes.
* **Palette Sémantique Naturelle :**
  - **Vert Sauge / Apaisé (`#2E7D5B`)** : Rues respectant la Zone 30 (< 30 km/h), mobilités actives.
  - **Ambre / Vigilance (`#D97706`)** : Vitesse intermédiaire (30-40 km/h), mixité délicate.
  - **Terre Cuite / Rouge Alerte (`#C0392B`)** : Vitesse V85 excessive (> 40 km/h), points noirs de sécurité.
  - **Bleu Encre (`#1E3A8A`)** : Voitures & repères institutionnels.
* **Épure Radicale :** Suppression totale des particules en Canvas, des effets de flou néon et des visualisations à lecture difficile (ridgeplots). Rendu SVG et vectoriel net, instantané et fluide sur tout appareil.

---

## 3. Découpage du Récit en 4 Tableaux d'Impact

Le récit adopte un format hybride combinant un **scrollytelling continu** et des **tableaux visuels autonomes** : chaque section pose une question, apporte sa preuve graphique et se conclut par une synthèse claire.

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Le Pacte de la Zone 30 (Vitesse réelle V85 vs 30 km/h)   │
├─────────────────────────────────────────────────────────────┤
│ 2. Le Partage de la Chaussée (La part du vélo & le boom)    │
├─────────────────────────────────────────────────────────────┤
│ 3. La Zone de Danger (Le croisement Vitesse x Vélos)        │
├─────────────────────────────────────────────────────────────┤
│ 4. Le Diagnostic d'Action Rue par Rue (Fiche & Aménagements)│
└─────────────────────────────────────────────────────────────┘
```

---

### Tableau 1 : La Zone 30 est-elle respectée ? (Le thermomètre des vitesses)
* **Question éditoriale :** *« Entre le panneau 30 et la réalité du bitume, à quelle vitesse roule-t-on vraiment chez nous ? »*
* **Visualisation :**
  - Carte du territoire épurée avec coloration des axes selon la vitesse réelle V85 constatée.
  - Classement direct en barres horizontales claires : chaque rue a sa barre de vitesse face à une ligne verticale rouge très visible marquant **30 km/h**.
  - Mise en exergue du contraste : la Place Communale apaisée (21 km/h) vs les axes où le V85 dépasse les 42 km/h.
* **Explication citoyenne :** Définition immédiate du V85 : *« La vitesse sous laquelle roulent 85 % des conducteurs. C’est l’indicateur officiel qui reflète la vitesse réelle de la rue. »*

---

### Tableau 2 : Qui a droit de cité ? (La place des vélos et des piétons)
* **Question éditoriale :** *« Sur 100 usagers croisés dans nos rues, combien se déplacent sans moteur ? »*
* **Visualisation :**
  - Graphique de répartition modale concret (jauge 100 % ou matrice d'icônes) : proportion de voitures, de piétons, de vélos et de poids lourds.
  - Comparatif choc **Hiver vs Printemps** : visualisation du bond de **+194 %** du trafic cyclable dès les beaux jours, montrant l'énorme potentiel bridé par la météo et l'infrastructure.
  - Identification des corridors de mobilité douce (axes menant aux gares et aux écoles).

---

### Tableau 3 : Le croisement critique (Où le danger est-il concentré ?)
* **Question éditoriale :** *« Quelles sont les rues prioritaires où la vitesse menace directement les cyclistes et les enfants ? »*
* **Visualisation :**
  - Matrice visuelle de vigilance croisant **Vitesse réelle** et **Fréquentation cycliste/piétonne**.
  - Mise en évidence immédiate des **3 axes à sécuriser d'urgence** (rues très empruntées par les vélos mais où les voitures roulent trop vite).
  - Élimination des débats d'opinion : la priorité d'investissement public est établie sur base de données physiques indiscutables.

---

### Tableau 4 : Le Diagnostic Citoyen & Décideurs (L'outil d'action)
* **Fonctionnalité :** Un sélecteur interactif permettant de choisir n'importe quel capteur / rue de la commune.
* **Contenu de la fiche rue :**
  1. **Indicateur de statut clair :** Badge visuel (*« Rue apaisée »*, *« Vigilance modérée »*, ou *« Action prioritaire requise »*).
  2. **Indicateurs clés :** V85 réel, écart à la limitation, part modale (vélos / marcheurs), volume journalier moyen.
  3. **Moteur de Recommandations d'Aménagement :**
     - Si excès de vitesse avéré : suggestion d'aménagements physiques (chicanes végétalisées, coussins berlinois, radars pédagogiques ciblés).
     - Si flux cyclable important non protégé : recommandation de bande cyclable suggérée ou piste protégée.
     - Si rue exemplaire (< 25 km/h) : proposition de valorisation en vélorue ou zone de rencontre (Zone 20).
  4. **Action immédiate :** Bouton *« Imprimer / Exporter la fiche de ma rue »* générant une page de synthèse épurée, idéale pour interpeller le collège communal ou appuyer un dossier de quartier.

---

## 4. Architecture Technique & Performance

* **Fichier unique optimisé (`index.html`)** :
  - Zéro dépendance à des bundlers lourds.
  - Utilisation de Tailwind CSS (CDN avec palette éditoriale personnalisée).
  - Rendu cartographique via **Leaflet** avec fond de carte sobre clair (CartoDB Positron / OSM épuré).
  - Graphiques vectoriels nets avec **Chart.js** ou **D3.js** sans surcharge de calcul.
* **Compatibilité Mobile Totale** :
  - Prise en charge parfaite des écrans smartphones (iPhone, Android) avec typographie dimensionnée pour la lecture tactile.
  - Pas de canvas bloquant le défilement au doigt.

---

## 5. Prochaines Étapes
1. **Validation de ce document de conception par l'utilisateur.**
2. **Transition vers la phase de planification (skill `planning`)** pour formaliser la feuille de route d'implémentation.
3. **Mise en œuvre du code.**
