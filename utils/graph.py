import matplotlib.pyplot as plt
import io
import base64

def graph_url(pos,neg):
    total = [pos,neg]  # 데이터1과 데이터2의 합
    total_labels = ['pos', 'neg']  # 데이터1과 데이터2에 대한 라벨

    # 파이차트 그리기
    fig, ax = plt.subplots()
    ax.pie(total, labels=total_labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    ax.axis('equal')  # 파이차트가 원 모양이 되도록 설정

    # 그래프를 PNG로 변환하여 base64로 인코딩
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    
    plt.show()
    return graph_url

if __name__ == "__main__":
    graph_url(10,20)