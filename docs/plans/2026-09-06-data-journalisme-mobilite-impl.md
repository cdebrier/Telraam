# Récit Data Journalisme Mobilité — Rixensart Implementation Plan

Ce plan d'implémentation détaille la refonte complète de l'application (`index.html`) pour la transformer en un récit de data journalisme épuré, percutant et grand public selon les spécifications validées dans `docs/plans/2026-09-06-data-journalisme-mobilite-design.md`.

---

## Guide d'Architecture & Choix Techniques

* **Fichier unique :** `index.html` (avec inclusion directe de `data/rixensart_data.js`).
* **Framework CSS :** Tailwind CSS CDN (Palette éditoriale presse chaude : `stone-50`, `stone-900`, vert sauge `#2E7D5B`, ambre `#D97706`, rouge brique `#C0392B`).
* **Typographie :** Google Fonts (Newsreader pour les titres et la narration éditoriale, Inter pour les chiffres et les interfaces).
* **Cartographie :** Leaflet.js avec fond épuré CartoDB Positron clair (pas de fond sombre ni de tuiles chargées).
* **Graphiques vectoriels :** Chart.js & D3.js épurés (barres horizontales, jauges de répartition modale, matrices claires, zéro canvas lourd).
* **Robustesse :** Aucun effet bloquant au scroll tactile, accessibilité mobile-first immédiate.

---

## Liste des Tâches d'Implémentation (Micro-Tâches)

- [x] **Tâche 1 : Sauvegarde & Préparation du squelette HTML5 « Grand Quotidien »**
  - **Fichiers modifiés :** `index.html`, `index.html.v2-backup.html`
  - **Détails :** 
    - Sauvegarder l'ancienne version dans `index.html.v2-backup.html`.
    - Initialiser un nouveau squelette propre avec les polices Google Fonts (Newsreader + Inter), Tailwind CSS personnalisé (palette éditoriale `stone`, vert, ambre, rouge), Leaflet.js et Chart.js.
    - Créer l'en-tête de grand quotidien : bandeau éditorial, chapeau percutant, métadonnées citoyennes (27M de passages, 13 capteurs, Rixensart).
  - **Méthode de test :** Vérifier que la page se charge sans erreur console avec un fond papier clair et une typographie éditoriale élégante.

- [x] **Tâche 2 : Implémentation du Tableau 1 — Le Pacte de la Zone 30 (Vitesse réelle V85 vs 30 km/h)**
  - **Fichiers modifiés :** `index.html`
  - **Détails :**
    - Construire le premier chapitre avec le titre de presse : *« Entre le panneau 30 et la réalité du bitume, à quelle vitesse roule-t-on vraiment chez nous ? »*.
    - Ajouter le paragraphe explicatif vulgarisant le V85 en langage citoyen.
    - Implémenter le thermomètre des vitesses : barres horizontales comparatives pour chaque rue avec ligne repère verticale nette à 30 km/h (vert sous 30, ambre entre 30 et 40, rouge au-dessus de 40).
    - Intégrer la carte communale Leaflet claire (fond Positron) coloriant les segments selon leur statut de vitesse.
  - **Méthode de test :** Vérifier le tracé des barres, l'exactitude des valeurs V85 (ex: Rue de la Gare à 44.5 km/h vs 30 km/h, Albert 1er à 62 km/h) et la réactivité mobile.

- [x] **Tâche 3 : Implémentation du Tableau 2 — Le Partage de la Chaussée (La place du vélo et le boom saisonnier)**
  - **Fichiers modifiés :** `index.html`
  - **Détails :**
    - Rédiger le récit du chapitre 2 : *« Sur 100 usagers croisés dans nos rues, combien se déplacent sans moteur ? »*.
    - Concevoir la barre de répartition modale 100 % (sur 100 personnes : proportion voitures, piétons, vélos, camions).
    - Implémenter le comparatif visuel choc **Hiver vs Printemps** : mise en scène du bond de **+194 %** du vélo aux beaux jours.
    - Identifier les corridors cyclables existants et les axes de rupture.
  - **Méthode de test :** Vérifier que les pourcentages modaux correspondent aux données réelles de `rixensart_data.js` et que le rendu est immédiat.

- [x] **Tâche 4 : Implémentation du Tableau 3 — La Zone de Danger (Le croisement Vitesse x Vélos)**
  - **Fichiers modifiés :** `index.html`
  - **Détails :**
    - Écrire le chapitre 3 : *« Où le danger est-il concentré ? Les axes où la vitesse menace les cyclistes et piétons »*.
    - Mettre en place la matrice/liste de priorité sécurité croisant la fréquentation cycliste et la vitesse V85.
    - Mettre en évidence les 3 axes prioritaires d'intervention (ex: axes de transit à forte présence de deux-roues où le V85 est excessif).
  - **Méthode de test :** Valider la logique de calcul de l'indice de vigilance et l'affichage des 3 points noirs de la commune.

- [x] **Tâche 5 : Implémentation du Tableau 4 — Le Diagnostic Citoyen & Décideurs (L'outil d'action)**
  - **Fichiers modifiés :** `index.html`
  - **Détails :**
    - Concevoir le sélecteur de rue interactif (liste déroulante et/ou clic direct sur la carte).
    - Afficher la fiche de diagnostic complète :
      - Statut (Rue apaisée / Vigilance modérée / Intervention prioritaire).
      - Indicateurs clés (V85 réel, limitation, % vélos, trafic jour).
      - Recommandations d'aménagements physiques automatiques (coussins berlinois, radars pédagogiques, pistes protégées, vélorues).
    - Ajouter le bouton d'impression/export propre en mode fiche citoyenne (`@media print` ou export CSS dédié).
  - **Méthode de test :** Sélectionner chaque rue tour à tour et vérifier que les métriques, le statut et les recommandations s'actualisent instantanément et fidèlement.

- [x] **Tâche 6 : Polissage UX, Typographie, Responsive Mobile & Vérification Finale**
  - **Fichiers modifiés :** `index.html`
  - **Détails :**
    - Vérifier l'affichage et l'ergonomie sur mobile (375px/390px) et grand écran.
    - Vérifier les contrastes WCAG AA (lisibilité parfaite des textes sur fond `stone-50`).
    - Tester l'impression/export de la fiche rue.
    - Contrôler qu'aucune erreur JS n'apparaît dans la console.
  - **Méthode de test :** Ouvrir la page dans le navigateur, tester le scroll, les clics, les filtres et valider avec un script de vérification automatisé.
