import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .models import RamenShop

# BeautifulSoupを使ったスクレイピング
def scrape_ramen_shops():
    url = "https://retty.me/area/PRE13/ARE8/LCAT5/CAT290/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        print("ページ取得成功")
    except requests.RequestException as e:
        print(f"ページ取得エラー: {e}")
        return []

    restaurants = []

    for item in soup.find_all("div", class_="restaurant"):
        restaurant = {}

        # 店舗名
        name_tag = item.find("h3", class_="restaurant__name")
        restaurant['name'] = name_tag.text.strip() if name_tag else None

        # 店舗URL
        link_tag = item.find("a", class_="restaurant__block-link")
        restaurant['url'] = link_tag['href'] if link_tag else None

        # 特徴
        voice_tag = item.find("p", class_="restaurant__voice")
        restaurant['features'] = voice_tag.text.strip() if voice_tag else None

        # 写真URL
        image_tag = item.find("img", class_="image-viewer__item-img")
        if image_tag and image_tag.get('src'):
            restaurant['image_url'] = urljoin(url, image_tag['src'])
        else:
            restaurant['image_url'] = '/static/images/default.webp'  # デフォルト画像

        print(f"画像URL: {restaurant['image_url']}")  # デバッグ出力

        # 駅からの距離
        location_tag = item.find("dd", class_="information-list__description")
        restaurant['distance_from_station'] = location_tag.text.strip() if location_tag else None

        # ジャンル
        category_tag = item.find_all("dd", class_="information-list__description")
        restaurant['category'] = category_tag[1].text.strip() if len(category_tag) > 1 else None

        # データベースに保存
        try:
            RamenShop.objects.update_or_create(
                name=restaurant['name'],
                defaults={
                    'url': restaurant['url'],
                    'features': restaurant['features'],
                    'image_url': restaurant['image_url'],
                    'distance_from_station': restaurant['distance_from_station'],
                    'category': restaurant['category'],
                }
            )
            print(f"保存成功: {restaurant['name']}")
        except Exception as e:
            print(f"保存エラー: {restaurant['name']} - {e}")

        restaurants.append(restaurant)

    return restaurants


# Seleniumを使ったスクレイピング
def scrape_ramen_shops_with_selenium():
    url = "https://retty.me/area/PRE13/ARE8/LCAT5/CAT290/"

    # Seleniumのセットアップ
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service("/usr/local/bin/chromedriver")  # ChromeDriverのパスを正しく設定
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        # ページ全体が完全にロードされるまで待機
        driver.implicitly_wait(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print("ページ取得成功")
    except Exception as e:
        print(f"ページ取得エラー: {e}")
        driver.quit()
        return []

    restaurants = []

    # 店舗情報の抽出
    for item in soup.find_all("div", class_="restaurant"):
        restaurant = {}

        # 店舗名
        name_tag = item.find("h3", class_="restaurant__name")
        restaurant['name'] = name_tag.text.strip() if name_tag else None

        # 店舗URL
        link_tag = item.find("a", class_="restaurant__block-link")
        restaurant['url'] = urljoin(url, link_tag['href']) if link_tag else None

        # 特徴
        voice_tag = item.find("p", class_="restaurant__voice")
        restaurant['features'] = voice_tag.text.strip() if voice_tag else None

        # 写真URL
        image_tag = item.find("img", class_="image-viewer__item-img")
        if image_tag and image_tag.get("src"):
            restaurant['image_url'] = urljoin(url, image_tag['src'])
        else:
            restaurant['image_url'] = "/static/images/default.webp"  # デフォルト画像

        print(f"画像URL: {restaurant['image_url']}")

        # 駅からの距離
        location_tag = item.find("dd", class_="information-list__description")
        restaurant['distance_from_station'] = location_tag.text.strip() if location_tag else None

        # データベース保存
        try:
            RamenShop.objects.update_or_create(
                name=restaurant['name'],
                defaults={
                    'url': restaurant['url'],
                    'features': restaurant['features'],
                    'image_url': restaurant['image_url'],
                    'distance_from_station': restaurant['distance_from_station'],
                }
            )
            print(f"保存成功: {restaurant['name']}")
        except Exception as e:
            print(f"保存エラー: {restaurant['name']} - {e}")

        restaurants.append(restaurant)

    driver.quit()
    return restaurants