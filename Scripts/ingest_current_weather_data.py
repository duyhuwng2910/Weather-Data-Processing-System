import requests
import pandas as pd
from datetime import datetime, timezone
import configparser
from pathlib import Path
from sqlalchemy import create_engine


# =========================
# Load configuration
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

API_KEY: str = config["openweathermap"]["api_key"]
CURRENT_WEATHER_URL: str = config["openweathermap"]["current_weather_url"]


# =========================
# MariaDB connection
# =========================

DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"      # nếu chạy container khác network -> đổi sang service name
DB_PORT = 3306
DB_NAME = "weather_data"
DB_TABLE = "weather_raw"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True
)


# =========================
# Province coordinates
# =========================

coordinates_by_city_dict = {
    "Tuyên Quang": [21.8223, 105.2196],
    "Lào Cai": [22.4833, 103.9566],
    "Thái Nguyên": [21.5938, 105.8486],
    "Phú Thọ": [21.3333, 105.1333],
    "Bắc Ninh": [21.1864, 106.0767],
    "Hưng Yên": [20.8672, 106.0144],
    "Hải Phòng": [20.8449, 106.6881],
    "Ninh Bình": [20.2500, 105.9740],
    "Quảng Trị": [16.7500, 107.2000],
    "Thành phố Đà Nẵng": [16.0544, 108.2022],
    "Quảng Ngãi": [15.1200, 108.8000],
    "Gia Lai": [13.7500, 108.2500],
    "Khánh Hoà": [12.2500, 109.2000],
    "Lâm Đồng": [11.5833, 108.4833],
    "Đắk Lắk": [12.6667, 108.0500],
    "Thành phố Hồ Chí Minh": [10.8333, 106.6667],
    "Đồng Nai": [10.9500, 106.8167],
    "Tây Ninh": [11.3333, 106.1000],
    "Thành phố Cần Thơ": [10.0333, 105.7833],
    "Vĩnh Long": [10.2500, 105.9667],
    "Đồng Tháp": [10.7167, 105.6333],
    "Cà Mau": [9.1833, 105.1500],
    "An Giang": [10.5000, 105.1667],
    "Thành phố Hà Nội": [21.0285, 105.8542],
    "Thành phố Huế": [16.4637, 107.5909],
    "Lai Châu": [22.3997, 103.4517],
    "Điện Biên": [21.3850, 103.0200],
    "Sơn La": [21.3250, 103.9000],
    "Lạng Sơn": [21.8450, 106.7575],
    "Quảng Ninh": [20.9528, 107.0800],
    "Thanh Hoá": [19.8000, 105.7833],
    "Nghệ An": [19.3333, 104.8333],
    "Hà Tĩnh": [18.3333, 105.9000],
    "Cao Bằng": [22.6667, 106.2500]
}


# =========================
# API call
# =========================

def fetch_weather(lat: float, lon: float) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "lang": "vi",
        "appid": API_KEY
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


# =========================
# Normalize JSON
# =========================

def normalize_weather(json_data: dict) -> dict:
    weather = json_data.get("weather", [{}])[0]
    main = json_data.get("main", {})
    wind = json_data.get("wind", {})
    clouds = json_data.get("clouds", {})

    return {
        "lat": json_data["coord"]["lat"],
        "lon": json_data["coord"]["lon"],
        "weather_main": weather.get("main"),
        "weather_description": weather.get("description"),
        "weather_icon": weather.get("icon"),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "temp_min": main.get("temp_min"),
        "temp_max": main.get("temp_max"),
        "pressure": main.get("pressure"),
        "humidity": main.get("humidity"),
        "visibility": json_data.get("visibility"),
        "wind_speed": wind.get("speed"),
        "wind_deg": wind.get("deg"),
        "wind_gust": wind.get("gust"),
        "clouds_all": clouds.get("all"),
        "city_id": json_data.get("id"),
        "event_ts": datetime.fromtimestamp(json_data.get("dt"), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "ingest_ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:00:00")
    }


# =========================
# Main ingest logic
# =========================

def main():
    records = []

    for province, coord in coordinates_by_city_dict.items():
        try:
            raw_json = fetch_weather(coord[0], coord[1])
            record = normalize_weather(raw_json)
            records.append(record)

            print(f"[SUCCESS] Ingested weather for {province}")
        except Exception as e:
            print(f"[ERROR] Failed {province}: {e}")

    if not records:
        print("No data collected.")

        return

    df = pd.DataFrame(records)

    try:
        df.to_sql(
            name=DB_TABLE,
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=100
        )

        print(f"[DONE] Inserted {len(df)} records into MariaDB table `{DB_TABLE}`")
    except Exception as e:
        print(f"[ERROR] Failed inserting to MariaDB: {e}")


# =========================
# Entry point
# =========================

if __name__ == "__main__":
    main()
