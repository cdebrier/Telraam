import socket
import urllib.request
import ssl
import json
import time
import os

# Force IPv4 to prevent macOS IPv6 connection hanging
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    return [r for r in old_getaddrinfo(*args, **kwargs) if r[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

ssl._create_default_https_context = ssl._create_unverified_context

# The 10 official sensors of the Rixensart network
SENSORS = [
    {
        "id": 9000007490,
        "street": "Rue de Genval",
        "locality": "Rixensart",
        "role": "Axe de liaison Rixensart - Genval",
        "speed_limit": 50
    },
    {
        "id": 9000007492,
        "street": "Chaussée de La Hulpe",
        "locality": "Rosières",
        "role": "Axe régional structurant / transit vers E411 & La Hulpe",
        "speed_limit": 50
    },
    {
        "id": 9000007497,
        "street": "Avenue Franklin Roosevelt",
        "locality": "Rixensart / Genval",
        "role": "Artère majeure de transit intercommunal",
        "speed_limit": 50
    },
    {
        "id": 9000007509,
        "street": "Rue de l'Institut",
        "locality": "Rixensart",
        "role": "Voirie de desserte résidentielle et scolaire",
        "speed_limit": 50
    },
    {
        "id": 9000007512,
        "street": "Rue de la Tasnière",
        "locality": "Genval",
        "role": "Quartier résidentiel et accès collines",
        "speed_limit": 30
    },
    {
        "id": 9000007523,
        "street": "Rue Haute",
        "locality": "Rixensart",
        "role": "Axe secondaire d'accès au centre et liaison",
        "speed_limit": 50
    },
    {
        "id": 9000007530,
        "street": "Place Communale",
        "locality": "Genval",
        "role": "Cœur de quartier et zone commerçante/conviviale",
        "speed_limit": 30
    },
    {
        "id": 9000007533,
        "street": "Avenue Albert 1er",
        "locality": "Rixensart / Genval",
        "role": "Axe structurant majeur et accès gare de Genval",
        "speed_limit": 50
    },
    {
        "id": 9000007534,
        "street": "Avenue de Boulogne-Billancourt",
        "locality": "Rixensart",
        "role": "Avenue résidentielle et desserte locale",
        "speed_limit": 50
    },
    {
        "id": 9000007578,
        "street": "Rue de la Gare",
        "locality": "Rixensart",
        "role": "Pôle multimodal gare de Rixensart / centre",
        "speed_limit": 30
    }
]

EXTRA_SENSORS = [
    {
        "id": 9000007261,
        "street": "Rue Mahiermont",
        "locality": "Genval",
        "role": "Desserte résidentielle (Genval)",
        "speed_limit": 50
    },
    {
        "id": 9000006402,
        "street": "Rue du Tilleul",
        "locality": "Genval",
        "role": "Desserte résidentielle (Genval)",
        "speed_limit": 30
    },
    {
        "id": 9000009405,
        "street": "Rue des Bergères",
        "locality": "Rosières",
        "role": "Projet 'L'école compte' (Rosières)",
        "speed_limit": 30
    }
]

def fetch_json(url, retries=3, delay=1.0):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt == retries - 1:
                print(f"Failed to fetch {url}: {e}")
                return None
            time.sleep(delay)
    return None

def main():
    print("Starting data extraction for Rixensart Telraam network...")
    output_dir = "/Users/charlesdebrier/Development/Telraam/data"
    os.makedirs(output_dir, exist_ok=True)
    
    extracted_data = {
        "metadata": {
            "commune": "Rixensart",
            "extracted_at": "2026-09-04",
            "total_official_sensors": len(SENSORS),
            "extra_sensors": len(EXTRA_SENSORS)
        },
        "sensors": []
    }
    
    all_sensors = SENSORS + EXTRA_SENSORS
    
    for i, s in enumerate(all_sensors, 1):
        sid = s["id"]
        is_official = any(s["id"] == x["id"] for x in SENSORS)
        print(f"[{i}/{len(all_sensors)}] Fetching sensor {sid} - {s['street']} ({s['locality']})...")
        
        sensor_info = dict(s)
        sensor_info["is_official_network"] = is_official
        
        # 1. Segment geometry & properties
        geo_url = f"https://telraam.net/api/segments/id/{sid}"
        geo_data = fetch_json(geo_url)
        if geo_data and "features" in geo_data and len(geo_data["features"]) > 0:
            feat = geo_data["features"][0]
            sensor_info["geometry"] = feat.get("geometry")
            sensor_info["properties"] = feat.get("properties")
        
        # 2. Reference period (Nov 2024 - when all 10 sensors were active)
        pie_nov24_url = f"https://telraam.net/api/measurements-piechart/segments/{sid}/2024-11-01/2024-11-30"
        sensor_info["nov2024_modal"] = fetch_json(pie_nov24_url)
        
        speed_nov24_url = f"https://telraam.net/api/measurements-speed/segments/{sid}/2024-11-01/2024-11-30"
        sensor_info["nov2024_speed"] = fetch_json(speed_nov24_url)
        
        v85_nov24_url = f"https://telraam.net/api/measurements-24-hour-chart-v85/segments/{sid}/2024-11-01/2024-11-30"
        sensor_info["nov2024_v85"] = fetch_json(v85_nov24_url)
        
        h24_nov24_url = f"https://telraam.net/api/measurements-24-hour-chart/segments/{sid}/2024-11-01/2024-11-30"
        sensor_info["nov2024_24h"] = fetch_json(h24_nov24_url)
        
        dir_nov24_url = f"https://telraam.net/api/measurements-24-hour-chart-direction/segments/{sid}/2024-11-01/2024-11-30"
        sensor_info["nov2024_direction"] = fetch_json(dir_nov24_url)
        
        # 3. Recent period (Last 14 days: 2026-08-21 to 2026-09-04)
        pie_recent_url = f"https://telraam.net/api/measurements-piechart/segments/{sid}/2026-08-21/2026-09-04"
        sensor_info["recent_modal"] = fetch_json(pie_recent_url)
        
        speed_recent_url = f"https://telraam.net/api/measurements-speed/segments/{sid}/2026-08-21/2026-09-04"
        sensor_info["recent_speed"] = fetch_json(speed_recent_url)
        
        v85_recent_url = f"https://telraam.net/api/measurements-24-hour-chart-v85/segments/{sid}/2026-08-21/2026-09-04"
        sensor_info["recent_v85"] = fetch_json(v85_recent_url)
        
        h24_recent_url = f"https://telraam.net/api/measurements-24-hour-chart/segments/{sid}/2026-08-21/2026-09-04"
        sensor_info["recent_24h"] = fetch_json(h24_recent_url)

        extracted_data["sensors"].append(sensor_info)
        print(f"  -> Successfully fetched {s['street']}")
        time.sleep(0.2)
        
    output_file = os.path.join(output_dir, "rixensart_telraam_full_data.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
    print(f"\nAll data successfully extracted and saved to {output_file}!")

if __name__ == "__main__":
    main()
