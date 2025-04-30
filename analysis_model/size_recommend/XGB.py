# 필요한 라이브러리 임포트
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from xgboost import XGBClassifier
import numpy as np
from joblib import dump, load

def create_size_model():
    df = pd.read_csv('./analysis_model/size_recommend/musinsa_size_XGB.csv', encoding='utf-8-sig')

    # '키'와 '몸무게'에서 숫자 부분만 추출 후 숫자형으로 변환
    df['height'] = df['height'].astype(str).str.extract(r'(\d+)').astype(float)
    df['weight'] = df['weight'].astype(str).str.extract(r'(\d+)').astype(float)

    # 결과 확인
    print(df[['height', 'weight']].head())

    # '사이즈'를 문자열로 변환 후 처리
    df['size'] = df['size'].astype(str).str.replace(r'[^SMLX23]', '', regex=True)

    # '2XL'을 'XL'로 대체
    df.loc[df['size'] == '2XL', 'size'] = 'XL'

    # 'XS'을 'S'로 대체
    df.loc[df['size'] == 'XS', 'size'] = 'S'

    # 원하는 사이즈 값만 남기기
    df = df[df['size'].isin(['M', 'L', 'S', 'XL'])]

    # 결과 확인
    print(df['size'])

    # #복사본 저장해두기
    df2 =df.copy()

    df['size'].value_counts()

    df=df2.copy()

    # BMI 범주화하여 새로운 컬럼 'bmi_category' 추가
    def categorize_bmi(bmi):
        if bmi < 18.5:
            return '저체중'
        elif 18.5 <= bmi < 24.9:
            return '정상'
        else:
            return '과체중'
        

    # 데이터 준비 및 전처리 (이전과 동일)
    size_order = ['S', 'M', 'L', 'XL']
    df['size'] = pd.Categorical(df['size'], categories=size_order, ordered=True)
    df['size'] = df['size'].cat.codes

    label_enc_gender = LabelEncoder()
    df['gender'] = label_enc_gender.fit_transform(df['gender'])

    df['BMI'] = df['weight'] / (df['height'] / 100) ** 2

    df['bmi_category'] = df['BMI'].apply(categorize_bmi)
    bmi_category_mapping = {'저체중': 0, '정상': 1, '과체중': 2}
    df['bmi_category'] = df['bmi_category'].map(bmi_category_mapping)

    X = df[['height', 'weight', 'bmi_category', 'gender']]
    y = df['size']

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X[['height', 'weight']])
    X_scaled = pd.DataFrame(X_scaled, columns=['height', 'weight'])
    X_scaled['gender'] = X['gender'].values
    X_scaled['bmi_category'] = X['bmi_category'].values

    # 최적의 하이퍼파라미터를 적용한 XGBoost 모델
    best_params = {'colsample_bytree': 1.0, 'learning_rate': 0.3, 'max_depth': 3, 'min_child_weight': 5, 'n_estimators': 50, 'subsample': 0.7}
    xgb_final_model = XGBClassifier(**best_params, use_label_encoder=False)
    xgb_final_model.fit(X_scaled, y)  # 전체 데이터로 학습

    from joblib import dump, load

    # 모델을 저장할 경로와 파일명 지정
    model_path = './analysis_model/size_recommend/size_model.joblib'

    # 모델 저장
    dump(xgb_final_model, model_path)
    print(f"모델이 {model_path}에 저장되었습니다.")

    scaler_path = './analysis_model/size_recommend/scaler.joblib'
    dump(scaler, scaler_path)
    print("Scaler 저장 완료!")


model_path = './analysis_model/size_recommend/size_model.joblib'
scaler_path = './analysis_model/size_recommend/scaler.joblib'

# 모델과 스케일러 로드
loaded_model = load(model_path)
scaler = load(scaler_path)  # 스케일러도 이전에 저장해두었다고 가정

# 기타 설정
size_order = ['S', 'M', 'L', 'XL']
label_enc_gender = LabelEncoder()  # 이 코드에서는 필요 없을 수도 있지만, gender를 변환할 때 사용한다고 가정
gender_mapping = {'남성': 0, '여성': 1}  # 예시로 추가한 gender 매핑

def categorize_bmi(bmi):
    if bmi < 18.5:
        return '저체중'
    elif 18.5 <= bmi < 24.9:
        return '정상'
    else:
        return '과체중'

def predict_size(height, weight, gender):
    # BMI 계산
    bmi = weight / (height / 100) ** 2
    bmi_category_label = categorize_bmi(bmi)
    
    # BMI 범주를 숫자로 변환
    bmi_category_mapping = {'저체중': 0, '정상': 1, '과체중': 2}
    bmi_category = bmi_category_mapping[bmi_category_label]
    
    # 입력 데이터 생성
    input_data = pd.DataFrame([[height, weight, gender_mapping[gender], bmi_category]], 
                              columns=['height', 'weight', 'gender', 'bmi_category'])
    input_data[['height', 'weight']] = scaler.transform(input_data[['height', 'weight']])  # 스케일링
    
    # 열 순서를 모델 학습 시 사용한 순서와 동일하게 변경
    input_data = input_data[['height', 'weight', 'gender', 'bmi_category']]
    
    # 예측
    prediction = loaded_model.predict(input_data)
    
    # 사이즈를 원래 레이블로 변환
    predicted_size = pd.Categorical.from_codes(prediction, categories=size_order)
    return predicted_size[0]


if __name__ == "__main__" :
    height = 174  # cm 단위
    weight = 72   # kg 단위
    gender = '남성'

    predicted_size = predict_size(height, weight, gender)
    print(f"예측된 사이즈: {predicted_size}")