import json
import os
import pandas as pd
import numpy as np

def load_data(filepath="/Users/charlesdebrier/Development/Telraam/data/rixensart_telraam_full_data.json"):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist yet.")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_sensors(data):
    rows = []
    for s in data["sensors"]:
        sid = s["id"]
        street = s["street"]
        locality = s["locality"]
        role = s["role"]
        speed_limit = s["speed_limit"]
        is_official = s.get("is_official_network", True)
        
        # Nov 2024 reference (where all sensors were active)
        nov_modal = s.get("nov2024_modal") or {}
        nov_cars = nov_modal.get("car", 0)
        nov_heavy = nov_modal.get("heavy", 0)
        nov_motorized = nov_cars + nov_heavy
        nov_bikes = nov_modal.get("bike", 0)
        nov_peds = nov_modal.get("pedestrian", 0)
        nov_active = nov_bikes + nov_peds
        nov_total = nov_motorized + nov_active
        
        nov_bike_pct = float(nov_modal.get("bikePerc", 0) or 0)
        nov_ped_pct = float(nov_modal.get("pedestrianPerc", 0) or 0)
        nov_active_pct = nov_bike_pct + nov_ped_pct
        nov_heavy_pct = float(nov_modal.get("heavyPerc", 0) or 0)
        
        # Speeds Nov 2024
        nov_speed = s.get("nov2024_speed", {}).get("data", {}) or {}
        pct_0_30 = float(nov_speed.get("zeroPerc", 0) or 0) + float(nov_speed.get("tenPerc", 0) or 0) + float(nov_speed.get("twentyPerc", 0) or 0)
        pct_30_50 = float(nov_speed.get("thirtyPerc", 0) or 0) + float(nov_speed.get("fourtyPerc", 0) or 0)
        pct_over_50 = float(nov_speed.get("fiftyPerc", 0) or 0) + float(nov_speed.get("sixtyPerc", 0) or 0) + float(nov_speed.get("seventyPerc", 0) or 0)
        pct_over_speed_limit = pct_over_50 if speed_limit == 50 else (pct_30_50 + pct_over_50)
        
        # V85 Nov 2024
        nov_v85_data = s.get("nov2024_v85", {}).get("data", {}).get("speed_v85", []) or []
        # Filter non-zero hours (typically daytime 07:00 - 20:00)
        valid_v85 = [v for v in nov_v85_data if v > 0]
        avg_v85 = round(sum(valid_v85) / len(valid_v85), 1) if valid_v85 else None
        max_v85 = round(max(valid_v85), 1) if valid_v85 else None
        
        # Recent period (Aug-Sep 2026)
        rec_modal = s.get("recent_modal") or {}
        rec_total = sum(rec_modal.get("piedata", [0, 0, 0, 0]))
        rec_cars = rec_modal.get("car", 0)
        rec_bikes = rec_modal.get("bike", 0)
        rec_peds = rec_modal.get("pedestrian", 0)
        
        rec_speed = s.get("recent_speed", {}).get("data", {}) or {}
        rec_over_50 = float(rec_speed.get("fiftyPerc", 0) or 0) + float(rec_speed.get("sixtyPerc", 0) or 0) + float(rec_speed.get("seventyPerc", 0) or 0)
        
        rec_v85_data = s.get("recent_v85", {}).get("data", {}).get("speed_v85", []) or []
        valid_rec_v85 = [v for v in rec_v85_data if v > 0]
        rec_avg_v85 = round(sum(valid_rec_v85) / len(valid_rec_v85), 1) if valid_rec_v85 else None

        # Coordinates
        geom = s.get("geometry", {})
        coords = geom.get("coordinates", []) if geom else []
        flat_coords = []
        def get_pts(c):
            if not c: return []
            if isinstance(c[0], (int, float)): return [c]
            r = []
            for sc in c: r.extend(get_pts(sc))
            return r
        pts = get_pts(coords)
        lat = round(sum(p[1] for p in pts) / len(pts), 5) if pts else None
        lon = round(sum(p[0] for p in pts) / len(pts), 5) if pts else None

        rows.append({
            "id": sid,
            "street": street,
            "locality": locality,
            "role": role,
            "speed_limit": speed_limit,
            "is_official": is_official,
            "lat": lat,
            "lon": lon,
            "nov_total_30d": nov_total,
            "nov_daily_motorized": round(nov_motorized / 30),
            "nov_daily_active": round(nov_active / 30),
            "nov_daily_total": round(nov_total / 30),
            "nov_car_pct": round(nov_cars / nov_total * 100, 1) if nov_total else 0,
            "nov_heavy_pct": nov_heavy_pct,
            "nov_bike_pct": nov_bike_pct,
            "nov_ped_pct": nov_ped_pct,
            "nov_active_pct": round(nov_active_pct, 1),
            "nov_pct_0_30": round(pct_0_30, 1),
            "nov_pct_30_50": round(pct_30_50, 1),
            "nov_pct_over_50": round(pct_over_50, 1),
            "nov_pct_speeding": round(pct_over_speed_limit, 1),
            "nov_avg_v85": avg_v85,
            "nov_max_v85": max_v85,
            "recent_total_14d": rec_total,
            "recent_daily_total": round(rec_total / 14) if rec_total else 0,
            "recent_avg_v85": rec_avg_v85,
            "status": "Actif" if rec_total > 0 else "Inactif / Déconnecté"
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    data = load_data()
    if data:
        df = summarize_sensors(data)
        print("=== SYNTHÈSE DES COMPTEURS TELRAAM DE RIXENSART ===")
        print(df[["id", "street", "locality", "status", "nov_daily_total", "nov_active_pct", "nov_pct_speeding", "nov_avg_v85"]].to_string())
        df.to_csv("/Users/charlesdebrier/Development/Telraam/data/rixensart_summary.csv", index=False, encoding="utf-8")
        print("\nSaved summary to /Users/charlesdebrier/Development/Telraam/data/rixensart_summary.csv")
