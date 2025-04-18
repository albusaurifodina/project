import requests
import csv
import time

# ✅ 한국관광공사 API 인증키 입력
API_KEY = "YOUR_API_KEY_HERE"  # 여기에 본인의 인증키 입력하세요
URL = "http://apis.data.go.kr/B551011/PhotoGalleryService1/galleryDetailList1"

# 입력 파일 이름
INPUT_FILE = "content_ids.csv"
# 출력 파일 이름
VALID_FILE = "alid_ids.csv"
NO_IMAGE_FILE = "o_image_ids.csv"

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
        response = requests.get(URL, params=params, timeout=5)
        data = response.json()

        items = data.get("response", {}).get("body", {}).get("items", {})
        if not items or "list" not in items or not items["list"]:
            print(f"[{content_id}] ❌ 이미지 없음 또는 응답 비정상")
            no_image_ids.append({"title": title, "content_id": content_id})
        else:
            print(f"[{content_id}] ✅ 이미지 있음")
            valid_ids.append({"title": title, "content_id": content_id})

    except Exception as e:
        print(f"[{content_id}] ⚠️ 요청 실패: {e}")
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

print("\n🎉 완료! 이미지 있는/없는 콘텐츠 ID가 분리되어 저장되었습니다.")
