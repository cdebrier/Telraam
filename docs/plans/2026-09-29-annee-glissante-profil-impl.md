# Année glissante et profil de rue — Plan d'implémentation

Référence : [design validé](2026-09-29-annee-glissante-profil-design.md) (décisions D1–D12).
Principe : chaque étape laisse une page fonctionnelle et commitable. Tranches verticales, données d'abord, interface ensuite.

## Constats préalables

- `extract_history.py` appelle déjà `measurements-piechart/segments/{id}/{début}/{fin}` (sans clé) sur 6 périodes fixes. `generate_dashboard.py` consolide vers `data/rixensart_data.js`, `rixensart_summary.json/.csv` et `rixensart_history.json`.
- La V85 actuelle de la page est la moyenne des heures de jour (`speed.avg_v85`, `speed.hourly_v85[24]`). Pour rester cohérent, la V85 annuelle doit suivre la même règle jour/nuit.
- `tools/check_aggregates.mjs` charge les données dans un contexte simulé et compare à `tools/reference_aggregates.json` (`--write`, `--check`).
- Le dépôt n'a ni remote ni CI. Les chemins absolus (`/Users/charlesdebrier/...`) sont codés en dur dans les scripts Python : à rendre relatifs dans les fichiers touchés.
- Les 13 capteurs : 10 officiels (`SENSORS`) et 3 supplémentaires (`EXTRA_SENSORS`) dans `extract_data.py`.

## Fichiers

- Nouveaux : `extract_year.py`, `extract_profile.py`, `update.py`, `tests/test_year.py` (+ jeux de données réduits), `data/rixensart_year.json`, `data/rixensart_profile.json`, `data/cache/year/` (ignoré par git si volumineux, à décider à l'étape 1), `.github/workflows/update.yml` (option).
- Modifiés : `generate_dashboard.py`, `index.html`, `tools/check_aggregates.mjs`, `tools/reference_aggregates.json`, `docs/METHODOLOGIE.md`, `README.md`.

## Étape 0 : Vérifier les hypothèses (avant de coder)

1. **V85 annuelle** : vérifier que `measurements-24-hour-chart-v85` et `measurements-24-hour-chart` acceptent une tranche de 30 jours (`segments/{id}/{début}/{fin}`) et donnent V85 et voitures par heure. Comparer le résultat sur nov. 2024 avec `speed.avg_v85` déjà en base : l'écart doit rester négligeable. Sinon, revoir D3 avec l'utilisateur.
2. **Profil** : inspecter le HTML de `location-profile/{id}` pour les 13 capteurs (via `curl`, sans navigateur) : le texte est-il présent dans la réponse serveur ? Lister les libellés et les variantes (« No idea », « No separate lanes »). Sortir une liste des champs et de leurs valeurs possibles.
3. **Taux de fonctionnement** : relever comment les totaux actuels traitent les heures sans données, pour appliquer la même règle à l'année.

**Validation** : note de 10 lignes des écarts constatés, remise à l'utilisateur avant l'étape 1.

## Étape 1 : Extraction de l'année glissante

1. `extract_year.py` : pour chaque capteur, 12 tranches de 30 jours se terminant la veille du lancement. Par tranche : piechart, V85 par heure, voitures par heure. Retries et pause entre appels comme dans `extract_history.py`.
2. Cache : `data/cache/year/{id}/{début}.json`, écrit seulement pour les tranches terminées. Une tranche en cours est toujours rechargée.
3. Agrégation dans `rixensart_year.json` : `end_date`, par capteur `{ modes (piétons, vélos, voitures, poids lourds, nuit), per_day, v85 (jour, pondérée voitures), coverage (nombre de tranches valides), stale }`.
4. Gestion d'erreur : dernière valeur connue + `stale: true` ; échec de plus de 3 capteurs = code de sortie non nul.
5. `tests/test_year.py` : sommes, pondération, cas d'une tranche manquante, cas d'un capteur sans mesure, sur jeux réduits.

**Validation** : les tests passent ; un second lancement ne fait que ~13 appels ; les valeurs de la rue de l'Institut sont plausibles face à celles de `telraam.net`.

## Étape 2 : Extraction du profil de rue

1. `extract_profile.py` : lit `location-profile/{id}`, extrait les champs listés à l'étape 0, écrit `rixensart_profile.json` avec `fetched_at`. Champ absent ou « No idea » = `null`.
2. Si les libellés attendus ne sont pas retrouvés, le capteur est ignoré avec un avertissement (D12).
3. Test : sur une page HTML enregistrée en fixture, extraction correcte ; sur une page tronquée, résultat `null` sans exception.

**Validation** : profil obtenu pour les 13 capteurs ; la rue de la Gare donne 4 m, trottoirs 1,5 m, sans piste cyclable, bus, desserte locale, 30 km/h.

## Étape 3 : Fusion dans les données de la page

1. `generate_dashboard.py` : lire `rixensart_year.json` et `rixensart_profile.json`, ajouter `year` et `profile` à chaque capteur dans `rixensart_data.js`, exposer `year.end_date`. Remplacer les chemins absolus par des chemins relatifs au fichier.
2. Le contenu existant (`nov2024`, `recent2026`, historique) reste inchangé.
3. `tools/check_aggregates.mjs` : ajouter les agrégats annuels (V85 annuelle, statut, trafic par jour, part de mobilité active) ; régénérer la référence avec `--write` **après relecture** des valeurs.

**Validation** : `node tools/check_aggregates.mjs --check` passe ; aucun chiffre existant ne change.

## Étape 4 : Carte, marqueurs et modale

1. Statut de vitesse (forme et couleur) calculé sur `year.v85`, repli sur nov. 2024 si absent (marqueur « ancienne » si `stale`).
2. Sélecteur à trois choix (Vitesse, Trafic, Mobilité active) au-dessus de la carte : change uniquement le texte sous le marqueur ; accessible au clavier, `aria-pressed`.
3. Modale : panneau de limitation, V85 annuelle en grand + écart, repère « nov. 2024 », barre empilée des modes et véhicules par jour, ligne de profil (« déclaré par le riverain »), lien vers la fiche. « Données au [date] » si `stale`.
4. Légende et note de la scène mises à jour : « V85 année glissante jusqu'au [date] ».
5. La modale de la rue de l'Institut reste ouverte à l'entrée de la scène (comportement actuel conservé).

**Validation** (navigateur, 375, 768, 1440 px) : trois modes du sélecteur, capteur sans mesure, donnée ancienne, profil non renseigné ; aucune erreur console.

## Étape 5 : Parcours vertical

1. Thermomètre : barres sur la V85 annuelle, limite et incertitude ±10 %, nov. 2024 en repère discret.
2. Nouvelle scène « Ce que la rue permet » après les usagers : croisement V85 annuelle × profil, texte calculé depuis les données (profils « non renseigné » exclus), avec la liste des rues concernées.
3. Fiche par rue : bloc « Profil » complet (voirie, équipements, ressentis du riverain présentés comme déclaratifs), inclus dans l'impression.
4. Vérifier les textes calculés existants qui citent nov. 2024 ou « fin d'été 2026 » et les aligner.

**Validation** : parcours complet sans erreur ; impression de la fiche correcte.

## Étape 6 : Automatisation

1. `update.py` : enchaîne `extract_year.py`, `extract_profile.py`, `generate_dashboard.py`, `node tools/check_aggregates.mjs --check`. Écriture des fichiers finaux seulement si tout réussit (fichiers temporaires puis renommage).
2. `.github/workflows/update.yml` (option, livré désactivé ou documenté) : job hebdomadaire, lance `update.py`, commite les données modifiées, échoue si l'un des contrôles échoue.
3. Contrôle : un écart de la référence après mise à jour n'écrase pas la référence ; il fait échouer le job pour relecture humaine.

**Validation** : `python3 update.py` de bout en bout ; échec simulé (coupure réseau, page de profil modifiée) : l'ancienne version reste en place.

## Étape 7 : Documentation

1. `docs/METHODOLOGIE.md` : définition de l'année glissante, agrégation en tranches, **approximation de la V85 annuelle**, nature déclarative du profil, limites de l'API Telraam (plages longues à zéro silencieux).
2. `README.md` : structure du projet mise à jour, procédure `python3 update.py`, option d'automatisation.

## Risques et parades

| Risque | Parade |
|---|---|
| Telraam change ses points d'accès ou ses pages | Échecs explicites, valeurs « ancienne », tests sur fixtures |
| V85 annuelle trop éloignée de la V85 de référence | Vérifiée à l'étape 0 ; retour à l'utilisateur avant d'aller plus loin |
| Cache volumineux dans git | Décision à l'étape 1 (ignorer `data/cache/` ou le versionner) |
| Chemins absolus dans les scripts | Passés en relatif dans les fichiers modifiés |

## Ordre et jalons

Étape 0 → 1 → 2 → 3 (données prêtes, testées) → 4 → 5 (interface) → 6 → 7. Chaque étape est commitée séparément (`feat(data)`, `feat(dashboard)`, `docs`).
