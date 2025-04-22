'''
getList_gal_title_detail.py
PhotoGalleryService1/galleryDetailList1'
관광사진 갤러리 리스트 타이틀에 해당하는 사진의 목록을 .csv 로 저장
사진의 URL경로, 촬영월, 촬영장소 등의 내용

title = '타이틀'
filename = f'list/{타이틀}_Detail_galD{검색된 페이지 번호}.csv'
'''
import json
import urllib.request
import urllib.parse
import pandas as pd  # pandas 모듈

title = '윈드서핑'
encoded_title = urllib.parse.quote(title)

service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

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
    end_point = 'http://apis.data.go.kr/B551011/PhotoGalleryService1/galleryDetailList1'

    params = (
        f'?serviceKey={service_key}'
        f'&numOfRows={pageSize}'
        f'&pageNo={pageNumber}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&title={encoded_title}'
    )

    url = end_point + params
    raw_data = getDataFromWeb(url)

    print("최종 요청 URL:", url)
    print("응답 내용 확인:\n", raw_data)

    if raw_data:
        try:
            data = json.loads(raw_data)
            items = data['response']['body']['items']['item']
            if isinstance(items, dict):  # 단일 객체일 경우 리스트로 변환
                items = [items]
            for item in items:
                img_url = item.get('galWebImageUrl')
                img_name = item.get('imgname', '정보없음')
                cpyrht = item.get('cpyrhtDivCd', '알 수 없음')
            return data  # 전체 JSON 응답 반환
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
            "제목": onedict.get("galTitle", ""),
            "이미지URL": onedict.get("galWebImageUrl", ""),
            "촬영장소": onedict.get("galPhotographyLocation", ""),
            "사진작가": onedict.get("galPhotographer", ""),
            "검색키워드": onedict.get("galSearchKeyword", ""),
            "콘텐츠ID": onedict.get("galContentId", ""),
            "콘텐츠타입ID": onedict.get("galContentTypeId", ""),
            "등록일시": onedict.get("galCreatedtime", ""),
            "수정일시": onedict.get("galModifiedtime", "")
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
    filename = f'list/{title}_Detail_galD{pageNumber}.csv'
    listTable.to_csv(filename, index=False, encoding='UTF-8')
    print(f"{filename} 파일이 저장되었습니다.")
else:
    print("리스트 데이터를 처리할 수 없습니다.")