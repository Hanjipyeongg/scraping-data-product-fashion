# Tokopedia Product Review Scraper
## Proyek ini merupakan web scraping ulasan produk dari platform Tokopedia menggunakan Python. Data yang dikumpulkan meliputi nama produk, harga, rating bintang, dan deskripsi ulasan pembeli yang selanjutnya akan digunakan untuk analisis teks seperti tokenizing, filtering, dan stemming.

# Tujuan Proyek
### Mengumpulkan data ulasan produk kaos polos dari Tokopedia secara otomatis untuk keperluan:
- Pembuatan dataset ulasan produk fashion
- Analisis sentimen
- Preprocessing teks (stemming & tokenizing)


#  Tech Stack
- Python 3.13
- Selenium — otomasi browser untuk navigasi halaman dinamis
- BeautifulSoup4 — parsing HTML
- Pandas — manipulasi dan export data
- openpyxl — export ke format Excel (.xlsx)
- Google Chrome + ChromeDriver


# Struktur Dataset
Dataset hasil scraping disimpan dalam format .xlsx dengan 4 kolom:
1. Nama Produk
2. Harga
3. Rating
4. Ulasan
