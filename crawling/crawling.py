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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.DB import tb_insert_crawling_add_info, tb_insert_crawling_ranking, tb_insert_crawling_review,delete,item_id_select,tb_insert_crawling_size
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# Selenium 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")
chrome_options.add_argument("--log-level=3")  # 로그 레벨 설정



def crawling_ranking():
    # 무신사 리뷰 페이지 URL
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=199&categoryCode=000&period=MONTHLY"
    driver.get(url)

    # 스크롤 및 크롤링 반복 설정

    SCROLL_PAUSE_TIME = 3  # 로딩을 기다리기 위해 대기 시간을 3초로 설정
    item_ids = []  # 리스트로 변경하여 순서 유지
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 모든 리뷰가 로드될 때까지 반복 (100개 수집 시 종료)
    while True:
        # 페이지의 HTML 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        item_divs = soup.find_all('div', class_="sc-1m4cyao-0 dQNLfk gtm-view-item-list")
        for item_div in item_divs:
            if len(item_ids) >= 100:
                break  # 100개 이상이면 중단
            try:
                # item_id, name, price, ranking
                name = item_div.find('p', class_='text-body_13px_reg line-clamp-2 break-all whitespace-break-spaces text-black font-pretendard').get_text(strip=True)
                if item_div and item_div.has_attr('data-item-id'):
                    item_id = item_div.get('data-item-id')
                    if item_id not in item_ids:  # 중복 방지
                        item_ids.append(name)  # 리스트에 추가하여 순서 유지

            
                ranking = item_div.find('span', class_='text-etc_11px_semibold text-black font-pretendard').get_text(strip=True)
                price = item_div.find('span', class_='text-body_13px_semi sc-1m4cyao-12 fYDlTs text-black font-pretendard').get_text(strip=True)
                print("data-item-id:", item_id, "name:", name, "ranking:", ranking, "price:", price)
                tb_insert_crawling_ranking(item_id, name, price, ranking)
                # rating, gender
                # item_url = f'https://www.musinsa.com/products/{item_id}'
                # driver.get(url)
        
                # gender = item_div.find('span', class_='text-xs font-normal text-gray-600 font-pretendard').get_text(strip=True)
                # rating = item_div.find('span', class_='text-xs font-medium pl-0.5 pr-1 cursor-default text-black font-pretendard').get_text(strip=True)
                # print("data-item-id:", item_id, "name:", name, "ranking:", ranking, "price:", price, "gender:", gender, "rating:", rating)

                # # review, height, weight
                # review_url = 'https://www.musinsa.com/review/goods/{item_id}'
                # driver.get(url)

            except AttributeError as e:
                print(f"Error parsing review item: {e}")

        # 100개 이상 수집했으면 반복 종료
        if len(item_ids) >= 100:
            break

        # 페이지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 스크롤 후 로딩을 위해 대기
        time.sleep(SCROLL_PAUSE_TIME)

        # 스크롤 이후의 페이지 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # 페이지 끝에 도달한 경우 종료
            break
        last_height = new_height
    driver.quit()

def crawling_add_info():
    # 무신사 리뷰 페이지 URL
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    df_item_id = item_id_select()

    # item_id 값들 출력 (iterrows 사용)
    for index, row in df_item_id.iterrows():
        url = f"https://www.musinsa.com/products/{row['item_id']}"
        driver.get(url)
                # 페이지 로딩 대기 (최대 10초 동안 "성별" 텍스트를 포함한 span 요소가 나타날 때까지 대기)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='성별']"))
            )
        except Exception as e:
            print(f"Timeout or Error loading item page for item_id {row['item_id']}: {e}")
            continue

        # 페이지의 HTML 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            # gender, rating 추출
            gender_label = soup.find('span', text='성별')  # "성별"이라는 텍스트를 가진 span 요소 찾기
            if gender_label:
                gender = gender_label.find_next_sibling('span').get_text(strip=True)  # 다음 형제 span 요소의 텍스트 추출
            rating = soup.find('span', class_='text-xs font-medium pl-0.5 pr-1 cursor-default text-black font-pretendard').get_text(strip=True)
            print("gender:", gender, "rating:", rating, "item_id:", row['item_id'])
            tb_insert_crawling_add_info(row['item_id'], gender, rating)
        except AttributeError as e:
            print(f"Error parsing review item: {e}")
        
        time.sleep(1)
    driver.quit()

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
            # 페이지의 HTML 가져오기
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 모든 리뷰 요소 찾기
            divs = soup.find_all("div", {"data-index": True})

            for div in divs:
                # 모든 해당 클래스 요소 찾기
                data_index = div.get("data-index")

                # 이미 처리한 data-index는 건너뛰기
                if data_index in processed_indices:
                    continue
                processed_indices.add(data_index)  # 새 data-index 추가

                elements = div.find_all('span', class_="text-body_13px_reg text-gray-600 font-pretendard")
                
                # 필요 요소 확인: 리스트 길이 검사
                if len(elements) >= 5:  # elements에 5개 이상 항목이 있는지 확인
                    try:
                        gender = elements[0].get_text(strip=True)
                        height = elements[1].get_text(strip=True)
                        weight = elements[2].get_text(strip=True)
                        size = elements[4].get_text(strip=True)
                        tb_insert_crawling_size(row['item_id'], height,weight, size)
                        print(row['item_id'],gender, height, weight, size)
                    except IndexError:
                        continue  # 필요한 정보가 없는 경우 건너뜁니다.

            # 페이지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            # 새로운 높이 가져오기
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # 더 이상 새로운 내용이 없으면 종료
            if new_height == last_height:
                break
            last_height = new_height

        # Selenium 브라우저 닫기
    driver.quit()

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
            # 페이지의 HTML 가져오기
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 모든 리뷰 요소 찾기
            divs = soup.find_all('div', class_="ReviewContentExpandable__Container-sc-14vwok6-0 iQPfei gtm-click-button")

            for div in divs:
                # 모든 해당 클래스 요소 찾기
                # data_index = div.get("data-index")

                # # 이미 처리한 data-index는 건너뛰기
                # if data_index in processed_indices:
                #     continue
                # processed_indices.add(data_index)  # 새 data-index 추가

                
                
                try:
                    review = div.find('p', class_='text-body_13px_reg ReviewContentExpandable__TextContainer-sc-14vwok6-1 guyFiO font-pretendard').get_text(strip=True)
                    tb_insert_crawling_review(row['item_id'], review)
                    print(row['item_id'], review)
                except IndexError:
                    continue  # 필요한 정보가 없는 경우 건너뜁니다.

            # 페이지 스크롤
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            # 새로운 높이 가져오기
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            # 더 이상 새로운 내용이 없으면 종료
            if new_height == last_height:
                break
            last_height = new_height

        # Selenium 브라우저 닫기
    driver.quit()

if __name__ == "__main__":
    # delete()
    # crawling_ranking()
    # crawling_add_info()
    # crawling_size()
    crawling_review()
