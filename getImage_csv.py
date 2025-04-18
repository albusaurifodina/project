'''
getImage_csv.py 파일 /.csv 리스트로부터 이미지 추출
원본 파일이 너무 산만해서 keepfile 폴더로 옮기고 이 파일은 gpt 에게 정리 부탁해서 새로 생성

폴더, 생성 파일 이름과 path 꼭 확인할 것
CSV_PATH = './csvlist/list_물놀이_galS1.csv'  # 입력 CSV 경로
생성파일 이름 = f"{safe_title}_{SOURCE}_{SEARCH_WORD}{idx}.jpg"
SAVE_DIR = 'images/' # 이미지 저장 폴더
'''
import os
import csv
import requests
import urllib.parse
from PIL import Image
from io import BytesIO

# ====================== 설정 ============================
SOURCE = 'gal3'       # 이미지 출처 구분 ('gal1', 'kor' 등)
SEARCH_WORD = '물놀이' # 키워드 (예: 물놀이, 수상레저 등)
ENCODED_SEARCHWORD = urllib.parse.quote(SEARCH_WORD)

CSV_PATH = './csvlist/list_물놀이_galS3.csv'  # 입력 CSV 경로
SAVE_DIR = 'images_test2/'# 이미지 저장 폴더

# 저장 폴더 준비
os.makedirs(SAVE_DIR, exist_ok=True)
# ==================== 함수 정의 ==========================

def clean_filename(title: str) -> str:
    """파일 이름에 쓸 수 있도록 문자열 정리"""
    return title.replace(" ", "_").replace("/", "_")

def is_valid_image_response(response) -> bool:
    """요청 응답이 이미지인지 검사"""
    content_type = response.headers.get('Content-Type', '')
    return 'image' in content_type

def save_image_from_url(img_url: str, filename: str, idx: int) -> None:
    """이미지를 URL에서 받아 저장"""
    try:
        response = requests.get(img_url, timeout=20, allow_redirects=True)

        if response.status_code != 200:
            print(f"[{idx}] 요청 실패 ({response.status_code}) → {img_url}")
            return

        if response.url != img_url:
            print(f"[{idx}] 리다이렉트 발생 → 최종 URL: {response.url}")

        if not is_valid_image_response(response):
            print(f"[{idx}] 이미지 아님 (Content-Type: {response.headers.get('Content-Type')}) → {img_url}")
            return

        image = Image.open(BytesIO(response.content))
        filepath = os.path.join(SAVE_DIR, filename)
        image.save(filepath)

        print(f"[{idx}] 저장 완료: {filepath}")

    except Exception as e:
        print(f"[{idx}] 저장 실패: {e}")

# ===================== 실행 로직 ==========================

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    for idx, row in enumerate(reader):
        if idx == 0:
            continue  # 헤더 건너뜀

        if len(row) < 2:
            print(f"[{idx}] 열이 부족하여 건너뜀: {row}")
            continue

        title, img_url = row[0].strip(), row[2].strip()
        safe_title = clean_filename(title)
        filename = f"{safe_title}_{SOURCE}_{SEARCH_WORD}_{idx}.jpg"

        save_image_from_url(img_url, filename, idx)