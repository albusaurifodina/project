'''
getList_kor_CategoryCode.py
국문관광정보 categoryCode1	서비스분류코드조회
'http://apis.data.go.kr/B551011/KorService1/categoryCode1'

filename = '../list/getList_korCategoryCode.csv # 파일명 체크필요
'''
import os
import json
import urllib.request
import pandas as pd  # pandas 모듈

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
    end_point = 'http://apis.data.go.kr/B551011/KorService1/categoryCode1'
    params = (
        f'?serviceKey={service_key}'
        f'&numOfRows={pageSize}'
        f'&pageNo={pageNumber}'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
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
                img_url = item.get('originimgurl')
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
            'code': onedict.get('code'),
            'name': onedict.get('name'),
            'rnum': onedict.get('rnum'),
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
    filename = '../list/getList_korCategoryCode.csv'
    listTable.to_csv(filename, index=False, encoding='UTF-8')
    print(f"{filename} 파일이 저장되었습니다.")
else:
    print("리스트 데이터를 처리할 수 없습니다.")