# Observatoire Citoyen de la Mobilité — Commune de Rixensart

Ce projet est un observatoire citoyen et un outil d'aide à la décision basé sur les données de comptage multimodal et de vitesse des capteurs **Telraam S2** installés chez les riverains de la commune de **Rixensart** (Rixensart, Genval, Rosières).

La page présente près de **27 millions de détections** enregistrées entre 2024 et 2026 sous forme de parcours défilant (scrollytelling) : profils horaires, vitesses V85 par rue, répartition par mode, effet des saisons, études de cas, puis une fiche imprimable par rue.

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
├── index.html                           # Page unique : parcours scrollytelling, fiche par rue, méthode
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
├── extract_data.py                      # Extraction des métadonnées et segments via l'API Telraam
├── extract_history.py                   # Extraction des séries temporelles historiques
└── analyze.py                           # Traitement statistique et calcul des indicateurs de synthèse
```

---

## 🚀 Utilisation Locale

Pour lancer l'application en local :

```bash
# Avec Python 3
python3 -m http.server 8000
```

Puis ouvrir `http://localhost:8000` dans un navigateur moderne.
La page est un fichier HTML unique, sans étape de build. Elle charge Leaflet (carte) et D3 (ridgeplot) depuis un CDN ; si l'un des deux manque, la scène concernée se replie sur un tableau. Le fond de carte vient d'OpenStreetMap.

Pour vérifier que les chiffres n'ont pas bougé après une modification des données ou du calcul :

```bash
node tools/check_aggregates.mjs --check
```
