"""Tracés officiels des segments Telraam, tels que la carte de telraam.net les dessine.

Écrit data/rixensart_geometry.json : {id du capteur: coordonnées MultiLineString [lon, lat]}.
Telraam ne publie pas la position du boîtier, seulement le tronçon de rue qu'il surveille.
"""
import json
import os
import ssl
import sys
import time
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "data", "rixensart_telraam_full_data.json")
OUT = os.path.join(ROOT, "data", "rixensart_geometry.json")


def get(sid, retries=3):
    req = urllib.request.Request(f"https://telraam.net/api/segments/id/{sid}", headers={"User-Agent": "Mozilla/5.0"})
    for k in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if k == retries - 1:
                raise
            time.sleep(1 + 2 * k)


def main():
    with open(SRC, encoding="utf-8") as f:
        ids = [s["id"] for s in json.load(f)["sensors"]]
    out = {}
    for sid in ids:
        feats = get(sid).get("features") or []
        geom = feats[0].get("geometry") if feats else None
        if not geom or not geom.get("coordinates"):
            print(f"Pas de tracé pour le segment {sid}", file=sys.stderr)
            return 1
        out[str(sid)] = geom["coordinates"]
        print(f"{sid} : {sum(len(p) for p in geom['coordinates'])} points")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
