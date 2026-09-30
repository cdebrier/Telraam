"""Lit le profil déclaré de chaque rue sur telraam.net/en/location-profile/{id}.

La page est rendue côté serveur (pas d'API). On la réduit à des lignes de texte, puis on associe
chaque question à sa réponse. Champ absent ou « No idea » = None. Si aucune question attendue n'est
retrouvée, le capteur est ignoré (jamais de valeur par défaut inventée).
"""
import concurrent.futures as cf
import datetime as dt
import html
import json
import os
import re
import ssl
import sys
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "data", "rixensart_profile.json")


def page_lines(raw):
    t = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", raw, flags=re.S)
    t = re.sub(r"<(br|/p|/div|/li|/h\d|/label|/option|/select|/span)[^>]*>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    lines = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
    return [l for l in lines if l]


def answer(lines, question, start=0):
    """Ligne qui suit la première ligne contenant `question` (recherche à partir de `start`)."""
    q = re.sub(r"\s+", " ", question).lower()
    for i in range(start, len(lines) - 1):
        if q in re.sub(r"\s+([,?])", r"\1", lines[i]).lower():
            return lines[i + 1], i
    return None, -1


def num(s, unit=None):
    m = re.search(r"-?\d+(?:[.,]\d+)?", s or "")
    return float(m.group(0).replace(",", ".")) if m else None


def parse_profile(raw):
    lines = page_lines(raw)
    a, i0 = answer(lines, "How wide is the road")
    if a is None:
        return None                       # gabarit de page inattendu : on n'invente rien
    p = {"road_width_m": num(a)}
    a, _ = answer(lines, "division of different lanes with white markings", i0)
    p["lane_markings"] = None if a is None or "no idea" in a.lower() else (a.lower() != "no separate lanes")
    a, _ = answer(lines, "infrastructure for cyclists", i0)
    p["bike_lane"] = None if a is None or "no idea" in a.lower() else ("no bicycle lane" not in a.lower())
    a, j = answer(lines, "width footpath", i0)
    one = other = None
    if j >= 0:
        for l in lines[j:j + 4]:
            if l.lower().startswith("one side"): one = num(l)
            if l.lower().startswith("other side"): other = num(l)
    p["footpath_m"] = [one, other]
    a, _ = answer(lines, "one-way street", i0)
    p["one_way"] = None if a is None or "no idea" in a.lower() else (not a.lower().startswith("no"))
    a, _ = answer(lines, "bus line in this street", i0)
    p["bus"] = None if a is None or "no idea" in a.lower() else (not a.lower().startswith("no"))
    a, _ = answer(lines, "parking lane or possibility to park", i0)
    p["parking"] = None if a is None or "no idea" in a.lower() else (not a.lower().startswith("no"))
    a, _ = answer(lines, "function that fills your street", i0)
    p["function"] = None if a is None or "no idea" in a.lower() or a.strip("- ") == "" else a
    a, _ = answer(lines, "Maximum permitted speed", i0)
    p["max_speed"] = num(a)
    a, _ = answer(lines, "percentage of congestion", i0)
    p["congestion_pct"] = num(a)
    a, _ = answer(lines, "How safe do you experience", i0)
    p["safety_10"] = num(a)
    a, _ = answer(lines, "quality of life in your street", i0)
    p["quality_10"] = num(a)
    return p


def fetch(sid):
    req = urllib.request.Request(f"https://telraam.net/en/location-profile/{sid}", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def main(ids):
    out, fails = {}, []
    with cf.ThreadPoolExecutor(4) as ex:
        futs = {ex.submit(fetch, sid): sid for sid in ids}
        for f in cf.as_completed(futs):
            sid = futs[f]
            try:
                p = parse_profile(f.result())
            except Exception as e:
                p = None
                print(f"  {sid}: erreur {e}", file=sys.stderr)
            if p is None:
                fails.append(sid)
            else:
                out[str(sid)] = p
    prev = {}
    if os.path.exists(OUT):
        prev = json.load(open(OUT, encoding="utf-8")).get("sensors", {})
    for sid in fails:                      # profil illisible : on garde le précédent, marqué ancien
        if str(sid) in prev:
            out[str(sid)] = dict(prev[str(sid)], stale=True)
    return {"fetched_at": dt.date.today().isoformat(), "sensors": out}, fails


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    from extract_data import SENSORS, EXTRA_SENSORS
    res, fails = main([s["id"] for s in SENSORS + EXTRA_SENSORS])
    tmp = OUT + ".tmp"
    json.dump(res, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, OUT)
    print(f"{len(res['sensors'])} profils, {len(fails)} échec(s) : {fails}")
