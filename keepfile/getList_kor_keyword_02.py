'''
getList_kor_keyword_02.py
국문관광정보 TourAPI4.0 / searchKeyword1 / 키워드검색조회
키워드로 검색을 하여 관광타입별 목록을 제공.

keyword = '검색 키워드'

사진없는 항목 제외된 리스트
f'csvlist/{키워드}_korS{페이지번호}.csv'

사진없는 항목 리스트
f'csvlist/{키워드}_skipped_korS{페이지번호}.csv'

['물놀이','해변', '해수욕장']
'''
import json
import urllib.request
import urllib.parse
import pandas as pd  # pandas 모듈

keyword = '해수욕장'
encoded_keyword = urllib.parse.quote(keyword)
service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'
pageNumber = 3
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
    end_point = 'http://apis.data.go.kr/B551011/KorService1/searchKeyword1'

    params = (
        f'?serviceKey={service_key}'
        f'&numOfRows={pageSize}'
        f'&pageNo={pageNumber}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&arrange=C'
        f'&keyword={encoded_keyword}'
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
skippedList = pd.DataFrame()  # 이미지 없는 항목 저장용

# JSON 데이터를 판다스 데이터프레임으로 변환하는 함수
def makeListTable(raw_data):
    global listTable, skippedList
    print('listTable 정보를 데이터프레임에 저장 중...')
    items = raw_data['response']['body']['items']['item']
    if isinstance(items, dict):
        items = [items]

    for onedict in items:
        first_image = onedict.get("firstimage", "")
        row_dict = {
            "콘텐츠제목": onedict.get("title", ""),
            "주소": onedict.get("addr1", ""),
            "대표이미지(원본)": first_image,
            "대표이미지(썸네일)": onedict.get("firstimage2", ""),
            "콘텐츠ID": onedict.get("contentid", ""),
            "콘텐츠타입ID": onedict.get("contenttypeid", ""),
            "교과서속여행지": onedict.get("booktour", ""),
            "상세주소": onedict.get("addr2", ""),
            "대분류": onedict.get("cat1", ""),
            "중분류": onedict.get("cat2", ""),
            "소분류": onedict.get("cat3", ""),
            "저작권유형": onedict.get("cpyrhtDivCd", ""),
            "GPSX좌표": onedict.get("mapx", ""),
            "GPSY좌표 ": onedict.get("mapy", ""),
            "MAP레벨": onedict.get("mlevel", ""),
            "등록일": onedict.get("createdtime", ""),
            "수정일": onedict.get("modifiedtime", ""),
            "전화번호": onedict.get("tel", ""),
            "지역코드": onedict.get("areacode", ""),
            "시군구코드": onedict.get("sigungucode", ""),
        }
        row = pd.DataFrame(row_dict, index=[0])
        if first_image:  # 이미지가 있는 경우
            listTable = pd.concat([listTable, row], ignore_index=True)
        else:  # 이미지가 없는 경우
            skippedList = pd.concat([skippedList, row], ignore_index=True)


# 메인 실행 파트
print('크롤링 중입니다. 잠시만 기다려 주세요...')
list_Data = listExtractor(pageNumber, pageSize)

if list_Data:
    makeListTable(list_Data)  # <- 이 부분 꼭 호출해야 데이터프레임이 만들어져요!

    # CSV로 저장
    filename = f'csvlist/{keyword}_korS{pageNumber}.csv'
    skipped_filename = f'csvlist/{keyword}_skipped_korS{pageNumber}.csv'

    listTable.to_csv(filename, index=False, encoding='UTF-8')
    print(f"{filename} 파일이 저장되었습니다.")

    # 이미지 없는 항목 따로 저장
    if not skippedList.empty:
        skippedList.to_csv(skipped_filename, index=False, encoding='UTF-8')
        print(f"이미지 없는 항목은 {skipped_filename} 파일에 저장되었습니다.")
else:
    print("데이터를 가져오지 못했습니다.")
