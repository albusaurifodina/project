import csv
import os
import requests
from PIL import Image
from io import BytesIO

# 저장할 폴더 생성
save_folder = './../images/thumbimages'
os.makedirs(save_folder, exist_ok=True)

# CSV 파일에서 이미지 URL 읽기
# csv_file = './../list/getList_물놀이장_korSearch1.csv'
csv_file = './../list/test/searchlist1_Detail_해운대해수욕장.csv'
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')  # 혹은 ',' 사용 (CSV 구조에 따라)

    for idx, row in enumerate(reader):
        if idx == 0:
            continue  # 첫 줄이 헤더면 건너뛰기

        title = row[0]  # 예: '더베이 101'
        img_url = row[1]  # 이미지 URL

        try:
            response = requests.get(img_url, timeout=10)
            image = Image.open(BytesIO(response.content))

            # 파일 이름 정리
            safe_title = title.replace(" ", "_")
            filename = f"{safe_title}_{idx}.jpg"
            filepath = os.path.join(save_folder, filename)

            image.save(filepath)
            print(f"저장 완료: {filepath}")

        except Exception as e:
            print(f"저장 실패 ({title}): {e}")