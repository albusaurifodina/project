import os
import requests

# Unsplash API 정보
ACCESS_KEY = "Ibvsh6VgZj8iyHwag77VN21bvCt92audKaE4bmQJYTM"  # Unsplash 개발자 페이지에서 발급
QUERY = "korean beach"  # 검색어 (한국어 '바닷가'도 가능)
PER_PAGE = 30  # 가져올 이미지 수
SAVE_DIR = "./../../unsplash_beach"


# 저장 폴더 만들기
os.makedirs(SAVE_DIR, exist_ok=True)

# API 요청
url = "https://api.unsplash.com/search/photos"
params = {
    "query": QUERY,
    "page": 3,
    "per_page": PER_PAGE,
    "client_id": ACCESS_KEY
}

response = requests.get(url, params=params)

data = response.json()

# 이미지 저장
for i, result in enumerate(data["results"]):
    img_url = result["urls"]["regular"]
    img_data = requests.get(img_url).content
    with open(os.path.join(SAVE_DIR, f"3{QUERY}{i+1}.jpg"), "wb") as f:
        f.write(img_data)
    print(f"{i+1}번 이미지 저장 완료")



