import tensorflow as tf
import pandas as pd
import numpy as np
import urllib.request
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tqdm import tqdm
import csv
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import sys
import os
import re
from collections import defaultdict
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from database.DB import get_review,tb_insert_review_analysis


# 모델 만들기.
def create_review_model():
  okt = Okt()
  train_data = pd.read_csv("C:/Users/Admin/Desktop/vscode/musinsa_project/analysis_model/review__analysis/musinsa_train_data.csv", quoting=csv.QUOTE_ALL, encoding='cp949')
  test_data = pd.read_csv("C:/Users/Admin/Desktop/vscode/musinsa_project/analysis_model/review__analysis/musinsa_test_data.csv", quoting=csv.QUOTE_ALL, encoding='cp949')


  train_data['document'] = train_data['document'].str.replace('\n', ' ', regex=False)
  test_data['document'] = test_data['document'].str.replace('\n', ' ', regex=False)
  train_data.drop_duplicates(subset=['document'], inplace=True)
  train_data = train_data.dropna(how = 'any') # Null 값이 존재하는 행 제거
  train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
  train_data['document'] = train_data['document'].str.replace('^ +', "", regex=True) # white space 데이터를 empty value로 변경
  train_data['document'].replace('', np.nan, inplace=True) # 빈값은 모두 null 값으로 변경
  train_data = train_data.dropna(how = 'any')
  test_data.drop_duplicates(subset = ['document'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
  test_data['document'] = test_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True) # 정규 표현식 수행
  test_data['document'] = test_data['document'].str.replace('^ +', "", regex=True) # 공백은 empty 값으로 변경
  test_data['document'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
  test_data = test_data.dropna(how='any') # Null 값 제거

  stopword_text ='의 가 이 은 들 는 좀 잘 걍 과 도 를 으로 자 에 와 한 하다'
  stopwords = stopword_text.split()
  X_train = []
  for sentence in tqdm(train_data['document']):
      tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
      stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
      X_train.append(stopwords_removed_sentence)
  # 기존 코드
  X_test = []
  for sentence in tqdm(test_data['document']):
      tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
      stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
      X_test.append(stopwords_removed_sentence)

  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(X_train)

  threshold = 3
  total_cnt = len(tokenizer.word_index) # 단어의 수
  rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
  total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
  rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

  # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
  for key, value in tokenizer.word_counts.items():
      total_freq = total_freq + value

      # 단어의 등장 빈도수가 threshold보다 작으면
      if(value < threshold):
          rare_cnt = rare_cnt + 1
          rare_freq = rare_freq + value

  vocab_size = total_cnt - rare_cnt + 1

  tokenizer = Tokenizer(vocab_size) # 빈도수 2 이하인 단어는 제거
  tokenizer.fit_on_texts(X_train)
  X_train = tokenizer.texts_to_sequences(X_train)
  X_test = tokenizer.texts_to_sequences(X_test)

  y_train = np.array(train_data['label'])
  y_test = np.array(test_data['label'])

  drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
  drop_test = [index for index, sentence in enumerate(X_test) if len(sentence) < 1]

  X_train = [x for i, x in enumerate(X_train) if i not in set(drop_train)]
  y_train = [x for i, x in enumerate(y_train) if i not in set(drop_train)]

  X_test = [x for i, x in enumerate(X_test) if i not in set(drop_test)]
  y_test = [x for i, x in enumerate(y_test) if i not in set(drop_test)]

  max_len = 50

  X_train = pad_sequences(X_train, maxlen = max_len)
  X_test = pad_sequences(X_test, maxlen = max_len)

  y_train = np.array(y_train)
  y_test = np.array(y_test)

  with open('analysis_model/review__analysis/tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

  es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
  mc = ModelCheckpoint('analysis_model/review__analysis/best_model.keras', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

  model = Sequential()
  model.add(Embedding(vocab_size, 100))
  model.add(LSTM(128))
  model.add(Dense(1, activation='sigmoid'))

  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
  history = model.fit(X_train, y_train, epochs=15,
                      callbacks=[es, mc],
                      batch_size=64,
                      validation_split=0.2)








# 리뷰 전처리
def review_preprocessing():
  review = get_review()
  review['review'] = review['review'].str.replace('\n', ' ', regex=False)
  # 고유 데이터 건수 확인
  review['item_id'].nunique(), review['review'].nunique()
  # document 열에서 중복인 내용이 있다면 중복 제거
  review.drop_duplicates(subset=['review'], inplace=True)
  review = review.dropna(how = 'any') # Null 값이 존재하는 행 제거
  # print(review.isnull().values.any()) # Null 값이 존재하는지 확인
  review['review'] = review['review'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)
  review['review'] = review['review'].str.replace('^ +', "", regex=True) # white space 데이터를 empty value로 변경
  review['review'].replace('', np.nan, inplace=True) # 빈값은 모두 null 값으로 변경
  review.loc[review.review.isnull()][:5]
  review = review.dropna(how = 'any')
  return review


# 리뷰 긍부정 지표 DB에 저장.
def sentiment_predict_by_item(review):
    # 아이템별 긍부정 비율을 저장할 딕셔너리 생성
    loaded_model = load_model('analysis_model/review__analysis/best_model.keras')
    with open('analysis_model/review__analysis/tokenizer.pkl', 'rb') as f:
      tokenizer = pickle.load(f)
    okt = Okt()
    item_sentiment = defaultdict(lambda: {'긍정': 0, '부정': 0})
    max_len = 50
    stopword_text ='의 가 이 은 들 는 좀 잘 걍 과 도 를 으로 자 에 와 한 하다'
    stopwords = stopword_text.split()

    for item_id, review_text in review[['item_id', 'review']].values:
        # 리뷰 전처리
        review_text = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', review_text)
        review_text = okt.morphs(review_text, stem=True)
        review_text = [word for word in review_text if not word in stopwords]

        # 정수 인코딩 및 패딩
        encoded = tokenizer.texts_to_sequences([review_text])
        pad_new = pad_sequences(encoded, maxlen=max_len)

        # 감정 예측
        score = float(loaded_model.predict(pad_new))
        sentiment = '긍정' if score > 0.5 else '부정'

        # 아이템별 긍부정 데이터 업데이트
        item_sentiment[item_id][sentiment] += 1

    # 결과 출력
    for item_id, sentiment_count in item_sentiment.items():
        total_reviews = sentiment_count['긍정'] + sentiment_count['부정']
        positive_ratio = (sentiment_count['긍정'] / total_reviews) * 100 if total_reviews > 0 else 0
        negative_ratio = (sentiment_count['부정'] / total_reviews) * 100 if total_reviews > 0 else 0
        print(f"Item ID {item_id}: 긍정 {positive_ratio:.2f}%, 부정 {negative_ratio:.2f}%")
        positive_ratio
        tb_insert_review_analysis(item_id,positive_ratio, negative_ratio)

def review_analysis():
  review = review_preprocessing()
  sentiment_predict_by_item(review)


if __name__ == "__main__":
  # review = review_preprocessing()
  # sentiment_predict_by_item(review)
  # create_review_model()
  review_analysis()
  pass