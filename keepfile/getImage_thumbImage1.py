import csv
import os
import requests
from PIL import Image
from io import BytesIO

save_folder = "project/images/thumbimages"
os.makedirs(save_folder, exist_ok=True)

searchword = '바나나보트'
csv_file = 'project/list/test/searchlist1_바나나보트.csv'
success_log = 'project/list/test/success_log.csv'
fail_log = 'project/list/test/fail_log.csv'

# 이미 저장된 이미지 URL 읽기 (중복 방지용)
existing_urls = set()
if os.path.exists(success_log):
    with open(success_log, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        existing_urls = {row[1] for row in reader}  # URL은 두 번째 컬럼이라고 가정

# 결과 파일들 열기 (append 모드)
success_writer = open(success_log, 'a', newline='', encoding='utf-8')
fail_writer = open(fail_log, 'a', newline='', encoding='utf-8')
success_csv = csv.writer(success_writer)
fail_csv = csv.writer(fail_writer)

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')

    for idx, row in enumerate(reader):
        if idx == 0:
            continue  # 헤더 건너뜀

        try:
            title = row[0]
            img_url = row[1]

            if img_url in existing_urls:
                print(f"[{idx}] 중복 URL → 건너뜀: {img_url}")
                continue

            response = requests.get(img_url, timeout=10)

            if response.status_code != 200:
                fail_csv.writerow([idx, title, img_url, f"HTTP {response.status_code}"])
                continue

            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type:
                fail_csv.writerow([idx, title, img_url, f"Not image: {content_type}"])
                continue

            image = Image.open(BytesIO(response.content))
            safe_title = title.replace(" ", "_")
            filename = f"{safe_title}{searchword}_{title}{idx}.jpg"
            filepath = os.path.join(save_folder, filename)
            image.save(filepath)

            print(f"저장 완료: {filepath}")
            success_csv.writerow([title, img_url])  # 성공한 경우 기록
            existing_urls.add(img_url)  # 중복 방지용 업데이트

        except Exception as e:
            print(f"[{idx}] 저장 실패 ({title}): {e}")
            fail_csv.writerow([idx, title, img_url, str(e)])

# 파일 닫기
success_writer.close()
fail_writer.close()
