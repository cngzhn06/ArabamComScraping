import requests
from bs4 import BeautifulSoup
import csv
import time
import random



def get_headers():
    user_agent = "YOUR_USER_AGENT"
    return {
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'DNT': '1'
    }


def get_soup(url, headers):
    time.sleep(random.uniform(1, 3))
    page = requests.get(url, headers=headers)
    print("HTTP Status Code:", page.status_code)
    print("Response Content:", page.content[:500])
    return BeautifulSoup(page.content, 'html.parser')


def save_to_csv(file_path, column_headers, row_datas):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(column_headers)
        for row in row_datas:
            writer.writerow(row)


def get_car_data(page_content):
    row_datas = []
    column_names = ["Model", "Yıl", "Fiyat", "Konum"]
    print("Page Content (Snippet):", page_content.prettify()[:500])

    rows = page_content.select('tr.listing-list-item')
    print(f"Bulunan Satır Sayısı: {len(rows)}")
    for row in rows:
        try:
            model = row.select_one('.listing-modelname .listing-text-new').get_text(strip=True)
            yil = row.select_one('td:nth-of-type(4) a').get_text(strip=True)
            fiyat = row.select_one('td:nth-of-type(7) .listing-price').get_text(strip=True)
            konum = row.select_one('td:nth-of-type(9) a').get_text(strip=True)
            row_datas.append([model, yil, fiyat, konum])
        except AttributeError as e:
            print(f"Veri çekmede hata: {e}")
            continue

    return column_names, row_datas


def main():
    headers = get_headers()
    base_url = "https://www.arabam.com/ikinci-el/otomobil/bmw-ankara"
    output_file_name = "arabam_com_bmw_ankara"
    all_rows_data = []
    column_names = []

    for page_num in range(1, 10):  # 10 sayfa için döngü
        url = f"{base_url}?page={page_num}"
        page_content = get_soup(url, headers)
        column_names, rows_data = get_car_data(page_content)
        all_rows_data.extend(rows_data)
        print(f"Sayfa {page_num} - Satır sayısı: {len(rows_data)}")

    if all_rows_data:
        save_to_csv(f'{output_file_name}.csv', column_names, all_rows_data)
        print(f"Toplam satır sayısı: {len(all_rows_data)}")


if __name__ == "__main__":
    main()
