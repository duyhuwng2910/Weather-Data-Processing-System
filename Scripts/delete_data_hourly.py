import configparser
from pathlib import Path
from sqlalchemy import create_engine, text
from datetime import datetime, timezone, timedelta


# =========================
# Load configuration
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


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
# Delete logic
# =========================

def delete_data_by_ingest_ts(ingest_ts: str) -> None:
    """
    Delete all records with specific ingest_ts value.
    ingest_ts format: YYYY-MM-DD HH:00:00

    Args:
        ingest_ts: Specific ingest_ts value to delete
    """
    try:
        with engine.connect() as connection:
            delete_query = text(f"""
                DELETE FROM {DB_TABLE}
                WHERE ingest_ts = :ingest_ts
            """)

            result = connection.execute(delete_query, {"ingest_ts": ingest_ts})
            rows_deleted = result.rowcount

            connection.commit()

            if rows_deleted > 0:
                print(f"[DONE] Deleted {rows_deleted} records with ingest_ts = {ingest_ts}")
            else:
                print(f"[INFO] No records found with ingest_ts = {ingest_ts}")

    except Exception as e:
        print(f"[ERROR] Failed deleting from MariaDB: {e}")


# =========================
# Main delete logic
# =========================

def main():
    """
    Run the periodic data deletion.
    Deletes records with ingest_ts equal to current hour (YYYY-MM-DD HH:00:00) in GMT+7.
    """
    print(f"[START] Beginning delete operation at {(datetime.now(timezone.utc) + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')}")

    # Get current datetime in GMT+7 and format to YYYY-MM-DD HH:00:00
    current_ingest_ts = (datetime.now(timezone.utc) + timedelta(hours=7)).strftime("%Y-%m-%d %H:00:00")

    print(f"[END] Delete operation completed")


# =========================
# Entry point
# =========================

if __name__ == "__main__":
    main()
