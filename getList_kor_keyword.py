'''
getList_kor_keyword.py
국문관광정보 TourAPI4.0 / searchKeyword1 / 키워드검색조회
키워드로 검색을 하여 관광타입별 또는 전체 목록을 조회하는 기능입니다.
파라미터에 따라 제목순, 수정일순(최신순), 등록일순 정렬검색을 제공합니다.
getList_kor_keyword_02.py 에서 페이지 자동생성 기능 추가

keyword = '검색 키워드'

사진없는 항목 제외된 리스트
f'csvlist/{키워드}_korS.csv'

사진없는 항목 리스트
f'csvlist/{키워드}_skipped_korS.csv'

['물놀이','해변', '해수욕장'] 등등
'''

import json
import urllib.request
import urllib.parse
import pandas as pd
import os

keyword = '해수욕장'
encoded_keyword = urllib.parse.quote(keyword)
service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'
pageSize = 100

# csvlist 폴더가 없으면 생성
if not os.path.exists("csvlist"):
    os.makedirs("csvlist")

def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('UTF-8')
    except Exception as err:
        print('크롤링 실패:', err)
        return None

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

    print(f"{pageNumber} 페이지 요청 중... URL: {url}")

    if raw_data:
        try:
            data = json.loads(raw_data)
            return data
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 에러: {e}")
            print(f"응답 원문:\n{raw_data}")
            return None
    return None

def makeListTable(raw_data):
    items = raw_data['response']['body']['items'].get('item', [])
    if isinstance(items, dict):
        items = [items]

    image_list, skipped_list = [], []
    for onedict in items:
        first_image = onedict.get("firstimage", "")
        row = {
            "TITLE": onedict.get("title", ""),
            "ADDR1": onedict.get("addr1", ""),
            "FIRST_IMG": first_image,
            "FIRST_IMG2": onedict.get("firstimage2", ""),
            "KEYID": onedict.get("contentid", ""),
            "KEYTYPE": onedict.get("contenttypeid", ""),
            "BOOKTOUR": onedict.get("booktour", ""),
            "ADR2": onedict.get("addr2", ""),
            "CAT1": onedict.get("cat1", ""),
            "CAT2": onedict.get("cat2", ""),
            "CAT3": onedict.get("cat3", ""),
            "CPYRIGHT": onedict.get("cpyrhtDivCd", ""),
            "GPSX": onedict.get("mapx", ""),
            "GPSY": onedict.get("mapy", ""),
            "MAPLEVEL": onedict.get("mlevel", ""),
            "CREATED": onedict.get("createdtime", ""),
            "MODIFIED": onedict.get("modifiedtime", ""),
            "TEL": onedict.get("tel", ""),
            "AREA1": onedict.get("areacode", ""),
            "AREA2": onedict.get("sigungucode", ""),
        }
        if first_image:
            image_list.append(row)
        else:
            skipped_list.append(row)

    return pd.DataFrame(image_list), pd.DataFrame(skipped_list)

def collect_all_pages():
    total_list = pd.DataFrame()
    total_skipped = pd.DataFrame()
    page = 1

    while True:
        data = listExtractor(page, pageSize)
        if not data:
            break

        # 안전하게 데이터 구조 확인
        try:
            items_data = data.get('response', {}).get('body', {}).get('items', {})
            items = items_data.get('item', [])
        except Exception as e:
            print(f"[!] {page} 페이지에서 데이터 구조 파싱 실패: {e}")
            break

        # items가 없으면 종료
        if not items:
            print(f"{page} 페이지에 더 이상 데이터가 없습니다.")
            break

        try:
            listTable, skippedList = makeListTable(data)
        except Exception as e:
            print(f"[!] {page} 페이지 makeListTable 처리 중 오류 발생: {e}")
            break

        total_list = pd.concat([total_list, listTable], ignore_index=True)
        total_skipped = pd.concat([total_skipped, skippedList], ignore_index=True)
        print(f"{page} 페이지 완료: 이미지 있음 {len(listTable)} / 없음 {len(skippedList)}")
        page += 1

    filename = f'csvlist/{keyword}_korS_total.csv'
    skipped_filename = f'csvlist/{keyword}_korS_skipped.csv'
    total_list.to_csv(filename, index=False, encoding='UTF-8')
    total_skipped.to_csv(skipped_filename, index=False, encoding='UTF-8')
    print(f"\n전체 리스트 저장 완료: {filename}")
    print(f"이미지 없는 항목 저장 완료: {skipped_filename}")

if __name__ == "__main__":
    collect_all_pages()
