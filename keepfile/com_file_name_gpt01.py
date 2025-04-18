'''
com_file_name_gpt01
.py gpt_파일이름 정리 예시들
gpt가 알려준 파일이름 조정 예시들 예시 컨텐츠아이디, 키워드, 이미지_url
# 자꾸 엉뚱한 파일을 쳐다보고 있는 상황이 계속되고 있어서 앞으로는 파일 맨 위에 파일 이름을 적어두는게 나을 것 같음..
'''

conid = 1010101
keyword = f'(검색키워드 ex) 모비딕_수상레저){conid}'
img_url = 'from csv list or conid'
'''
1. 파일 이름에서 숫자 외의 문자 제거하기
예: 3000415_image2_1.jpg ➝ 3000415.jpg (지금처럼), 또는
abc3000415_xyz.jpg ➝ 3000415.jpg ← 숫자만 추출하는 방식
'''
import os, re
original_name = os.path.basename(img_url)
numbers_only = re.findall(r'\d+', original_name)
if numbers_only:
    name_only = numbers_only[0]  # 가장 앞에 나오는 숫자만 사용
    filename = f"{keyword}_{name_only}.jpg"

'''
2. URL 경로에서 특정 위치 정보만 추출
예: URL이 이런 식이라면
http://example.com/gallery/3000419/image2_1.jpg
경로 중 gallery/3000419/만 파일 이름에 넣고 싶을 수도 있죠.
'''
url_parts = img_url.split('/')
folder_id = url_parts[-2]  # '3000419'
filename = f"{keyword}_{folder_id}.jpg"

'''
3. 시간 정보, 날짜 정보, 카테고리 정보 등을 자동 추가
결과 예) 모비딕_수상레저_3006242_3000419_20250418_142301.jpg
'''
from datetime import datetime
now = datetime.now().strftime('%Y%m%d_%H%M%S')  # 예: 20250418_142301
filename = f"{keyword}_{name_only}_{now}.jpg"

'''
4. 중복 방지용 해시 추가
혹시나 파일명이 겹치지 않게 하려면 URL을 해싱해서 파일명 뒤에 붙일 수도 있어요.
결과 예) 모비딕_수상레저_3006242_3000419_a1b2c3d4.jpg
'''
import hashlib
hash = hashlib.md5(img_url.encode()).hexdigest()[:8]  # 앞 8글자만 사용
filename = f"{keyword}_{name_only}_{hash}.jpg"

'''
5. 함수 만들기 🔄 이렇게 하면 좋은 점:
keyword 만들 때 복잡한 포맷 문자열 안 써도 되고,
키워드 생성 방식이 바뀌어도 함수 하나만 수정하면 됨!
그리고 다른 이미지 저장에서도 재사용 가능! (재활용 100% 😎)
'''
def make_keyword(title, tag, conid):
    return f"{title}_{tag}_{conid}"

keyword = make_keyword('모비딕', '수상레저', 3006242)

# 혹은 컨텐츠 딕셔너리를 쓰고 있다면(?)
content_info = {
    'title': '모비딕',
    'tag': '수상레저',
    'conid': 3006242
}
keyword = make_keyword(**content_info)  # 언팩해서 넘기기

'''
6. 한걸음 더: 폴더도 자동으로 나누고 싶다면?
결과: 키워드: 모비딕_수상레저_3006242
저장 디렉토리: images/수상레저/모비딕/
'''
def make_paths(base_dir, title, tag, conid):
    keyword = f"{title}_{tag}_{conid}"
    save_dir = os.path.join(base_dir, tag, title)
    return keyword, save_dir

keyword, save_dir = make_paths('images', '모비딕', '수상레저', 3006242)









