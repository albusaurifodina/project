import urllib.request
import urllib.parse
import json
import os

# 발급받은 서비스 키 (URL 인코딩되어 있어야 함)
service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

# 이미지 저장 함수
def save_image_from_url(img_url, save_dir='./images/', filename=None):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not filename:
        filename = os.path.basename(img_url)  # 이미지 URL에서 파일 이름 추출
        save_path = os.path.join(save_dir, filename)
    try:
        urllib.request.urlretrieve(img_url, save_path)
        print(f"이미지 저장 완료: {save_path}")
    except Exception as e:
        print(f"이미지 저장 실패: {e}")


# 웹에서 데이터 요청
def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
    except Exception as err:
        print("크롤링 실패:", err)
        return None


# 이미지 정보 추출
def imageExtractor(contentId, pageNumber=1, pageSize=10):
    end_point = 'http://apis.data.go.kr/B551011/KorService1/detailImage1'
    params = (
        f'?serviceKey={service_key}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&contentId={contentId}'
        f'&imageYN=Y'
        f'&subImageYN=Y'
        f'&numOfRows={pageSize}'
        f'&pageNo={pageNumber}'
    )

    url = end_point + params
    raw_data = getDataFromWeb(url)

    if raw_data:
        data = json.loads(raw_data)
        items = data['response']['body']['items']['item']
        for item in items:
            img_url = item['originimgurl']
            save_image_from_url(img_url)
    else:
        print("데이터를 가져오지 못했습니다.")


# 테스트 호출 (예: contentId=1095732)
imageExtractor(contentId=1095732)
