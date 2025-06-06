import time
import random

# 수정된 save_image_from_url 함수
def save_image_from_url(img_url, save_dir='images', filename=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, filename)
    try:
        urllib.request.urlretrieve(img_url, save_path)
        print(f"[✔] 저장 완료: {save_path}")
        return True
    except Exception as e:
        print(f"[✘] 저장 실패: {e}")
        return False

# 콘텐츠 ID 하나로 이미지 추출
def imageExtractor(contentId, title, pageNumber=1, pageSize=100):
    try:
        end_point = 'http://apis.data.go.kr/B551011/KorService1/detailImage1'
        params = (
            f'?serviceKey={service_key}'
            f'&MobileOS=ETC&MobileApp=AppTest&_type=json'
            f'&contentId={contentId}&imageYN=Y&subImageYN=Y'
            f'&numOfRows={pageSize}&pageNo={pageNumber}'
        )
        url = end_point + params
        raw_data = getDataFromWeb(url)
        if not raw_data:
            print(f"[!] 콘텐츠 ID {contentId}: 응답 없음")
            return

        data = json.loads(raw_data)
        items = data['response']['body']['items'].get('item', [])
        if isinstance(items, dict):
            items = [items]

        for idx, item in enumerate(items):
            img_url = item.get('originimgurl')
            if not img_url:
                print(f"[!] 이미지 URL 없음 (contentId={contentId})")
                continue
            safe_title = "".join(c for c in title if c.isalnum())
            filename = f"{safe_title}_{contentId}_{idx + 1}.jpg"
            save_image_from_url(img_url, save_dir=save_dir, filename=filename)
            time.sleep(random.uniform(0.3, 0.8))  # 과부하 방지용 지연
    except Exception as e:
        print(f"[!] 예외 발생 (contentId={contentId}): {e}")

# 진행된 인덱스 저장 로직 추가
for idx, row in df.iterrows():
    try:
        content_id = row['KEYID']
        title = row['TITLE']
        print(f"→ [{idx + 1}/{len(df)}] 콘텐츠 ID: {content_id}")
        imageExtractor(content_id, title)
    except Exception as e:
        print(f"[!] 반복 중 에러 (idx={idx}): {e}")
        continue
