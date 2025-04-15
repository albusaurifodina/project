import requests
import os

# 예제 이미지 URL과 제목
img_url = "https://example.com/image.jpg"
img_title = "아름다운경치"

# 저장 폴더 생성
save_dir = "./images"
os.makedirs(save_dir, exist_ok=True)

# 이미지 다운로드 및 저장
response = requests.get(img_url)
if response.status_code == 200:
    with open(os.path.join(save_dir, f"{img_title}.jpg"), "wb") as f:
        f.write(response.content)
        print("이미지 저장 완료!")
