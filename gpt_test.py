import pandas as pd
import os
import urllib.request
import urllib.parse
import json

service_key = '발급받은_서비스키'

keyword = '해수욕장'
save_dir = os.path.join('images', keyword)

def save_image_from_url(img_url, save_dir='images', filename=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, filename)
    try:
        urllib.request.urlretrieve(img_url, save_path)
        print(f"[✔] 이미지 저장 완료: {save_path}")
    except Exception as e:
        print(f"[✘] 이미지 저장 실패: {e}")

def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as err:
        print("크롤링 실패:", err)
        return None

def imageExtractor(contentId, title, pageNumber = 1, pageSize = 100):
    end_point = 'http://apis.data.go.kr/B551011/KorService1/detailImage1'
    params = (
        f'?serviceKey={service_key}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&contentId={contentId}'
        f'&imageYN=Y'
        f'&subImageYN=Y'
        f'&numOfRows={pageSize}'
        f'&pageNo={pageNumber}'
    )
    url = end_point + params
    raw_data = getDataFromWeb(url)
    if raw_data:
        try:
            data = json.loads(raw_data)
            items = data['response']['body']['items']['item']
            for idx, item in enumerate(items):
                img_url = item['originimgurl']
                img_id = os.path.basename(img_url).split('.')[0]  # 예: 123456_image_1
                safe_title = "".join(c for c in title if c.isalnum())  # 파일명 안전하게 처리
                filename = f"{safe_title}_{contentId}_{img_id}.jpg"
                save_image_from_url(img_url, save_dir=save_dir, filename=filename)
        except Exception as e:
            print(f"[!] 이미지 추출 중 오류 발생 (contentId={contentId}):", e)
    else:
        print("[✘] 데이터 없음")

# CSV 파일 불러오기 (KEYID: 콘텐츠 ID, TITLE: 제목)
df = pd.read_csv('csvlist/해수욕장_korS_total.csv')

for idx, row in df.iterrows():
    content_id = row['KEYID']
    title = row['TITLE']
    print(f"→ 콘텐츠 ID 처리 중: {content_id}")
    imageExtractor(content_id, title)
