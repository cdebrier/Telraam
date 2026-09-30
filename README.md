# Observatoire Citoyen de la Mobilité — Commune de Rixensart

Ce projet est un observatoire citoyen et un outil d'aide à la décision basé sur les données de comptage multimodal et de vitesse des capteurs **Telraam S2** installés chez les riverains de la commune de **Rixensart** (Rixensart, Genval, Rosières).

La page présente près de **27 millions de détections** enregistrées entre 2024 et 2026 sous forme de parcours défilant (scrollytelling) : profils horaires, vitesses V85 par rue, répartition par mode, effet des saisons, études de cas, une section sur les chantiers, une carte de l'évolution date par date (écart de chaque rue à la tendance communale), puis une fiche imprimable par rue.

---

## 📚 Documentation & Méthodologie

Le cadre scientifique, matériel, cinématique et statistique complet est consigné dans le document dédié :

👉 **[Consulter le Cadre Méthodologique Détaillé (`docs/METHODOLOGIE.md`)](docs/METHODOLOGIE.md)**

Ce document détaille :
1. **L'architecture matérielle et la vision Edge AI** (processeur neuronal Hailo-8, conformité RGPD intégrale).
2. **Le traitement de la photopériode et la règle jour/nuit** (flux diurne classifié vs phares nocturnes).
3. **Le calcul de la vitesse V85** (définition mathématique du percentile 85, incertitude standard de ±10 %, seuils de risque).
4. **L'analyse temporelle pluriannuelle sans biais** (méthode iso-période et périmètre constant à 9 capteurs neutralisant les arrêts de capteurs).
5. **La matrice de vigilance sécurité** croisant vitesse réelle et usagers vulnérables.
6. **La corrélation avec les chantiers communaux** et la théorie de l'évaporation du trafic (*Disappearing Traffic*).
7. **L'arbre de décision d'aménagements physiques** (coussins berlinois, radars pédagogiques, vélorues, zones de rencontre).
8. **Le référentiel exhaustif des sources institutionnelles et académiques** (Telraam, WeCount, SPW Mobilité, VIAS, Cerema, SNCB, etc.).

---

## 🗂️ Structure du Projet

```text
├── index.html                           # Page unique : parcours scrollytelling, chantiers, carte d'évolution, fiche par rue, méthode
├── README.md                            # Présentation générale du projet
├── docs/
│   ├── METHODOLOGIE.md                  # Référentiel méthodologique et scientifique complet
│   └── plans/                           # Design, journal des décisions et plan d'implémentation de la refonte
├── data/
│   ├── rixensart_data.js                # Données consolidées pour l'interface web (capteurs, historique, travaux)
│   ├── rixensart_summary.json           # Synthèse JSON des compteurs et métriques clés
│   ├── rixensart_summary.csv            # Synthèse tabulaire CSV
│   ├── rixensart_history.json           # Séries temporelles pluriannuelles (2024-2026)
│   ├── rixensart_telraam_full_data.json # Données brutes issues de l'API Telraam
│   └── rixensart_travaux.json           # Registre des chantiers et arrêtés de police communaux
├── tools/
│   ├── check_aggregates.mjs             # Recoupe les chiffres avec la référence (node tools/check_aggregates.mjs --check)
│   └── reference_aggregates.json        # Chiffres de référence (V85, statuts, comparaisons saisonnières)
├── update.py                            # Met à jour année glissante + profils, régénère les données, contrôle les chiffres
├── extract_year.py                      # Année glissante par capteur (4 tranches de 91 jours)
├── extract_profile.py                   # Profil déclaré de chaque rue (telraam.net/en/location-profile)
├── tests/                               # Tests unitaires de l'agrégation annuelle et de l'analyse des profils
├── .github/workflows/update.yml         # Option : mise à jour hebdomadaire sur GitHub Actions
├── generate_dashboard.py                # Consolide les données brutes en data/rixensart_data.js, rixensart_summary.json et l'historique
├── extract_data.py                      # Extraction des métadonnées et segments via l'API Telraam
├── extract_history.py                   # Extraction des séries temporelles historiques
└── analyze.py                           # Traitement statistique et calcul des indicateurs de synthèse
```

---

## 🔄 Mise à jour des données

```bash
python3 update.py
```

Récupère l'année glissante (environ 5 minutes, appels en parallèle) et les profils de rue, régénère `data/rixensart_data.js` et vérifie les chiffres. Si une étape échoue, les fichiers de données reviennent à leur état précédent. Pour une exécution hebdomadaire automatique, planifier cette commande (`cron`, ou le workflow `.github/workflows/update.yml` si le dépôt est sur GitHub). Tests : `python3 -m unittest tests.test_year`.

## 🚀 Utilisation Locale

Pour lancer l'application en local :

```bash
# Avec Python 3
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000` dans un navigateur moderne.
La page est un fichier HTML unique, sans étape de build. Elle charge Leaflet (carte) et D3 (ridgeplot) depuis un CDN ; si l'un des deux manque, la scène concernée se replie sur un tableau. Le fond de carte est le « Canvas Dark Gray » d'Esri (gratuit, sans clé, zoom maximal 16, données © OpenStreetMap).

Pour vérifier que les chiffres n'ont pas bougé après une modification des données ou du calcul :

```bash
node tools/check_aggregates.mjs --check
```
