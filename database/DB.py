import pandas as pd
from sqlalchemy import create_engine, text
import pymysql

# DB연결
def db_connect():
    engine = create_engine("mysql+pymysql://root:1234@127.0.0.1/musinsa")
    return engine

# insert
# DB에 데이터 넣는 함수(table = crawling_ranking)
"""   
    DB = musinsa 
    Table = crawling_ranking
    colunm = item_id, name, price, ranking
"""
def tb_insert_crawling_ranking(item_id, name, price, ranking):
    engine = db_connect()

    query = text("INSERT INTO crawling_ranking VALUES (:val1, :val2, :val3, :val4)")  # colunm = item_id, name, price, ranking
    
    values = {"val1": item_id, "val2": name, "val3": price, "val4": ranking}
    
    with engine.connect() as conn:
        try:
            
            conn.execute(query, values)  
            conn.commit() 
        except Exception as e:
            print(f"DB에 넣는거 실패함 ㅜㅜ 수빈에몽 고쳐줘: {e},tb_insert_crawling_ranking")
            
# DB에 데이터 넣는 함수(table = crawling_add_info)
"""   
    DB = musinsa 
    Table = crawling_add_info
    colunm = item_id, gender, rating
"""
def tb_insert_crawling_add_info(item_id, gender, rating):
    engine = db_connect()
    
    query = text("INSERT INTO crawling_add_info VALUES (:val1, :val2, :val3)")  # colunm = item_id, gender, rating
    
    values = {"val1": item_id, "val2": gender, "val3": rating}
    
    with engine.connect() as conn:
        try:
            conn.execute(query, values)  
            conn.commit()
            print("데이터 삽입 성공~~~~!!!!")
        except Exception as e:
            print(f"DB에 넣는거 실패함 ㅜㅜ 수빈에몽 고쳐줘: {e},tb_insert_crawling_add_info")

# DB에 데이터 넣는 함수(table = crawling_size)
"""   
    DB = musinsa 
    Table = crawling_size
    colunm = item_id, height, weight, size
"""
def tb_insert_crawling_size(item_id, height,weight, size):
    engine = db_connect()
    query = text("INSERT INTO crawling_size VALUES (:val1, :val2, :val3, :val4)") # colunm = item_id, height, weight, size
    values = {"val1": item_id, "val2": height, "val3": weight, "val4": size}
    with engine.connect() as conn:
        try:
            conn.execute(query, values)  
            conn.commit() 
        except Exception as e:
            print(f"tb_insert_crawling_review : DB에 넣는거 실패함 ㅜㅜ 수빈에몽 고쳐줘: {e}")

# DB에 데이터 넣는 함수(table = crawling_review)
"""   
    DB = musinsa 
    Table = crawling_review
    colunm = item_id, review
"""
def tb_insert_crawling_review(item_id, review):
    engine = db_connect()
    query = text("INSERT INTO crawling_review VALUES (:val1, :val2)")  # colunm = item_id, review
    values = {"val1": item_id, "val2": review}
    with engine.connect() as conn:
        try:
            conn.execute(query, values)  
            conn.commit()
            print("데이터 삽입 성공~~~~!!!!")
        except Exception as e:
            print(f"tb_insert_crawling_review : DB에 넣는거 실패함 ㅜㅜ 수빈에몽 고쳐줘: {e}")




# 모든 데이터 지우는 함수 --> 랭킹은 수시로 바뀌기 때문.
def delete():
    engine = db_connect()
    delete_queries = [
        text("DELETE FROM crawling_ranking"),
        text("DELETE FROM crawling_review"),
        text("DELETE FROM crawling_add_info"),
        text("DELETE FROM crawling_size")
    ]
    with engine.connect() as conn:
        try:
            for query in delete_queries:
                conn.execute(query)
            conn.commit()
            print("모든 테이블 데이터 삭제 완료!")
            
        except Exception as e:
            print(f"DB에서 삭제 실패함 ㅜㅜ: {e}, delete")


# DB 데이터 불러오는 함수
def item_id_select():
    engine = db_connect()
    SQL = "SELECT item_id FROM crawling_ranking ORDER BY ranking" 
    with engine.connect() as conn:
        df = pd.read_sql(SQL, conn)
    return df



if __name__ == "__main__":
    df_item_id = item_id_select()

    # item_id 값들 출력 (iterrows 사용)
    for index, row in df_item_id.iterrows():
        print(row["item_id"])