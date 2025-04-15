import csv
import requests
from PIL import Image
from io import BytesIO
import os


def download_image(title, url, count):
    try:
        response = requests.get(url, timeout=40)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        ext = img.format.lower()
        filename = f'images/{title}_{count}.{ext}'
        img.save(filename)
        print(f"재시도 저장 완료: {filename}")
        return True

    except Exception as e:
        print(f"[재시도 실패] {title} ({url}): {e}")
        return False

# 실패 로그에서 'timeout' 만 필터링
retry_targets = []
with open('list/failed_requests.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if 'Read timed out' in row[3]:
            retry_targets.append((row[1], row[2]))  # (title, url)

# 이미지 폴더 없으면 생성
os.makedirs('list', exist_ok=True)

# 재시도
for i, (title, url) in enumerate(retry_targets, 1):
    download_image(title, url, i)