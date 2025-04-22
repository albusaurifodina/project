'''
getImage_unsplash.py 파일 # 파일명 변경시 같이 변경 요망

https://unsplash.com/ko unsplash.com 사이트 에서 이미지 가져오는 파일
url = "https://api.unsplash.com/search/photos"

생성파일 이름 {QUERY}{i+1}.jpg
QUERY = "korean beach"  # 검색어 (한국어 '바닷가'도 가능)
PER_PAGE = 30  # 가져올 이미지 수
SAVE_DIR = "./../../unsplash_beach"

License
Privacy Policy
Cookie Policy
Terms & Conditions
API Terms
Unsplash+ License
Unsplash+ Terms
License
Unsplash visuals are made to be used freely. Our license reflects that.

All images can be downloaded and used for free
Commercial and non-commercial purposes
No permission needed (though attribution is appreciated!)
What is not permitted
Images cannot be sold without significant modification.
Compiling images from Unsplash to replicate a similar or competing service.
Tip: How to give attribution
Even though attribution isn’t required, Unsplash photographers appreciate it as it provides exposure to their work and encourages them to continue sharing.

Photo by Jeremy Bishop on Unsplash

Longform
Unsplash grants you an irrevocable, nonexclusive, worldwide copyright license to download, copy, modify, distribute, perform, and use images from Unsplash for free, including for commercial purposes, without permission from or attributing the photographer or Unsplash. This license does not include the right to compile images from Unsplash to replicate a similar or competing service.
'''

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




