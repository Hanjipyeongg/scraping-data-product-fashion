from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)


product_list = [
    {
        "url": "https://www.tokopedia.com/utamapolyflex/kaos-polos-lengan-pendek-cotton-combed-30s-premium-quality-merah-solid-s"
    },
    {
        "url": "https://www.tokopedia.com/pushopstore/pushop-kaos-polos-basic-pria-wanita-t-shirt-atasan-polos-unisex-cotton-combed-30s-reguler-fit-distro-baju-1729577787752745890"
    },
    {
        "url": "https://www.tokopedia.com/gildanplus/new-states-apparel-nsa-7200-t-shirt-premium-cotton-kaos-polos-s-white"
    },
    {
        "url": "https://www.tokopedia.com/mybasicindonesia/mybasic-boxy-crop-t-shirt-kaos-boxy-fit-with-cotton-combed-24s-dengan-200-gsm-1730149094126093896"
    }
]
MAX_HALAMAN = 30  
all_data = []

for i, product in enumerate(product_list):
    print(f"\n{'='*50}")
    print(f"Produk ke-{i+1}")

    for attempt in range(3):
        try:
            driver.get(product["url"])
            time.sleep(5)
            break
        except Exception as e:
            print(f"Attempt {attempt+1} gagal: {e}")
            time.sleep(5)

    soup_page = BeautifulSoup(driver.page_source, "html.parser")

    #  get product name
    nama_tag = soup_page.find("h1", attrs={"data-testid": "lblPDPDetailProductName"})
    nama_produk = nama_tag.get_text(strip=True) if nama_tag else ""

    # get price product
    harga_tag = soup_page.find("div", attrs={"data-testid": "lblPDPDetailProductPrice"})
    harga = harga_tag.get_text(strip=True) if harga_tag else ""

    print(f"Nama: {nama_produk}")
    print(f"Harga: {harga}")

    # access review tab
    try:
        tab_ulasan = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="review"]'))
        )
        driver.execute_script("arguments[0].click();", tab_ulasan)
        time.sleep(3)
        print("Tab Ulasan diklik!")
    except Exception as e:
        print(f"Tab Ulasan tidak ditemukan: {e}")
        continue

    page = 1
    while True:
        if page > MAX_HALAMAN:
            print("Batas halaman tercapai.")
            break

        print(f"-- Halaman {page} --")
        soup_detail = BeautifulSoup(driver.page_source, "html.parser")
        reviews = soup_detail.find_all("article", class_="css-15m2bcr")

        if not reviews:
            print("Tidak ada ulasan.")
            break

        for review in reviews:
            # get rating product
            rating_tag = review.find("div", attrs={"data-testid": "icnStarRating"})
            if rating_tag:
                aria = rating_tag.get("aria-label", "")
                rating = int(aria.split()[-1]) if aria else 0
            else:
                rating = 0

            # get description review
            ulasan_tag = review.find("span", attrs={"data-testid": "lblItemUlasan"})
            if not ulasan_tag:
                ulasan_tag = review.find("p", attrs={"data-testid": "lblItemUlasan"})
            ulasan = ulasan_tag.get_text(strip=True) if ulasan_tag else ""

            if ulasan or rating:
                all_data.append({
                    "Nama Produk": nama_produk,
                    "Harga": harga,
                    "Rating": rating,
                    "Ulasan": ulasan
                })
                print(f"  ⭐{rating} | {ulasan[:50]}...")

        # access pagination review
        try:
            next_page = driver.find_element(
                By.CSS_SELECTOR, f'button[aria-label="Laman {page + 1}"]'
            )
            driver.execute_script("arguments[0].click();", next_page)
            time.sleep(3)
            page += 1
        except:
            print("Halaman ulasan habis.")
            break

driver.close()

# export to excel
df = pd.DataFrame(all_data, columns=["Nama Produk", "Harga", "Rating", "Ulasan"])
df.to_excel("ulasan_kaospolos1.xlsx", index=False)
print(f"\nSelesai! Total {len(all_data)} ulasan → ulasan_kaospolos.xlsx")