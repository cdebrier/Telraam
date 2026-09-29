# Observatoire Citoyen de la Mobilité — Commune de Rixensart

Ce projet est un observatoire citoyen et un outil d'aide à la décision basé sur les données de comptage multimodal et de vitesse des capteurs **Telraam S2** installés chez les riverains de la commune de **Rixensart** (Rixensart, Genval, Rosières).

L'enquête interactive met en perspective plus de **27 millions de détections** enregistrées entre 2024 et 2026 pour évaluer l'apaisement réel du trafic, le respect de la Zone 30, l'essor des mobilités douces et l'impact des chantiers de voirie.

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
├── index.html                           # Application web principale (Récit data-journalisme & outil d'action)
├── README.md                            # Présentation générale du projet
├── docs/
│   ├── METHODOLOGIE.md                  # Référentiel méthodologique et scientifique complet
│   └── plans/                           # Spécifications de design et plans d'implémentation
├── data/
│   ├── rixensart_data.js                # Données consolidées pour l'interface web (capteurs, historique, travaux)
│   ├── rixensart_summary.json           # Synthèse JSON des compteurs et métriques clés
│   ├── rixensart_summary.csv            # Synthèse tabulaire CSV
│   ├── rixensart_history.json           # Séries temporelles pluriannuelles (2024-2026)
│   ├── rixensart_telraam_full_data.json # Données brutes issues de l'API Telraam
│   └── rixensart_travaux.json           # Registre des chantiers et arrêtés de police communaux
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
L'application est conçue pour fonctionner de manière autonome (sans bundler lourd) avec Tailwind CSS, Leaflet.js et Chart.js.
