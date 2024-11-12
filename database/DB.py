import pandas as pd
from sqlalchemy import create_engine, text
import pymysql
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:1234@127.0.0.1/musinsa")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# insert
# DB에 데이터 넣는 함수(table = crawling_ranking)
"""   
    DB = musinsa 
    Table = crawling_ranking
    colunm = item_id, name, price, ranking,brand
"""
def tb_insert_crawling_ranking(item_id, name, price, ranking, brand):
    query = text("INSERT INTO crawling_ranking(item_id, name, price, ranking,brand) VALUES (:val1, :val2, :val3, :val4, :val5)")  # colunm = item_id, name, price, ranking, brand
    values = {"val1": item_id, "val2": name, "val3": price, "val4": ranking, "val5": brand}
    
    with engine.connect() as conn:
        try:
            conn.execute(query, values)
            conn.commit() 
            print("tb_insert_crawling_ranking : 데이터 삽입성공!")
        except Exception as e:
            print(f"tb_insert_crawling_ranking : DB에 넣는거 실패함 ㅜㅜ 고쳐라: {e}")
            
# DB update 함수(table = crawling_ranking)
"""   
    DB = musinsa 
    Table = crawling_ranking
    colunm = gender, rating, img
"""
def tb_insert_crawling_add_info(item_id, gender, rating, img):
    query = text("UPDATE crawling_ranking SET gender = :val2, rating = :val3, img = :val4 WHERE item_id = :val1")  # colunm = gender, rating,img
    values = {"val1": item_id, "val2": gender, "val3": rating, "val4" : img}
    
    with engine.connect() as conn:
        try:
            conn.execute(query, values)  
            conn.commit()
            print("tb_insert_crawling_add_info : 데이터 삽입 성공~~~~!!!!")
        except Exception as e:
            print(f"tb_insert_crawling_add_info : DB에 넣는거 실패함 ㅜㅜ 일해라 : {e}")

# DB에 데이터 넣는 함수(table = crawling_size)
"""   
    DB = musinsa 
    Table = crawling_size
    colunm = item_id, height, weight, size, gender
"""
def tb_insert_crawling_size(item_id, height,weight, size, gender):
    query = text("INSERT INTO crawling_size VALUES (:val1, :val2, :val3, :val4, :val5)") # colunm = item_id, height, weight, size, gender
    values = {"val1": item_id, "val2": height, "val3": weight, "val4": size, "val5": gender}

    with engine.connect() as conn:
        try:
            conn.execute(query, values)  
            conn.commit()
            print("tb_insert_crawling_review : 데이터 삽입 성공~~~~!!!!")
        except Exception as e:
            print(f"tb_insert_crawling_review : DB에 넣는거 실패함 ㅜㅜ 빨리 고쳐라: {e}")

# DB에 데이터 넣는 함수(table = crawling_review)
"""   
    DB = musinsa 
    Table = crawling_review
    colunm = item_id, review
"""
def tb_insert_crawling_review(item_id, review):
    query = text("INSERT INTO crawling_review VALUES (:val1, :val2)")  # colunm = item_id, review
    values = {"val1": item_id, "val2": review}

    with engine.connect() as conn:
        try:
            conn.execute(query, values)  
            conn.commit()
            print("tb_insert_crawling_review : 데이터 삽입 성공~~~~!!!!")
        except Exception as e:
            print(f"tb_insert_crawling_review : DB에 넣는거 실패함 ㅜㅜ 고쳐줘잉: {e}")

# delete
# 모든 데이터 지우는 함수 --> 랭킹은 수시로 바뀌기 때문에 하루에 한번씩 다시 수정하기
def delete():
    delete_queries = [
        text("DELETE FROM crawling_ranking"),
        text("DELETE FROM crawling_review"),
        text("DELETE FROM crawling_size")
    ]

    with engine.connect() as conn:
        try:
            for query in delete_queries:
                conn.execute(query)
            conn.commit()
            print("모든 테이블 데이터 삭제 완료!")
            
        except Exception as e:
            print(f"delete : DB에서 삭제 실패함 ㅜㅜ 근데 이게 실패할 수가 있는건가??: {e}")

# select
# item_id 불러오기
def item_id_select():
    SQL = "SELECT item_id FROM crawling_ranking ORDER BY ranking" 

    with engine.connect() as conn:
        df = pd.read_sql(SQL, conn)
    return df

# item 값들 불러오기
def get_item():
    session = SessionLocal()
    try:
        query = text("SELECT item_id, name, price, img, brand, ranking,rating,gender FROM crawling_ranking order by ranking" )
        result = session.execute(query)
        items = [{"item_id": row[0], "name": row[1], "price": row[2], "img": row[3], "brand" : row[4], "ranking" : row[5], "rating" : row[6], "gender" : row[7]} for row in result]
    finally:
        session.close()
    return items


if __name__ == "__main__":

    # tb_insert_crawling_ranking(123,"오버핏 맨투맨","123,123원",23)
    # tb_insert_crawling_add_info(123,"공용",4.6)
    # tb_insert_crawling_size(123,"180cm","76kg","XL")
    # tb_insert_crawling_review(123,"옷이 너무 구려요")

    #delete()

    # df_item_id = item_id_select()
    # for index, row in df_item_id.iterrows():
    #     print(row["item_id"])

    pass