'''
com_file_name_meta2.py  폴더 path 꼭 확인
특정 폴더안의 파일 이름을 변경하고 meta 데이타는 csv 로 저장
한글과 특수문자 제거 후 숫자 2개 추출(컨텐츠 아이디와 이미지 고유 아이디 추출기능)
생성파일 = img_metadata2.csv' 생성화일 이름 과 생성 path 꼭 확인할 것

com_file_name_meta.py 파일과 다른점.
conid = numbers[-2] if numbers else 'contentId'
img_id = numbers[-1] if numbers else 'imageId'

com_file_name_meta2.py 의 생성파일 img_metadata2.csv
filename,tag,title,conid,img_id
3006242_3000405.jpg,unknown,unknown,3006242,3000405 #
3006242_3000409.jpg,unknown,unknown,3006242,3000409

com_file_name_meta.py 의 생성파일 img_metadata.csv
filename,conid,img_id
3006242_3000405.jpg,3006242,3000405 한글이 빠지고 변경된 파일이름 과 추출된 컨텐츠 아이디와 이미지 아이디
'''
import os
import re
import csv

def parse_filename(filename):
    # 예: 서핑_모비딕_3006242_3000419.jpg
    base = os.path.splitext(filename)[0]
    parts = re.split(r'[_\W]+', base)

    # 숫자 2개는 conid, img_id로 추정
    numbers = [p for p in parts if p.isdigit()]
    texts = [p for p in parts if not p.isdigit()]

    if len(numbers) >= 2:
        conid = numbers[-2] if numbers else 'contentId'
        img_id = numbers[-1] if numbers else 'imageId'
        tag = texts[0] if texts else 'unknown'
        title = texts[1] if len(texts) > 1 else 'unknown'
        return conid, img_id, tag, title
    return None, None, None, None


def rename_files_and_extract_metadata(img_dir='./../images_test', csv_path='./../csvlist/etc/img_metadata2.csv'):
    metadata = []

    for filename in os.listdir(img_dir):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            conid, img_id, tag, title = parse_filename(filename)
            if conid and img_id:
                new_filename = f"{conid}_{img_id}.jpg"
                old_path = os.path.join(img_dir, filename)
                new_path = os.path.join(img_dir, new_filename)

                # 파일명 바꾸기 (중복 체크)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"파일명 변경: {filename} → {new_filename}")
                else:
                    print(f"이미 존재: {new_filename}, 기존 유지")

                metadata.append([new_filename, tag, title, conid, img_id])
            else:
                print(f"ID 추출 실패: {filename}")

    # 메타데이터 저장
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'tag', 'title', 'conid', 'img_id'])
        writer.writerows(metadata)

    print(f"\n📄 메타데이터 저장 완료: {csv_path}")


# 실행
rename_files_and_extract_metadata()
