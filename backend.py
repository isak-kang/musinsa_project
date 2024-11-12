from crawling.crawling import crawling_add_info,crawling_ranking,crawling_review,crawling_size
from database.DB import delete

# DB 갱신을 위한 삭제
delete() # 모든 테이블 데이터 삭제

# 데이터 크롤링 후 DB에 저장
crawling_ranking() # top 100 정보 크롤링
crawling_add_info() # top 100 다른 정보 크롤링
crawling_size() # 사이즈 정보 크롤링
crawling_review() # 리뷰 크롤링

# 긍부정검사

# 사이즈 추천