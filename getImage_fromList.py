import csv
import os
import requests
from PIL import Image
from io import BytesIO

# 저장할 폴더 생성
save_folder = 'images/'
os.makedirs(save_folder, exist_ok=True)

# CSV 파일에서 이미지 URL 읽기
csv_file = 'list/'  # 결과 CSV 경로
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
            filename = f"{safe_title}{title}{idx}.jpg"
            filepath = os.path.join(save_folder, filename)

            image.save(filepath)
            print(f"저장 완료: {filepath}")

        except Exception as e:
            print(f"[{idx}] 저장 실패 ({title}): {e}")
