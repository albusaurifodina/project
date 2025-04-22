'''
getList_kor_Check_avaliability.py
국문관광정보 리스트의 상세이미지 정보가 저장가능한지 조회
http://apis.data.go.kr/B551011/KorService1/detailImage1

filename = '../list/getList_korCategoryCode.csv # 파일명 체크필요
'''
import requests
import csv
import time

# 한국관광공사 API 인증키 입력
API_KEY = "azksr7Fgk8fnWawWSRq/Rzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J+YdJm4QcpiSAGRw=="
URL = "http://apis.data.go.kr/B551011/KorService1/detailImage1"

# 입력 파일 이름
INPUT_FILE = "csvlist/list.csv"
# 출력 파일 이름
VALID_FILE = "csvlist/etc/valid_ids.csv"
NO_IMAGE_FILE ="csvlist/etc/no_img_ids.csv"

valid_ids = []
no_image_ids = []

# 1. 콘텐츠 ID 목록 불러오기
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    content_list = [row for row in reader]

# 2. API 요청하여 이미지 유무 확인
for item in content_list:
    title = item["title"]
    content_id = item["content_id"]

    params = {
        "serviceKey": API_KEY,
        "numOfRows": 10,
        "MobileOS": "ETC",
        "MobileApp": "TestApp",
        "contentId": content_id,
        "_type": "json"
    }

    try:
        response = requests.get(URL, params=params, timeout=30)
        print(f"[{content_id}] 응답 내용: {response.text}")  # ← 여기 추가
        data = response.json()

        items = data.get("response", {}).get("body", {}).get("items", {})
        if not items or "list" not in items or not items["list"]:
            print(f"[{content_id}] 이미지 없음 또는 응답 비정상")
            no_image_ids.append({"title": title, "content_id": content_id})
        else:
            print(f"[{content_id}] 이미지 있음")
            valid_ids.append({"title": title, "content_id": content_id})

    except Exception as e:
        print(f"[{content_id}] 요청 실패: {e}")
        no_image_ids.append({"title": title, "content_id": content_id})

    time.sleep(0.3)  # API 호출 간 간격

# 3. 결과 저장
with open(VALID_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "content_id"])
    writer.writeheader()
    writer.writerows(valid_ids)

with open(NO_IMAGE_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "content_id"])
    writer.writeheader()
    writer.writerows(no_image_ids)

print("완료! 이미지 있는/없는 콘텐츠 ID가 분리되어 저장되었습니다.")