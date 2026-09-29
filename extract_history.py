import socket
import urllib.request
import ssl
import json
import time
import os

# Force IPv4
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    return [r for r in old_getaddrinfo(*args, **kwargs) if r[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

ssl._create_default_https_context = ssl._create_unverified_context

SENSORS = [
    {"id": 9000007490, "street": "Rue de Genval", "locality": "Rixensart"},
    {"id": 9000007492, "street": "Chaussée de La Hulpe", "locality": "Rosières"},
    {"id": 9000007497, "street": "Avenue Franklin Roosevelt", "locality": "Rixensart / Genval"},
    {"id": 9000007509, "street": "Rue de l'Institut", "locality": "Rixensart"},
    {"id": 9000007512, "street": "Rue de la Tasnière", "locality": "Genval"},
    {"id": 9000007523, "street": "Rue Haute", "locality": "Rixensart"},
    {"id": 9000007530, "street": "Place Communale", "locality": "Genval"},
    {"id": 9000007533, "street": "Avenue Albert 1er", "locality": "Rixensart / Genval"},
    {"id": 9000007534, "street": "Avenue de Boulogne-Billancourt", "locality": "Rixensart"},
    {"id": 9000007578, "street": "Rue de la Gare", "locality": "Rixensart"},
]

PERIODS = [
    {"key": "nov2024", "label": "Nov 2024 (Lancement)", "start": "2024-11-01", "end": "2024-11-30", "season": "Automne"},
    {"key": "jan2025", "label": "Jan 2025 (Hiver)", "start": "2025-01-15", "end": "2025-02-15", "season": "Hiver"},
    {"key": "may2025", "label": "Mai 2025 (Printemps)", "start": "2025-05-01", "end": "2025-05-31", "season": "Printemps"},
    {"key": "nov2025", "label": "Nov 2025 (1 an après)", "start": "2025-11-01", "end": "2025-11-30", "season": "Automne"},
    {"key": "may2026", "label": "Mai 2026 (Printemps)", "start": "2026-05-01", "end": "2026-05-31", "season": "Printemps"},
    {"key": "aug2026", "label": "Août 2026 (Récent)", "start": "2026-08-01", "end": "2026-08-31", "season": "Été"}
]

def fetch_period(sid, start, end):
    url = f"https://telraam.net/api/measurements-piechart/segments/{sid}/{start}/{end}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                d = json.loads(r.read().decode('utf-8'))
                tot = sum(d.get("piedata", [0, 0, 0, 0]))
                return {
                    "total": tot,
                    "cars": d.get("car", 0),
                    "heavy": d.get("heavy", 0),
                    "bikes": d.get("bike", 0),
                    "pedestrians": d.get("pedestrian", 0),
                    "bike_pct": float(d.get("bikePerc", 0) or 0),
                    "ped_pct": float(d.get("pedestrianPerc", 0) or 0),
                    "car_pct": float(d.get("carPerc", 0) or 0),
                    "heavy_pct": float(d.get("heavyPerc", 0) or 0),
                    "active_pct": round(float(d.get("bikePerc", 0) or 0) + float(d.get("pedestrianPerc", 0) or 0), 1)
                }
        except Exception as e:
            if attempt == 1:
                return {"total": 0, "cars": 0, "heavy": 0, "bikes": 0, "pedestrians": 0, "bike_pct": 0, "ped_pct": 0, "car_pct": 0, "heavy_pct": 0, "active_pct": 0}
            time.sleep(0.5)
    return {"total": 0, "cars": 0, "heavy": 0, "bikes": 0, "pedestrians": 0, "bike_pct": 0, "ped_pct": 0, "car_pct": 0, "heavy_pct": 0, "active_pct": 0}

def main():
    print("Starting historical timeline extraction for the 10 Rixensart sensors...", flush=True)
    history_data = {
        "periods": PERIODS,
        "sensors_history": []
    }
    
    # Global seasonal totals
    global_timeline = {p["key"]: {"total": 0, "cars": 0, "heavy": 0, "bikes": 0, "pedestrians": 0} for p in PERIODS}
    
    for i, s in enumerate(SENSORS, 1):
        sid = s["id"]
        print(f"[{i}/{len(SENSORS)}] Extracting history for {s['street']}...", flush=True)
        s_hist = {
            "id": sid,
            "street": s["street"],
            "locality": s["locality"],
            "periods": {}
        }
        
        cumulative_estimate = 0
        active_periods_count = 0
        
        for p in PERIODS:
            res = fetch_period(sid, p["start"], p["end"])
            s_hist["periods"][p["key"]] = res
            
            # Aggregate to global timeline if sensor was active
            if res["total"] > 0:
                global_timeline[p["key"]]["total"] += res["total"]
                global_timeline[p["key"]]["cars"] += res["cars"]
                global_timeline[p["key"]]["heavy"] += res["heavy"]
                global_timeline[p["key"]]["bikes"] += res["bikes"]
                global_timeline[p["key"]]["pedestrians"] += res["pedestrians"]
                cumulative_estimate += res["total"]
                active_periods_count += 1
                
            time.sleep(0.2)
            
        # Estimate total 2-year cumulative volume (based on monthly average * active months)
        if active_periods_count > 0:
            avg_month = cumulative_estimate / active_periods_count
            total_months = 14 if sid == 9000007492 else 23 # Rosieres stopped after ~14 months
            s_hist["estimated_2year_cumulative"] = round(avg_month * total_months)
        else:
            s_hist["estimated_2year_cumulative"] = 0
            
        history_data["sensors_history"].append(s_hist)
        print(f"  -> {s['street']}: ~{s_hist['estimated_2year_cumulative']:,} passages cumulés estimés", flush=True)

    history_data["global_timeline"] = global_timeline
    
    # Total cumulative estimate for entire municipal network
    total_network_cumulative = sum(s["estimated_2year_cumulative"] for s in history_data["sensors_history"])
    history_data["network_total_cumulative"] = total_network_cumulative
    print(f"\nTOTAL Estimé Réseau Communal (2 ans) : {total_network_cumulative:,} passages !", flush=True)
    
    out_path = "/Users/charlesdebrier/Development/Telraam/data/rixensart_history.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)
        
    print(f"Saved historical data to {out_path} successfully!", flush=True)

if __name__ == "__main__":
    main()
