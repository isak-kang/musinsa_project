무신사 랭킹 탑 100 리뷰 긍부정검사 및 체형에 맞는 사이즈 추천

소속 : LG U+ SW camp 2기
팀원 : 강이삭, 장은별, 정수빈
기간 : 24.11.6 ~ 24.11.13

1. 무신사 크롤링

   1-1. 무신사 최근 1달 기준 랭킹 탑 100 크롤링(item_id, name, price, brand, ranking) (url = https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=199&categoryCode=000)

   1-2. item_id를 통해 제품 상세 페이지 접속 후 나머지 필요 데이터 크롤링 (rating, gender, img_url) (url = https://www.musinsa.com/products/item_id)

   1-3. item_id를 통해 제품의 상세 리뷰 페이지 접속 후 체형 + 사이즈 정보 크롤링 (height, weight, size) (url = https://www.musinsa.com/review/goods/item_id)

   1-4. 마찬가지로 상세 리뷰 페이지에서 리뷰크롤링(review)

3. 크롤링한 데이터 DataBase에 넣기
4. 데이터 모델링
5. 서비스 만들기
6. AWS배포
