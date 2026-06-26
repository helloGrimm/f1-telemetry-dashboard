import json
import urllib.request

# FUNKCJE API ERGAST/JOLPICA - DANE FORMULA 1
# --- POBIERA LISTĘ DOSTĘPNYCH SEZONÓW (1950-obecnie) ---
def get_seasons(request: bool):
    try:
        url = "https://api.jolpi.ca/ergast/f1/seasons.json?limit=100"
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (LabVIEW F1 Project)',
                'Accept': 'application/json'
            }
        )

        seasons = []
        if request:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                for _ in data['MRData']['SeasonTable']['Seasons']:
                    seasons.append(_['season'])

        return json.dumps(seasons)

    except Exception as e:
        return json.dumps({"error": str(e), "seasons": []})

# --- POBIERA LISTĘ WYŚCIGÓW W DANYM SEZONIE ---
def get_races(request: bool, year: str):
    try:
        url = f"https://api.jolpi.ca/ergast/f1/{year}.json"
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (LabVIEW F1 Project)',
                'Accept': 'application/json'
            }
        )

        races = []
        if request:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            for r in data['MRData']['RaceTable']['Races']:
                races.append(r['raceName'])

        return json.dumps(races)

    except Exception as e:
        return json.dumps({"error": str(e), "races": []})

# --- POBIERA WYNIKI WYŚCIGU (pozycje, kierowcy, zespoły, czasy) ---
def get_race_results(request: bool, year: str, round_num: int):
    try:
        url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/results.json"
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (LabVIEW F1 Project)',
                'Accept': 'application/json'
            }
        )

        placement = []
        if request:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            races = data["MRData"]["RaceTable"]["Races"]
            if not races:
                return json.dumps([])

            race = races[0]
            results = race.get("Results", [])

            for r in results:
                placement.append({
                    'position': str(r['position']),
                    'driver': f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
                    'team': r['Constructor']['name'],
                    'grid': str(r['grid']),
                    'laps': str(r['laps']),
                    'time': r.get('Time', {}).get('time', 'DNF'),
                    'points': str(r['points'])
                })

        return json.dumps(placement)

    except Exception as e:
        return json.dumps({"error": str(e), "placement": []})

# --- POBIERA DANE TORU Z PLIKÓW GEOJSON (lokalnie) ---
# Mapowanie nazwy GP na nazwę pliku w folderze circuits/
# Zwraca współrzędne GPS (lon, lat) do narysowania toru
def get_track_data(request: bool, gp_name: str):
    try:
        if not request:
            return json.dumps({"error": True, "lon": [], "lat": []})

        if isinstance(gp_name, list):
            gp_name = gp_name[0] if gp_name else ""

        gp_name = str(gp_name).strip()

        GP_TO_FILE = {
            "Bahrain Grand Prix": "bh-2002",
            "Sakhir Grand Prix": "bh-2002",
            "Saudi Arabian Grand Prix": "sa-2021",
            "Australian Grand Prix": "au-1953",
            "Japanese Grand Prix": "jp-1962",
            "Chinese Grand Prix": "cn-2004",
            "Miami Grand Prix": "us-2022",
            "Emilia Romagna Grand Prix": "it-1922",
            "San Marino Grand Prix": "it-1922",
            "Monaco Grand Prix": "mc-1929",
            "Canadian Grand Prix": "ca-1978",
            "Spanish Grand Prix": "es-1991",
            "Austrian Grand Prix": "at-1969",
            "Styrian Grand Prix": "at-1969",
            "British Grand Prix": "gb-1948",
            "70th Anniversary Grand Prix": "gb-1948",
            "Hungarian Grand Prix": "hu-1986",
            "Belgian Grand Prix": "be-1925",
            "Dutch Grand Prix": "nl-1948",
            "Italian Grand Prix": "it-1922",
            "Azerbaijan Grand Prix": "az-2016",
            "European Grand Prix": "az-2016",
            "Singapore Grand Prix": "sg-2008",
            "United States Grand Prix": "us-2012",
            "Mexican Grand Prix": "mx-1962",
            "Mexico City Grand Prix": "mx-1962",
            "Brazilian Grand Prix": "br-1940",
            "São Paulo Grand Prix": "br-1940",
            "Las Vegas Grand Prix": "us-2023",
            "Qatar Grand Prix": "qa-2004",
            "Abu Dhabi Grand Prix": "ae-2009",
            "French Grand Prix": "fr-1969",
            "German Grand Prix": "de-1927",
            "Turkish Grand Prix": "tr-2005",
            "Portuguese Grand Prix": "pt-2008",
            "Russian Grand Prix": "ru-2014",
            "Argentine Grand Prix": "ar-1952",
            "South African Grand Prix": "za-1961",
            "Malaysian Grand Prix": "my-1999",
            "Madrid Grand Prix": "es-2026",
        }

        file_name = GP_TO_FILE.get(gp_name, "")
        if not file_name:
            return json.dumps({"error": True, "lon": [], "lat": []})

        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'circuits', f"{file_name}.geojson")

        if not os.path.exists(file_path):
            return json.dumps({"error": True, "lon": [], "lat": []})

        with open(file_path, 'r') as f:
            data = json.load(f)

        features = data.get('features', [])
        if not features:
            return json.dumps({"error": True, "lon": [], "lat": []})

        geometry = features[0]['geometry']
        coords = geometry['coordinates']

        lon = []
        lat = []

        for point in coords:
            lon.append(float(point[0]))
            lat.append(float(point[1]))

        return json.dumps({
            "error": False,
            "lon": lon,
            "lat": lat
        })

    except Exception as e:
        return json.dumps({"error": True, "lon": [], "lat": []})

# --- POBIERA CZASY OKRĄŻEŃ + PIT STOPY DLA KIEROWCY ---
def get_lap_times_with_pits(request: bool, year: str, round_num: int, driver_name: str):
    try:
        if not request:
            return json.dumps({"error": "Nic a nic", "laps": [], "times": [], "pits": []})

        parts = driver_name.strip().split()
        last_name = parts[-1].lower()
        full_name = driver_name.lower().replace(" ", "_")

        possible_ids = [last_name, full_name]

        if len(parts) > 1:
            first_name = parts[0].lower()
            possible_ids.append(f"{first_name}_{last_name}")

        driver_id = None
        for try_id in possible_ids:
            url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/drivers/{try_id}/laps.json?limit=100"

            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (LabVIEW F1 Project)'}
            )

            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))

            races = data['MRData']['RaceTable']['Races']

            if races:
                driver_id = try_id
                break

        if driver_id is None:
            return json.dumps({"error": "Nic a nic", "laps": [], "times": [], "pits": []})

        laps = []
        times = []

        for lap_data in races[0].get('Laps', []):
            lap_num = int(lap_data['number'])
            for timing in lap_data.get('Timings', []):
                if timing.get('driverId') == driver_id:
                    time_str = timing.get('time', '0:00.000')
                    time_parts = time_str.split(':')
                    if len(time_parts) == 2:
                        minutes = float(time_parts[0])
                        seconds = float(time_parts[1])
                        total_seconds = minutes * 60 + seconds
                    else:
                        total_seconds = float(time_parts[0])

                    laps.append(lap_num)
                    times.append(total_seconds)

        pit_url = f"https://api.jolpi.ca/ergast/f1/{year}/{round_num}/pitstops.json"
        pit_req = urllib.request.Request(pit_url, headers={'User-Agent': 'Mozilla/5.0'})

        pit_laps = []
        try:
            with urllib.request.urlopen(pit_req, timeout=10) as response:
                pit_data = json.loads(response.read().decode('utf-8'))

            pit_races = pit_data['MRData']['RaceTable']['Races']
            if pit_races:
                for pit in pit_races[0].get('PitStops', []):
                    if pit.get('driverId') == driver_id:
                        pit_laps.append(int(pit['lap']))
        except Exception as e:
            return json.dumps({"error": str(e), "laps": [], "times": [], "pits": []})

        return json.dumps({
            "error": "Nic a nic",
            "laps": laps,
            "times": times,
            "pits": pit_laps
        })

    except Exception as e:
        return json.dumps({"error": str(e), "laps": [], "times": [], "pits": []})