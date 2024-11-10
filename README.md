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

   4-1. 리뷰 감성분석

         4-1-1. 무신사에서 리뷰 데이터 수집 

         4-1-2. train, test data 라벨링

         4-1-3. 데이터 전처리

         4-1-4. 모델링

   4-2. 사이즈 후기를 통한 사이즈 추천 모델

         4-2-1. 무신사에서 사이즈 리뷰 데이터 수집

         4-2-2. ?

5. 서비스 만들기

   5-1. main 화면
         1. 무슨 기능 있으면 좋을까?

   5-2. top 100
         1. 사진, 제품이름, 브랜드이름, 랭킹 표시되면 좋을듯

   5-3. 제품 상세 정보
   
         1. 사진, 제품이름, 브랜드이름, 랭킹, 가격, 별점, 성별
   
         2. 고민1 --> 리뷰 감성분석한 결과를 매겨서 넣을까? 아니면 버튼을 하나 만들어서 들어가면 감성분석한 결과가 보이게 할까
   
         3. 고민2 --> 사이즈 추천하는 기능 --> 다른 url하나 만들어서 키와 몸무게 넣으면 추천하는 사이즈 나오게 or 이 제품은 000cm , 00kg의 사람들이 많이 구매했다. / 성별은 0성별이 몇% 구매했다 등등 이런식으로 넣을까??????
   
6. AWS배포

   2개의 ec에 배포
   
   하나는 DB
   
   하나는 서비스

   고민 -> 다른 서버를 하나 파서 특정시간( ex) 아침 9시 )에 크롤링, DB업데이트, 분석 모델이 돌아갈 수 있게 만들어서 항상 업데이트가 될 수 있도록 만드는 방안은 어떤가???

   
