# Document de Conception : Les Ondes Urbaines (Ridge Plot / Joyplot 24h) pour l'Observatoire Telraam

**Date :** 5 septembre 2026  
**Projet :** Observatoire Mobilité Telraam — Commune de Rixensart  
**Sujet :** Remplacement de l'affichage cartographique des flux par une visualisation en **Ondes Urbaines (Ridge Plot / Joyplot 24h)** dans le récit visuel D3.js.  
**Inspiration :** Data-art scientifique (*Joyplot / Ridge Plot* popularisé par *The Pudding*, *Observable* et l'imagerie pulsar), combiné à la narration éditoriale de Karim Douieb.

---

## 1. Contexte & Problématique

### Le constat d'échec de la carte géographique brute :
Dans une commune périurbaine comme Rixensart, 13 capteurs disposés sur une carte géographique laissent de très grands vides territoriaux entre les rues. L'affichage de lignes ou de particules sur des tronçons isolés donne une impression de fragmentation ("13 segments coupés les uns des autres") et ne permet pas d'embrasser d'un seul coup d'œil **l'intensité des flux, les écarts de volume et le rythme de vie de la commune**.

### L'opportunité des « Ondes Urbaines » :
Les données de Telraam fournissent pour chaque rue le profil horaire précis sur 24 heures (`carsWeekdays`, `bikeWeekdays`, `pedestrianWeekdays`). La visualisation en **Ridge Plot** (courbes de densité superposées en cascade) transforme ces données temporelles en une **sculpture graphique vivante** :
- Les 13 voiries sont étagées verticalement, de l'axe le plus fréquenté au plus apaisé.
- L'axe horizontal représente les 24 heures de la journée (0h à 24h).
- L'amplitude des vagues illustre de manière spectaculaire le réveil matinal (7h-9h), le plateau de midi, la grande vague du retour du soir (16h-19h) et le calme nocturne.
- Le contraste entre voiries saturées (hautes crêtes acérées) et voiries apaisées (vagues douces et plates) devient visuellement fulgurant.

---

## 2. Architecture Visuelle & Scénographie D3.js

Le visualiseur D3.js fixé (*sticky viewport*) affiche désormais les **13 Ondes Urbaines** à la place de la carte géographique :

### A. Anatomie Graphique d'une Onde
1. **Tracé de courbe D3** : Courbe lissée par interpolation monotone (`d3.curveMonotoneX` ou `d3.curveBasis`) garantissant une fluidité organique sans angle dur.
2. **Dégradé lumineux (*Gradient Fill*)** :
   - Fond sombre ardoise (`#0f172a`).
   - Remplissage translucide sous la crête avec gradient lumineux :
     - Bleu nuit (`#1e293b`) aux heures creuses.
     - Cyan électrique (`#38bdf8`) en journée.
     - Ambre ardent / Rougeoyant (`#f59e0b` $\rightarrow$ `#ef4444`) au sommet des crêtes de pointe (7h-9h et 16h-18h).
     - Vert émeraude (`#10b981`) pour les voiries résidentielles et le mode vélo.
3. **Ligne de crête lumineuse (*Stroke Glow*)** : Ligne supérieure fine et brillante avec léger halo lumineux (effet néon délicat).
4. **Étiquettes typographiques intégrées** : Nom de la rue, quartier et volume journalier moyen alignés élégamment à gauche de chaque crête en Montserrat.

---

### B. Dynamique Narrative au Fil du Scrollytelling

Le Ridge Plot réagit aux étapes du récit :

| Étape narrative | Comportement visuel des Ondes Urbaines |
| :--- | :--- |
| **Acte 1 : Le souffle communal** | Les 13 ondes s'animent en cascade de bas en haut. Les crêtes imposantes des 4 grands axes (Franklin Roosevelt 7,5k, Albert 1er 6,4k, La Hulpe 5,6k, Haute 4,9k) dominent visuellement le paysage, révélant la concentration du trafic. |
| **Acte 2 : Le paradoxe du ressenti** | **Surbrillance de l'Avenue de Boulogne-Billancourt** : Sa crête s'élève brutalement de +71% et vire au rouge vif pour matérialiser la surcharge de la déviation de l'Avenue Royale fermée. |
| **Acte 2 (suite) : L'apaisement en Zone 20** | **Focus sur la Place Communale de Genval** : Sa courbe s'affaisse pour devenir une vague basse, douce et vert émeraude (-67%), illustrant concrètement l'évaporation du transit. |
| **Acte 3 : L'essor du vélo** | Les courbes motorisées s'estompent pour laisser place aux **Ondes Vélos** : Les crêtes vélos explosent au printemps (+194%), formant deux pics caractéristiques à 8h et 17h convergeant vers la gare. |
| **Acte 4 : V85 & Vitesse** | Des marqueurs de vitesse V85 apparaissent au sommet des vagues de chaque rue, comparant la vitesse réelle observée à la limitation légale. |

---

### C. Interaction Directe (Au survol ou glissement tactile)
- **Ligne temporelle verticale interactive** : En glissant le doigt ou la souris sur le Ridge Plot, un repère temporel vertical parcourt les 24h et affiche instantanément le volume précis à cette heure pour toutes les rues simultanément.
- **Basculeur de mode** : Boutons rapides pour afficher le profil *Tous véhicules*, *Voitures*, *Vélos* ou *Piétons*.

---

## 3. Rôle de la Carte Géographique

- La carte géographique Leaflet **n'est pas supprimée**, mais elle est replacée là où elle est la plus utile et pertinente : **dans le Laboratoire Citoyen (au bas du récit)**.
- Ainsi, le visiteur bénéficie d'abord de la puissance esthétique et explicative des **Ondes Urbaines** pour comprendre l'histoire, puis retrouve la **carte géographique classique** pour situer son domicile, explorer les travaux et faire ses recherches locales.

---

## 4. Données et Transformations Requises

Aucune donnée nouvelle n'est requise. Les données horaires existent déjà dans `data/rixensart_data.js` :
- `sensor.nov2024.hourly.cars_weekday` (tableau de 24 valeurs horaires)
- `sensor.nov2024.hourly.bikes_weekday` (tableau de 24 valeurs horaires)
- `sensor.nov2024.hourly.peds_weekday` (tableau de 24 valeurs horaires)
- `sensor.nov2024.hourly.cars_weekend` (pour la comparaison week-end)

D3.js se chargera de normaliser ces 24 points sur l'axe X (0 à 24) et de calculer l'échelle verticale Y décalée pour chacune des 13 couches.

---

## 5. Prochaines Étapes
1. Validation du présent document de conception par l'utilisateur.
2. Décomposition en plan d'implémentation (compétence `planning`).
3. Implémentation du moteur D3 Ridge Plot dans `index.html`.
