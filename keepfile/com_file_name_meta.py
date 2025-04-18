'''
com_file_name_meta.py
특정 폴더안의 파일 이름을 변경하고 meta 데이타는 csv 로 저장
한글과 특수문자 제거 후 숫자 2개 추출(컨텐츠 아이디와 이미지 고유 아이디 추출기능)

생성파일 = img_metadata.csv'
filename,conid,img_id
3006242_3000405.jpg,3006242,3000405 한글이 빠지고 변경된 파일이름 과 추출된 컨텐츠 아이디와 이미지 아이디
'''
import os
import re
import csv

def extract_ids(filename):
    # 한글과 특수문자 제거 후 숫자 2개 추출
    numbers = re.findall(r'\d+', filename)
    if len(numbers) >= 2:
        return numbers[-2], numbers[-1]  # conid, img_id
    return None, None

def rename_files_and_create_metadata(img_dir='./../images_test', csv_path='./../csvlist/etc/img_metadata.csv'):
    metadata = []

    for filename in os.listdir(img_dir):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            conid, img_id = extract_ids(filename)
            if conid and img_id:
                new_filename = f"{conid}_{img_id}.jpg"
                old_path = os.path.join(img_dir, filename)
                new_path = os.path.join(img_dir, new_filename)

                if not os.path.exists(new_path):  # 이름 충돌 방지
                    os.rename(old_path, new_path)
                    print(f"파일명 변경: {filename} → {new_filename}")
                else:
                    print(f"이미 존재: {new_filename}, 기존 유지")

                metadata.append([new_filename, conid, img_id])
            else:
                print(f"ID 추출 실패: {filename}")

    # 메타데이터 저장
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'conid', 'img_id'])
        writer.writerows(metadata)

    print(f"\n📄 메타데이터 저장 완료: {csv_path}")

# 실행
rename_files_and_create_metadata()
