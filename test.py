import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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



def crawling_size():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    df_item_id = item_id_select()

    SCROLL_PAUSE_TIME = 0.5 
    last_height = driver.execute_script("return document.body.scrollHeight")
    item_ids = []
    for item_id in item_ids:
        url = f"https://www.musinsa.com/review/goods/{item_id}"
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

                        tb_insert_crawling_size(item_id, height,weight, size, gender)
                        
                        print(item_id,gender, height, weight, size)

                    except IndexError:
                        continue  

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            last_height = new_height

    driver.quit()

crawling_size()

