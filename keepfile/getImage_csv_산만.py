'''
getImage_csv_산만.py 파일 /.csv 리스트로부터 이미지 추출
너무 산만해서 gpt 에게 정리 부탁해서 버전 2 만들어 놓고 keepfile로 옮김/ 실제로 쓸 일이 없을 것 같아서

타겟 폴더, 생성 파일 이름과 path 꼭 확인할 것
root_dir = r"./../../project/keepfile" 타겟 폴더
output_csv = f"./../csvlist/etc/list_keepfile_202504.csv" 생성 파일
'''
import csv
import os
import requests
import urllib.parse
from PIL import Image
from io import BytesIO

# 저장할 폴더 생성
save_folder = 'images/'
os.makedirs(save_folder, exist_ok=True)

'''
csv 파일이 list_물놀이_galS1.csv 인 경우 source = 'gal1' searchword = '물놀이' 
'''
source = 'gal1' # 혹은 'kor'
searchword = '물놀이' # 혹은 수상레저 등등의 키워드
encoded_searchword = urllib.parse.quote(searchword)

# CSV 파일에서 이미지 URL 읽기
csv_file = '../csvlist/list_물놀이_galS1.csv'
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')  # 혹은 ',' 사용 (CSV 구조에 따라)

    for idx, row in enumerate(reader):
        if idx == 0:
            continue  # 첫 줄이 헤더면 건너뛰기

        if len(row) < 2:
            print(f"[{idx}] 열이 부족하여 건너뜀: {row}")
            continue

        title = row[0].strip()  # 예: '더베이 101'
        img_url = row[1].strip()  # 이미지 URL

        try:
            response = requests.get(img_url, timeout=20, allow_redirects=True)
            # response = requests.get(img_url, timeout=10, allow_redirects=False)
            # response = requests.get(img_url, timeout=10)
            if response.status_code != 200:
                print(f"[{idx}] 요청 실패 ({response.status_code}) → {img_url}")
                continue

            # 최종 URL 검사 (리다이렉트 확인용)
            if response.url != img_url:
                print(f"[{idx}] 리다이렉트 발생 → 최종 URL: {response.url}")

            # 이어서 상태 코드 및 content-type 검사
            content_type = response.headers.get('Content-Type')

            if 'image' not in content_type:
                print(f"[{idx}] 이미지 아님 (Content-Type: {content_type}) → URL: {img_url}")
                continue

            image = Image.open(BytesIO(response.content))

            # 파일 이름 정리
            safe_title = title.replace(" ", "_").replace("/", "_")
            filename = f"{safe_title}_{source}{searchword}{idx}.jpg"
            filepath = os.path.join(save_folder, filename)

            image.save(filepath)
            print(f"저장 완료: {filepath}")

        except Exception as e:
            print(f"[{idx}] 저장 실패 ({title}): {e}")
