import json
import urllib.request
import urllib.parse
import pandas as pd  # pandas 모듈

'''
국문관광정보 TourAPI4.0 / 11  detailImage1/  이미지정보조회 (상세정보4)
각관광타입(관광지, 숙박등)에해당하는이미지URL 목록을조회하는기능입니다.
http://apis.data.go.kr/B551011/KorService1/detailImage1
f'&contentId={contentId}'
contentId=키워드 리스트(예/물놀이 리스트)의 개별 상세이미지 리스트 생성
컨텐츠 아이디에 해당하는 이미지가 없을 경우를 위해 코딩추가
'''

service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

contentId = 3006242
keyword1 = '수상레저'
keyword2 = '모비딕수상레저'
encoded_keyword = urllib.parse.quote(keyword1,keyword2)

pageNumber = 1
pageSize = 100

# 웹페이지에서 데이터를 가져오는 함수
def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('UTF-8')
    except Exception as err:
        print('크롤링 실패:', err)
        return None


# 이미지 리스트와 정보 추출 함수
def listExtractor(pageNumber, pageSize):
    end_point = 'http://apis.data.go.kr/B551011/KorService1/detailImage1'

    params = (
        f'?serviceKey={service_key}'
        f'&numOfRows={pageSize}'
        f'&pageNo={pageNumber}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&contentId={contentId}'
        f'&imageYN=Y'
        f'&subImageYN=Y'
    )

    url = end_point + params
    raw_data = getDataFromWeb(url)

    print("최종 요청 URL:", url)
    print("응답 내용 확인:\n", raw_data)

    if raw_data:
        try:
            data = json.loads(raw_data)
            items_raw = data['response']['body'].get('items')

            # 데이터가 없거나 잘못된 경우 처리
            if not isinstance(items_raw, dict) or 'item' not in items_raw:
                print(f"[{contentId}] 이미지 없음 또는 응답 비정상")
                return None

            items = items_raw['item']
            if isinstance(items, dict):  # 단일 이미지일 경우
                items = [items]

            for item in items:
                img_url = item.get('originimgurl')
                # 필요한 정보 추출 가능

            return data
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 에러: {e}")
            print("응답 내용:\n", raw_data)
    else:
        print("데이터를 가져오지 못했습니다.")
    return None

# 이미지 정보를 저장할 데이터프레임
listTable = pd.DataFrame()

# JSON 데이터를 판다스 데이터프레임으로 변환하는 함수
def makeListTable(listData):
    global listTable
    print('listTable 정보를 데이터프레임에 저장 중...')
    items = listData['response']['body']['items']['item']
    if isinstance(items, dict):
        items = [items]

    for onedict in items:
        onedict = {
            "콘텐츠제목": onedict.get("title", ""),
            "콘텐츠ID": onedict.get("contentid", ""),
            "이미지이름": onedict.get("imgname", ""),
            "이미지주소": onedict.get("originmgurl", ""),
            "저작권": onedict.get("cpyrhtDivCd", ""),
            "썸네일이미지주소": onedict.get("smallimageurl", ""),
        }
        row = pd.DataFrame(onedict, index=[0])
        listTable = pd.concat([listTable, row], ignore_index=True)

# 메인 실행 파트
print('크롤링 중입니다. 잠시만 기다려 주세요...')
list_Data = listExtractor(pageNumber, pageSize)

if list_Data:
    total_count = list_Data['response']['body'].get('totalCount')
    print(f"total_count : {total_count}")
    makeListTable(list_Data)

    # CSV로 저장
    filename = f'list/{keyword1}_{keyword2}_korD{pageNumber}.csv'
    listTable.to_csv(filename, index=False, encoding='UTF-8')
    print(f"{filename} 파일이 저장되었습니다.")
else:
    print("리스트 데이터를 처리할 수 없습니다.")