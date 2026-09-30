"""Année glissante jusqu'à hier, par capteur, assemblée en 4 tranches de 91 jours.

Telraam renvoie des zéros (sans erreur) au-delà de ~90 jours : l'année ne peut pas être demandée d'un bloc.
Trafic par mode : somme des tranches. V85 : moyenne des V85 horaires (heures avec assez de mesures),
pondérée par les voitures de chaque heure : une approximation, documentée dans docs/METHODOLOGIE.md.
Les valeurs passées sont retraitées par Telraam : pas de cache par tranche, on recalcule tout.
"""
import concurrent.futures as cf
import datetime as dt
import json
import os
import ssl
import sys
import time
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "data", "rixensart_year.json")
BASE = "https://telraam.net/api/"
N_TRANCHES, LEN = 4, 91
MAX_FAILS = 3


def tranches(end):
    """4 tranches contiguës de 91 jours se terminant à `end` (ordre chronologique)."""
    out, e = [], end
    for _ in range(N_TRANCHES):
        s = e - dt.timedelta(days=LEN - 1)
        out.append((s, e))
        e = s - dt.timedelta(days=1)
    return out[::-1]


def get(path, retries=3):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    for k in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if k == retries - 1:
                raise
            time.sleep(1 + 2 * k)


def fetch_tranche(sid, s, e):
    rng = f"segments/{sid}/{s}/{e}"
    return {
        "pie": get(f"measurements-piechart/{rng}"),
        "v85": get(f"measurements-24-hour-chart-v85/{rng}")["data"],
        "h24": get(f"measurements-24-hour-chart/{rng}")["data"],
        "days": get(f"measurements-day-barchart/{rng}")["data"],
    }


def _d(x):
    return x if isinstance(x, dict) else {}      # Telraam renvoie [] pour un capteur sans données


def aggregate(raws, total_days):
    """Combine les tranches d'un capteur. Pure : testée sans réseau."""
    modes = {k: 0 for k in ("car", "heavy", "bike", "pedestrian", "night")}
    days, num, den, hours = 0, 0.0, 0.0, 0
    for r in raws:
        for k in modes:
            modes[k] += _d(r["pie"]).get(k, 0) or 0
        days += sum(1 for c in _d(r["days"]).get("car", []) if c and c > 0)
        v, op, cars = _d(r["v85"]).get("speed_v85", []), _d(r["v85"]).get("speed_histogram_opacity", []), _d(r["h24"]).get("car", [])
        for x, o, c in zip(v, op, cars):
            if x and x > 0 and o >= 0.5 and c and c > 0:
                num += x * c
                den += c
                hours += 1
    out = {"modes": modes, "days_with_data": days, "coverage": round(days / total_days, 2),
           "v85": round(num / den, 1) if den else None, "v85_hours": hours}
    if days:
        m = modes
        motor, active = m["car"] + m["heavy"], m["bike"] + m["pedestrian"]
        out["per_day"] = {"vehicles": round(motor / days), "cars": round(m["car"] / days), "heavy": round(m["heavy"] / days),
                          "bikes": round(m["bike"] / days), "pedestrians": round(m["pedestrian"] / days),
                          "night": round(m["night"] / days)}
        tot = motor + active
        out["active_pct"] = round(active / tot * 100, 1) if tot else 0
        out["mode_pct"] = {k: round(m[k] / tot * 100, 1) if tot else 0 for k in ("car", "heavy", "bike", "pedestrian")}
    return out


def main(ids, end=None):
    end = end or dt.date.today() - dt.timedelta(days=1)
    tr = tranches(end)
    jobs = [(sid, s, e) for sid in ids for s, e in tr]
    got, errors = {}, {}
    with cf.ThreadPoolExecutor(4) as ex:
        futs = {ex.submit(fetch_tranche, *j): j for j in jobs}
        for f in cf.as_completed(futs):
            sid, s, e = futs[f]
            try:
                got.setdefault(sid, {})[(s, e)] = f.result()
            except Exception as exc:
                errors.setdefault(sid, []).append(f"{s}: {exc}")
    prev = {}
    if os.path.exists(OUT):
        prev = json.load(open(OUT, encoding="utf-8")).get("sensors", {})
    sensors, fails = {}, []
    for sid in ids:
        if sid in errors or len(got.get(sid, {})) < N_TRANCHES:
            fails.append(sid)
            if str(sid) in prev:
                sensors[str(sid)] = dict(prev[str(sid)], stale=True)
            continue
        sensors[str(sid)] = aggregate([got[sid][t] for t in tr], LEN * N_TRANCHES)
    return {"start": str(tr[0][0]), "end": str(end), "days": LEN * N_TRANCHES,
            "fetched_at": dt.date.today().isoformat(), "sensors": sensors}, fails, errors


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    from extract_data import SENSORS, EXTRA_SENSORS
    res, fails, errors = main([s["id"] for s in SENSORS + EXTRA_SENSORS])
    for sid, errs in errors.items():
        print(f"  {sid}: {errs[0]}", file=sys.stderr)
    if len(fails) > MAX_FAILS:
        print(f"{len(fails)} capteurs en échec (> {MAX_FAILS}) : mise à jour abandonnée", file=sys.stderr)
        sys.exit(1)
    tmp = OUT + ".tmp"
    json.dump(res, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, OUT)
    print(f"{res['start']} → {res['end']} : {len(res['sensors'])} capteurs, {len(fails)} échec(s) {fails}")
