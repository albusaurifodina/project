'''
getImage_csv_korIdDetail.py 파일 # 파일명 변경시 같이 변경 요망
키워드로 추출한 csv 파일 리스트의 컨텐츠ID에 해당하는 url에 접속 상세 이미지 생성

keyword = '키워드'
저장폴더 = '이미지폴더' 안 키워드 폴더)
파일이름 {safe_title}_{contentId}_{idx + 1}.jpg # 깔끔한 파일명!
'''

import urllib.request
import urllib.parse
import json
import os
import csv
import pandas as pd

# 발급받은 서비스 키
service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

# 키워드명 및 CSV 경로
keyword = '요트'
save_dir = os.path.join('images', keyword)

# CSV 파일 불러오기 (KEYID: 콘텐츠 ID, TITLE: 제목)
df = pd.read_csv(f'csvlist/{keyword}_korS_total.csv')

# 이미지 저장 함수
def save_image_from_url(img_url, save_dir='images', filename=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, filename)
    try:
        urllib.request.urlretrieve(img_url, save_path)
        print(f"[✔] 이미지 저장 완료: {save_path}")
    except Exception as e:
        print(f"[✘] 이미지 저장 실패: {e}")


# 웹 요청 함수
def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as err:
        print("크롤링 실패:", err)
        return None


# 콘텐츠 ID 하나로 이미지 추출
def imageExtractor(contentId, title, pageNumber=1, pageSize=100):
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
                safe_title = "".join(c for c in title if c.isalnum())  # 파일명 안전 처리
                filename = f"{safe_title}_{contentId}_{idx + 1}.jpg"  # 깔끔한 파일명!
                save_image_from_url(img_url, save_dir=save_dir, filename=filename)
        except Exception as e:
            print(f"[!] 이미지 추출 중 오류 발생 (contentId={contentId}):", e)
    else:
        print("[✘] 데이터 없음")

for idx, row in df.iterrows():
    content_id = row['KEYID']
    title = row['TITLE']
    print(f"→ 콘텐츠 ID 처리 중: {content_id}")
    imageExtractor(content_id, title)