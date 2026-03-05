from utils.extract import extract_all
from utils.transform import transform_data
from utils.load import load_data

def main():
    print("=" * 50)
    print("Memulai proses ETL")
    print("=" * 50)

    # extract
    df_raw = extract_all()

    if df_raw.empty:
        print("Data kosong, proses dihentikan.")
        return

    # transform
    df_clean = transform_data(df_raw)

    # load
    load_data(df_clean)

    print("=" * 50)
    print("ETL selesai")
    print("=" * 50)

if __name__ == "__main__":
    main()