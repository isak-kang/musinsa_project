import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io
import base64

# 한글 폰트 설정
def set_korean_font():
    font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows의 맑은 고딕
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 도넛 차트 그리기
def graph_url(pos, neg):
    set_korean_font()  # 한글 폰트 설정

    total = [pos, neg]  # 데이터
    total_labels = ['긍정 (Positive)', '부정 (Negative)']  # 한글 라벨
    total_percentage = [f'{(pos / sum(total)) * 100:.1f}%', f'{(neg / sum(total)) * 100:.1f}%']

    # 파이차트 설정
    explode = (0.1, 0)  # 첫 번째 조각 강조
    fig, ax = plt.subplots(figsize=(8, 6))  # 그래프 크기 설정
    wedges, texts = ax.pie(
        total,
        labels=None,  # 라벨 제거
        shadow=True,
        startangle=90,
        colors=['#595959', '#e0e0e0'],
        wedgeprops=dict(width=0.6),
        explode=explode
    )

    # 범례 추가 (각 항목의 색상 표시) - 그래프 아래로 이동
    ax.legend(
        labels=[f"{label} ({percentage})" for label, percentage in zip(total_labels, total_percentage)],
        loc="center",
        fontsize=12,
        frameon=False,
        title_fontsize=14,
        bbox_to_anchor=(0.5, -0.2),  # 범례를 그래프 아래로 배치
        ncol=2  # 범례를 두 개의 열로 나누어 표시
    )

    # 그래프 저장
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    #plt.show()  # 그래프 표시
    return graph_url

# def review_rating2():


if __name__ == "__main__":
    # 테스트 실행
    #graph_url(80, 20)
    pass