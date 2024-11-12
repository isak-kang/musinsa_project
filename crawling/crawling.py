import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# 모듈 경로 설정.... 이렇게 해줘야 다른 디랙토리에 있는 모듈 가져다 쓸 수 있음... !!
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.DB import tb_insert_crawling_add_info, tb_insert_crawling_ranking, tb_insert_crawling_review,delete,item_id_select,tb_insert_crawling_size

# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
chrome_options.add_argument("--log-level=3")


# 랭킹 탑 100에 있는 이름, 랭킹, 가격 그리고 나중에 상세페이지 들어갈 때 쓰일 고유ID가져오기!!
def crawling_ranking():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=001000&period=MONTHLY"
    driver.get(url)

    SCROLL_PAUSE_TIME = 3  # 로딩 대기시간
    item_ids = []  # 리스트로 변경하여 순서 유지 --> 없으면 정보를 뒤죽박죽 가져옴.
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 랭킹 탑100에 대한 정보 수집 (100개 수집 시 종료)
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        divs = soup.find_all('div', class_="sc-1m4cyao-0 dQNLfk gtm-view-item-list")

        for div in divs:
            if len(item_ids) >= 100:
                break  
            try:
                # item_id, name, price, ranking, brand
                name = div.find('p', class_='text-body_13px_reg line-clamp-2 break-all whitespace-break-spaces text-black font-pretendard').get_text(strip=True)
                ranking = div.find('span', class_='text-etc_11px_semibold text-black font-pretendard').get_text(strip=True)
                price = div.find('span', class_='text-body_13px_semi sc-1m4cyao-12 fYDlTs text-black font-pretendard').get_text(strip=True)
                brand = div.find('p', class_='text-etc_11px_semibold line-clamp-1 break-all whitespace-break-spaces text-black font-pretendard').get_text(strip=True)
                
                
                if div and div.has_attr('data-item-id'):

                    item_id = div.get('data-item-id')
                    if item_id not in item_ids: 
                        item_ids.append(item_id)
                
                
                print("data-item-id:", item_id, "name:", name, "ranking:", ranking, "price:", price, "brand:", brand)
                
                # DataBase에 추가하기
                tb_insert_crawling_ranking(item_id, name, price, ranking,brand)

            except AttributeError as e:
                print(f"이거 외않되.. 수빈에몽 도와줭.. : {e}")

        # 100개 이상 수집했으면 반복 종료
        if len(item_ids) >= 100:
            break

    driver.quit()

# 추가 정보가져오기 추천성별, 별점(나중에 리뷰 긍부정 검사한거랑 비교해서 보여주면 좋을듯!)
def crawling_add_info():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    df_item_id = item_id_select()

    # item_id 값들 출력
    for index, row in df_item_id.iterrows():
        url = f"https://www.musinsa.com/products/{row['item_id']}"
        driver.get(url)

        # 페이지 로딩 대기 (최대 10초 동안 "성별" 텍스트를 포함한 span 요소가 나타날 때까지 대기)  --> 한번씩 성별 뺴먹고 가져올 때가 있어서 추가했어
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='성별']")))

        except Exception as e:
            print(f"로딩을 아무리해도 안나온다.. 도와줘요 수빈에몽 {row['item_id']}: {e}")
            continue

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            # gender, rating 추출
            gender_label = soup.find('span', text='성별')
            if gender_label:
                gender = gender_label.find_next_sibling('span').get_text(strip=True) 
            rating = soup.find('span', class_='text-xs font-medium pl-0.5 pr-1 cursor-default text-black font-pretendard').get_text(strip=True)
            img = soup.find("img", class_ = "sc-8j14dt-8 ljkzhU").attrs["src"]

            print("gender:", gender, "rating:", rating, "item_id:", row['item_id'], "img:", img)
            tb_insert_crawling_add_info(row['item_id'], gender, rating,img)

        except AttributeError as e:
            print(f"이거 외않되.. 수빈에몽 도와줭.. : {e}")
        
        time.sleep(1)
    driver.quit()

# 상세리뷰에서 키,몸무게,사이즈 정보가져오기 --> 키,몸무게 입력 시 추천 사이즈 뽑을 수 있게 하기 위함.
def crawling_size():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    df_item_id = item_id_select()

    SCROLL_PAUSE_TIME = 0.5 
    last_height = driver.execute_script("return document.body.scrollHeight")
    for index, row in df_item_id.iterrows():
        url = f"https://www.musinsa.com/review/goods/{row['item_id']}"
        driver.get(url)
        processed_indices = set()
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            divs = soup.find_all("div", {"data-index": True})

            for div in divs:
                data_index = div.get("data-index")

                # 이미 처리한 data-index는 건너뛰기
                if data_index in processed_indices:
                    continue
                processed_indices.add(data_index)

                elements = div.find_all('span', class_="text-body_13px_reg text-gray-600 font-pretendard")
                
                # 필요 요소 확인: 리스트 길이 검사
                if len(elements) >= 5:
                    try:
                        gender = elements[0].get_text(strip=True)
                        height = elements[1].get_text(strip=True)
                        weight = elements[2].get_text(strip=True)
                        size = elements[4].get_text(strip=True)

                        tb_insert_crawling_size(row['item_id'], height,weight, size, gender)
                        
                        print(row['item_id'],gender, height, weight, size)

                    except IndexError:
                        continue  

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height

    driver.quit()

# 상세리뷰에서 리뷰가져오기 --> 긍부정 검사를 위함.
def crawling_review():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    df_item_id = item_id_select()

    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    for index, row in df_item_id.iterrows():
        url = f"https://www.musinsa.com/review/goods/{row['item_id']}"
        driver.get(url)
        processed_indices = set()
        while True:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            divs = soup.find_all('div', class_="ReviewContentExpandable__Container-sc-14vwok6-0 iQPfei gtm-click-button")

            for div in divs:
                
                try:
                    review = div.find('p', class_='text-body_13px_reg ReviewContentExpandable__TextContainer-sc-14vwok6-1 guyFiO font-pretendard').get_text(strip=True)
                    tb_insert_crawling_review(row['item_id'], review)
                    print(row['item_id'], review)

                except IndexError:
                    continue 

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

    driver.quit()

if __name__ == "__main__":
    # delete()
    # crawling_ranking()
    # crawling_add_info()
    # crawling_size()
    # crawling_review()
    pass

