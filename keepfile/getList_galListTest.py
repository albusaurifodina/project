import os
import json
import urllib.request
import urllib.parse
import pandas as pd  # pandas 모듈

service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

def getDataFromWeb(url):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return response.read().decode('UTF-8')
    except Exception as err:
        print('크롤링 실패:', err)
        return None

def test_galleryList1():
    url = (
        'http://apis.data.go.kr/B551011/PhotoGalleryService1/galleryList1'
        f'?serviceKey={service_key}'
        f'&numOfRows=10'
        f'&pageNo=1'
        f'&MobileOS=ETC'
        f'&MobileApp=AppTest'
        f'&_type=json'
        f'&arrange=A'
    )
    raw_data = getDataFromWeb(url)
    print("응답 내용:\n", raw_data)

test_galleryList1()
