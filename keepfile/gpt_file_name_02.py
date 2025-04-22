'''
gpt_file_name_02
### **1. 이미지 중복 여부를 파일명에서 구별 가능하게 하기**
즉, 파일명에 "검색 키워드"도 명시해서, **같은 `conid`라도 어떤 키워드로 찾았는지** 구분할 수 있게! 이렇게 하면 동일한 conid라도 검색 키워드 기준으로 나눠 저장이 되니까 **중복 여부 확인도 되고**,
**분류 히스토리 추적도 가능**해져요.

예: 서핑_3006242.jpg , 물놀이_3006242.jpg

### **2. 검색 키워드별로 하위 폴더 정리 (선택사항)**
이건 지금 당장은 안 쓰셔도 되지만, 나중에 정리가 필요해졌을 때 이런 식으로도 가능해요:

images/
├── 서핑/
│   ├── 3006242.jpg
│   └── 3009999.jpg
├── 물놀이/
│   └── 3006242.jpg
'''

# 예)
conid = 1010101
keyword = f'(검색키워드 ex) 모비딕_수상레저){conid}'
search_keyword = keyword # 통일이 좀 안돼고 있기는 한...참..답답한 상황
img_url = 'from csv list or conid'

#### 적용 코드 예시:
def make_keyword(search_keyword, conid):
    return f"{search_keyword}_{conid}"  # 예: '물놀이_3006242'

'''
혹시 **같은 conid인데 이미지 내용도 완전 똑같은지 알고 싶을 때**, 해시를 붙이면 좋습니다.
## 보너스 꿀팁: 중복 이미지 비교용 해시 붙이기 (optional)
같은 conid, 같은 키워드라도 이미지 해시가 다르면 "다른 이미지다!" 라는 걸 구분할 수 있어요 '''

import hashlib, urllib

def get_image_hash(img_url):
    try:
        with urllib.request.urlopen(img_url) as response:
            data = response.read()
            return hashlib.md5(data).hexdigest()[:8]  # 앞 8자리 해시
    except:
        return 'nohash'

# 그 후 파일명에 추가:
img_hash = get_image_hash(img_url)
filename = f"{search_keyword}_{conid}_{img_hash}.jpg"

# ========================================================== #

'''## 🛠️ 최종 예시 코드: 중복 conid 관리 + 키워드 구분 + 이미지 해시 '''
import os
import urllib.request
import hashlib

def make_keyword(search_keyword, conid):
    return f"{search_keyword}_{conid}"

def get_image_hash(img_url):
    try:
        with urllib.request.urlopen(img_url) as response:
            data = response.read()
            return hashlib.md5(data).hexdigest()[:8]
    except:
        return 'nohash'
# ----------------------------- 이건..이미 하고 있기는 한데..걍..냅두기
def save_image_from_url(img_url, search_keyword, conid, base_dir='images'):
    keyword = make_keyword(search_keyword, conid)
    img_hash = get_image_hash(img_url)

    # 하위 폴더에 키워드별로 정리
    save_dir = os.path.join(base_dir, search_keyword)
    os.makedirs(save_dir, exist_ok=True)

    # 파일명 = 키워드 + conid + 해시
    filename = f"{keyword}_{img_hash}.jpg"
    save_path = os.path.join(save_dir, filename)

    try:
        urllib.request.urlretrieve(img_url, save_path)
        print(f"이미지 저장 완료: {save_path}")
    except Exception as e:
        print(f"이미지 저장 실패: {e}")

### 사용 예:
img_url = 'http://example.com/3000415_image2_1.jpg'
search_keyword = '물놀이'
conid = 3006242
save_image_from_url(img_url, search_keyword, conid)
### 저장 결과 예: images/물놀이/물놀이_3006242_a1b2c3d4.jpg
