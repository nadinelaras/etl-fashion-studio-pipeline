import pandas as pd

EXCHANGE_RATE = 16000

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        print("Memulai proses transformasi...")

        # remove unknown title
        df = df[df["Title"].notna()]
        df = df[df["Title"] != "Unknown Product"]

        # clean rating
        df = df[df["Rating"].notna()]
        df = df[~df["Rating"].str.contains("Invalid", na=False)]
        df["Rating"] = df["Rating"].str.extract(r"(\d+\.?\d*)")
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        # clean price + konversi rupiah
        df = df[df["Price"].notna()]
        df["Price"] = df["Price"].str.replace("$", "", regex=False).str.strip()
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["Price"] = df["Price"] * EXCHANGE_RATE

        # clean colors
        df["Colors"] = df["Colors"].str.extract(r"(\d+)")
        df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce")

        # clean size
        df["Size"] = df["Size"].str.replace("Size:", "", regex=False).str.strip()

        # clean gender
        df["Gender"] = df["Gender"].str.replace("Gender:", "", regex=False).str.strip()

        # drop null dan duplicate
        df = df.drop_duplicates()
        df = df.dropna()
        df = df.reset_index(drop=True)

        print("Transformasi selesai.")
        print("Jumlah data setelah cleaning:", len(df))

        return df

    except Exception as e:
        print(f"Terjadi kesalahan saat transformasi: {e}")
        return pd.DataFrame()