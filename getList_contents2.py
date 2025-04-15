import requests
import csv
import time
import os

# 키워드 리스트
keyword_list = [
    "바나나보트", "땅콩보트", "빅마블", "보트투어", "플라이피쉬", "워터슬라이드",
    "수상튜브", "아쿠아보트", "워터바이크", "패들보트", "카약", "수상 트램펄린",
    "수상 놀이공원", "수상 스쿠터", "서핑", "윈드서핑", "수상스키", "웨이크보드",
    "웨이크서핑", "제트스키", "스킨스쿠버", "스노클링", "요트", "SUP", "플라이보드"
]

API_KEY = "azksr7Fgk8fnWawWSRq/Rzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J+YdJm4QcpiSAGRw=="
ENDPOINT = "http://apis.data.go.kr/B551011/KorService/searchKeyword1"

# 결과 저장 폴더 생성
os.makedirs('list', exist_ok=True)
output_file = 'list/content_ids.csv'

with open(output_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['keyword', 'contentid', 'title'])

    for keyword in keyword_list:
        page = 1
        while True:
            params = {
                'serviceKey': API_KEY,
                'MobileOS': 'ETC',
                'MobileApp': 'AppTest',
                'arrange': 'A',
                'numOfRows': 100,
                'pageNo': page,
                'keyword': keyword,
                '_type': 'json',
                'listYN': 'Y'
            }

            response = requests.get(ENDPOINT, params=params)
            if response.status_code != 200:
                print(f"[{keyword}] 요청 실패: {response.status_code}")
                print(response.text)
                break

            items = response.json().get('response', {}).get('body', {}).get('items', {}).get('item', [])
            if not items:
                break

            for item in items:
                writer.writerow([keyword, item.get('contentid'), item.get('title')])

            print(f"[{keyword}] Page {page} 완료")
            page += 1
            time.sleep(0.5)

print("콘텐츠 ID 수집 완료!")
