# Année glissante et profil de rue sur la carte des vitesses — Design

Statut : validé section par section avec l'utilisateur le 2026-09-29.
Suite : [plan d'implémentation](2026-09-29-annee-glissante-profil-impl.md).

## Résumé de compréhension

- **Quoi** : sur la carte des vitesses, remplacer les deux photographies (nov. 2024, fin d'été 2026) par une référence sur l'**année glissante jusqu'à la date du jour**, ajouter le **profil déclaré de la rue** dans la modale, et enrichir le parcours vertical.
- **Pourquoi** : les photographies de 14 à 30 jours sont trop courtes et sensibles aux chantiers et aux vacances. Le visiteur retrouve aussi la lecture de telraam.net.
- **Pour qui** : les habitants et les décideurs communaux de Rixensart, sur une page statique.
- **Contraintes** : page HTML unique sans build ; modale légère ; cohérence avec la méthode documentée (V85 des heures de jour, incertitude ±10 %) ; mise à jour **automatique**.
- **Hors périmètre** : données « live » ou « typique du créneau » de la carte Telraam ; appels à Telraam depuis le navigateur du visiteur.

## Constats sur l'API Telraam (vérifiés le 2026-09-29)

- `measurements-piechart` accepte des périodes de 90 jours. À 6 mois et 12 mois, il renvoie des **zéros sans erreur**. L'année doit donc être assemblée par tranches.
- `measurements-day-barchart`, `-hour-barchart-pct-up`, `-24-hour-chart`, `-speed`, `-24-hour-chart-v85`, `-24-hour-chart-direction` existent avec la même forme `segments/{id}/{début}/{fin}`.
- `segments/snapshot/traffic` (dernière heure, tous tronçons) et `segments/snapshot/typical` (typique année écoulée, **un seul créneau jour-heure**, 5 Mo) dépendent de l'heure de consultation : écartés.
- `location-profile/{id}` est une page rendue côté serveur (pas d'API) : largeur de chaussée, trottoirs, marquage, piste cyclable, sens unique, bus, stationnement, fonction, vitesse maximale, et trois ressentis du riverain (congestion, sécurité, qualité de vie).
- La page `location` limite l'intervalle à 14 jours.

## Hypothèses

1. Le trafic annuel est la somme des tranches. La V85 annuelle est une moyenne pondérée par les voitures, donc **approximative** (documentée dans la méthode).
2. La mise à jour est automatique et hebdomadaire ; la date de fin de l'année est affichée sur la page.
3. Le profil de rue est déclaratif, présenté comme tel avec sa date de récupération.
4. Le taux de fonctionnement des capteurs reste traité comme aujourd'hui.
5. Pas d'enjeu de vie privée nouveau (données publiques agrégées) ; charge négligeable.
6. L'hébergeur n'est pas choisi (le dépôt n'a ni remote ni CI).

## Design

### 1. Pipeline de données

`extract_year.py` produit `data/rixensart_year.json` : 12 tranches de 30 jours glissants par capteur, mises en cache dans `data/cache/year/{capteur}/{début}.json`. Une tranche passée est immuable ; un lancement ne recharge que la tranche en cours. Trafic par mode sommé ; V85 annuelle pondérée par les voitures. Une seconde étape lit `location-profile` de chaque capteur et enregistre le texte extrait dans `data/rixensart_profile.json` avec sa date. En cas d'échec sur un capteur ou un mois, on garde la dernière valeur, marquée « ancienne » ; plus de 3 capteurs en échec arrêtent la mise à jour. `generate_dashboard.py` fusionne les deux fichiers dans `rixensart_data.js`.

### 2. Carte et modale

Forme et couleur du marqueur = statut de vitesse sur la V85 annuelle. Un sélecteur à trois choix change le texte sous le marqueur : **Vitesse** (« 53 km/h », défaut), **Trafic** (« 4 200 véh./j »), **Mobilité active** (« 9 % »). Modale : panneau de limitation, nom et localité ; V85 annuelle en grand avec écart à la limite et repère « nov. 2024 » discret ; barre empilée fine des modes et véhicules par jour ; une ligne de profil (« Chaussée 4 m · sans piste cyclable · ligne de bus · rue de desserte », mention « déclaré par le riverain ») ; lien vers la fiche de la rue. La modale de la rue de l'Institut reste ouverte par défaut. Cas limites : capteur sans mesure = marqueur creux ; donnée ancienne = « données au [date] ».

### 3. Détail en scrollant

Le thermomètre passe à l'année glissante (limite, incertitude ±10 %, nov. 2024 en repère). Nouvelle scène courte « Ce que la rue permet » après les usagers : croisement V85 annuelle et profil (« X rues dépassent leur limite sans piste cyclable »), texte calculé depuis les données, profils « non renseigné » exclus. La fiche par rue reçoit un bloc « Profil » complet, avec les ressentis du riverain présentés comme déclaratifs, imprimable.

### 4. Automatisation, erreurs, tests

`python3 update.py` enchaîne `extract_year.py`, `generate_dashboard.py`, `node tools/check_aggregates.mjs --check` ; le fichier de données n'est remplacé que si tout réussit. Workflow GitHub Actions hebdomadaire fourni en **option**, indépendant de l'hébergeur. Profil ignoré (jamais inventé) si l'extraction ne retrouve plus les champs. Tests : agrégation annuelle sur jeux réduits ; `check_aggregates.mjs` étendu aux chiffres annuels (référence mise à jour volontairement) ; vérification visuelle des cas limites et du mobile. Documentation : approximation de la V85 annuelle et nature déclarative du profil dans `docs/METHODOLOGIE.md` ; procédure de mise à jour dans le README.

## Journal des décisions

| # | Décision | Alternatives écartées | Pourquoi |
|---|---|---|---|
| D1 | Pipeline planifié + fichier de données | Appels depuis le navigateur ; script manuel | Charge (plus de 150 appels par visite), fiabilité, besoin d'automatisme |
| D2 | Tranches de 30 jours avec cache | 4 tranches de 90 jours | Un cache par mois évite de tout recharger |
| D3 | V85 annuelle pondérée par les voitures | Recalcul depuis toutes les données horaires | Coût élevé pour un gain limité |
| D4 | Job indépendant de l'hébergeur, workflow GitHub en option | Imposer GitHub | Hébergeur non choisi |
| D5 | Forme = statut de vitesse, seul le texte change | Recolorer selon la métrique | Un marqueur = un sens |
| D6 | Sélecteur à trois métriques | Toutes à la fois | Reste léger |
| D7 | Profil déclaratif en une ligne dans la modale | Tableau complet | Modale courte |
| D8 | Thermomètre sur l'année, nov. 2024 en repère | Supprimer nov. 2024 | Garder la comparaison dans le temps |
| D9 | Une seule nouvelle scène de croisement | Plusieurs scènes | Parcours léger |
| D10 | Ressentis du riverain dans la fiche seulement | Modale ou carte | Subjectif, second plan |
| D11 | `update.py` unique, remplacement conditionnel | Étapes manuelles ; écriture progressive | Jamais de page à moitié à jour |
| D12 | Profil ignoré si l'extraction échoue | Valeurs par défaut | Ne pas inventer de données |

## Risques reconnus

- Les points d'accès Telraam ne sont pas une API officielle : plages longues à zéro silencieux, forme des pages de profil susceptible de changer. Couverts par des échecs explicites et des tests.
- V85 annuelle approximative (moyenne pondérée) : documentée.
- Profil déclaratif : présenté comme tel.
