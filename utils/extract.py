import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev"

def fetch_page(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error saat mengambil halaman {url}: {e}")
        return None

def scrape_page(soup):
    products = []

    cards = soup.find_all("div", class_="collection-card")

    for card in cards:
        try:
            title_tag = card.find("h3", class_="product-title")
            title = title_tag.text.strip() if title_tag else None

            price_tag = card.find("span", class_="price")
            price = price_tag.text.strip() if price_tag else None

            details = card.find_all("p")

            rating = details[0].text.strip() if len(details) > 0 else None
            colors = details[1].text.strip() if len(details) > 1 else None
            size = details[2].text.strip() if len(details) > 2 else None
            gender = details[3].text.strip() if len(details) > 3 else None

            products.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "timestamp": datetime.now()
            })

        except Exception:
            continue

    return products

def extract_all(pages: int = 50):
    all_products = []

    for page in range(1, pages + 1):

        if page == 1:
            url = f"{BASE_URL}/"
        else:
            url = f"{BASE_URL}/page{page}"

        print(f"Scraping halaman {page}...")

        soup = fetch_page(url)
        if soup:
            products = scrape_page(soup)
            all_products.extend(products)

    df = pd.DataFrame(all_products)
    print(f"Total data berhasil diambil: {len(df)}")

    return df

if __name__ == "__main__":
    df = extract_all()
    print(df.head())