무신사 랭킹 탑 100 리뷰 긍부정검사 및 체형에 맞는 사이즈 추천

소속 : LG U+ SW camp 2기
팀원 : 강이삭, 장은별, 정수빈
기간 : 24.11.6 ~ 24.11.13

1. 무신사 크롤링

   1-1. 무신사 최근 1달 기준 랭킹 탑 100 크롤링(item_id, name, price, brand, ranking)
   (url = https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=199&categoryCode=000)

   1-2. item_id를 통해 제품 상세 페이지 접속 후 나머지 필요 데이터 크롤링 (rating, gender, img_url)
   (url = https://www.musinsa.com/products/item_id)

   1-3. item_id를 통해 제품의 상세 리뷰 페이지 접속 후 체형 + 사이즈 정보 크롤링 (height, weight, size)
   (url = https://www.musinsa.com/review/goods/item_id)

   1-4. 마찬가지로 상세 리뷰 페이지에서 리뷰크롤링(review)
   (url = https://www.musinsa.com/review/goods/item_id)

2. DataBase(musinsa) 구성
   
   2-1. Table : crawling_ranking(column : item_id, name, price, brand, ranking, rating, gender, img)
   
   2-2. Table : crawling_size(column : item_id, height, weight, size)
   
   2-3. table : crawling_review(column : item_id, review)

3. 크롤링한 정보 DataBase에 삽입

   3-1. 크롤링한 후 DB에 바로 삽입 할 수 있도록하기.
   
4. 데이터 모델링
5. 
   4-1. 리뷰 감성분석

      4-1-1. 무신사에서 리뷰 데이터 수집 

      4-1-2. train, test data 라벨링

      4-1-3. 데이터 전처리

      4-1-4. 모델링

   4-2. 사이즈 후기를 통한 사이즈 추천 모델

      4-2-1. 무신사에서 사이즈 리뷰 데이터 수집

      4-2-2. ?

7. 서비스 만들기
8. AWS배포
