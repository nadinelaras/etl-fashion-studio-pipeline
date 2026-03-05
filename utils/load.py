import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

GOOGLE_SHEET_NAME = "ETL Fashion Studio"
SERVICE_ACCOUNT_FILE = "google-sheets-api.json"

# CSV
def save_to_csv(df: pd.DataFrame, filename: str = "products.csv"):
    try:
        # simpan ke root folder project
        df.to_csv(filename, index=False)
        print(f"CSV berhasil disimpan di {filename}")
    except Exception as e:
        print(f"Gagal menyimpan CSV: {e}")

# google sheets
def save_to_google_sheets(df: pd.DataFrame):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_FILE, scope
        )

        client = gspread.authorize(credentials)
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1

        # convert timestamp ke string
        df_copy = df.copy()
        if "timestamp" in df_copy.columns:
            df_copy["timestamp"] = df_copy["timestamp"].astype(str)

        sheet.clear()
        sheet.update([df_copy.columns.values.tolist()] + df_copy.values.tolist())

        print("Data berhasil disimpan ke Google Sheets")

    except Exception as e:
        print(f"Gagal menyimpan ke Google Sheets: {e}")

# PostgreSQL
def save_to_postgresql(df: pd.DataFrame):
    try:
        DB_USER = "postgres"
        DB_PASSWORD = "Psychosocial4!"
        DB_HOST = "localhost"
        DB_PORT = "5432"
        DB_NAME = "etl_db"

        engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        df.to_sql("fashion_products", engine, if_exists="replace", index=False)

        print("Data berhasil disimpan ke PostgreSQL")

    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")

# load pipeline
def load_data(df: pd.DataFrame):
    print("Memulai proses load...")

    save_to_csv(df)
    save_to_google_sheets(df)
    save_to_postgresql(df)

    print("Proses load selesai.")