import os
import json
import urllib.request
import pandas as pd

# 저장 폴더가 없으면 생성
def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

# 웹 요청 함수
def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('UTF-8')
    except Exception as err:
        print('❌ 크롤링 실패:', err)
        return None

# 이미지 저장 함수
def save_image(img_url, save_dir):
    try:
        filename = os.path.basename(img_url)
        save_path = os.path.join(save_dir, filename)
        urllib.request.urlretrieve(img_url, save_path)
        print(f"✅ 저장 완료: {save_path}")
    except Exception as e:
        print(f"❌ 저장 실패: {img_url} / 오류: {e}")

# 이미지 리스트 요청 및 처리 함수
def imageListExtractor(contentId, service_key, pageNo=1, numOfRows=10):
    endpoint = 'http://apis.data.go.kr/B551011/PhotoGalleryService1/galleryList1'
    params = (
        f'?serviceKey={service_key}'
        f'&numOfRows={numOfRows}'
        f'&pageNo={pageNo}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&contentId={contentId}'
    )
    url = endpoint + params
    raw_data = getDataFromWeb(url)

    print("✅ 최종 요청 URL:", url)
    print("🔍 응답 내용 확인:\n", raw_data)

    if raw_data:
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError as e:
            print("⚠️ JSON 파싱 오류:", e)
            return None
    return None

# JSON 데이터를 판다스 데이터프레임으로 변환
def makeImageTable(imageData):
    imageTable = pd.DataFrame()
    items = imageData['response']['body']['items']['item']
    if isinstance(items, dict):
        items = [items]

    for item in items:
        row = {
            'imgName': item.get('imgname'),
            'imgUrl': item.get('originimgurl'),
            'cpyrhtDivCd': item.get('cpyrhtDivCd'),
            'galContentId': item.get('galContentId'),
            'galTitle': item.get('galTitle'),
            'galPhotographyMonth': item.get('galPhotographyMonth'),
            'galPhotographyLocation': item.get('galPhotographyLocation'),
            'galPhotographer': item.get('galPhotographer'),
            'galSearchKeyword': item.get('galSearchKeyword'),
        }
        imageTable = pd.concat([imageTable, pd.DataFrame([row])], ignore_index=True)
    return imageTable
