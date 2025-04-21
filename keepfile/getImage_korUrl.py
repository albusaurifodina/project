import urllib.request
import urllib.parse
import json

# 발급받은 서비스 키 (URL 인코딩되어 있어야 함)
service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

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
        for idx, item in enumerate(items, start=1):
            print(f"[{idx}] {item['originimgurl']}")
    else:
        print("데이터를 가져오지 못했습니다.")


# 테스트 호출 (예: contentId=1095732)
imageExtractor(contentId=1095732)
