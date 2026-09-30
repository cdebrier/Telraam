#!/usr/bin/env python3
"""Met à jour l'année glissante et le profil des rues, puis régénère les données de la page.

    python3 update.py

Étapes : extract_year.py, extract_profile.py, generate_dashboard.py, puis contrôle des chiffres.
Si une étape échoue, les fichiers de données reviennent à leur état d'avant : jamais de page à moitié à jour.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILES = ["rixensart_year.json", "rixensart_profile.json", "rixensart_data.js", "rixensart_summary.json",
              "rixensart_summary.csv", "rixensart_history.json"]
STEPS = [
    ("Année glissante", [sys.executable, "extract_year.py"]),
    ("Profils de rue", [sys.executable, "extract_profile.py"]),
    ("Fusion des données", [sys.executable, "generate_dashboard.py"]),
    ("Contrôle des chiffres", ["node", "tools/check_aggregates.mjs", "--check"]),
]


def main():
    backup = tempfile.mkdtemp(prefix="telraam-backup-")
    saved = []
    for f in DATA_FILES:
        src = os.path.join(ROOT, "data", f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(backup, f))
            saved.append(f)
    for label, cmd in STEPS:
        print(f"\n== {label} ==", flush=True)
        if subprocess.run(cmd, cwd=ROOT).returncode != 0:
            print(f"\nÉchec à l'étape « {label} » : données restaurées.", file=sys.stderr)
            for f in DATA_FILES:
                dst = os.path.join(ROOT, "data", f)
                if f in saved:
                    shutil.copy2(os.path.join(backup, f), dst)
                elif os.path.exists(dst):
                    os.remove(dst)
            shutil.rmtree(backup, ignore_errors=True)
            return 1
    shutil.rmtree(backup, ignore_errors=True)
    print("\nMise à jour terminée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
