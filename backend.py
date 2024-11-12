from crawling.crawling import crawling_add_info,crawling_ranking,crawling_review,crawling_size
from database.DB import delete
from analysis_model.review__analysis.review_model import review_analysis
from analysis_model.size_recommend.XGB import predict_size
# DB 갱신을 위한 삭제
delete() # 모든 테이블 데이터 삭제

# 데이터 크롤링 후 DB에 저장
crawling_ranking() # top 100 정보 크롤링
crawling_add_info() # top 100 다른 정보 크롤링
crawling_size() # 사이즈 정보 크롤링
crawling_review() # 리뷰 크롤링

# 리뷰 긍부정검사 후 DB에 저장
review_analysis()

# 사이즈 추천

# redicted_size = predict_size(height, weight, gender)