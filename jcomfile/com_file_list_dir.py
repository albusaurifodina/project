'''
com_file_list_dir.py 파일
폴더 속 파일과 폴더 정보를 리스트로 추출하는 파일

타겟 폴더, 생성 파일 이름과 path 꼭 확인할 것
root_dir = r"./../../project/keepfile" 타겟 폴더
output_csv = f"./../csvlist/etc/list_keepfile_202504.csv" 생성 파일
'''
import os
import csv
from datetime import datetime

# 설정
root_dir = r"./../../project/keepfile"
output_csv = f"./../csvlist/etc/list_keepfile_20250418.csv"

exclude_dirs = {'.git', '__pycache__', '.ipynb_checkpoints', 'venv', '.venv'}

file_list = []

for folder_path, dirs, files in os.walk(root_dir):
    # 제외할 폴더 제거
    dirs[:] = [d for d in dirs if d not in exclude_dirs]

    # 폴더 정보 저장
    for d in dirs:
        dir_path = os.path.join(folder_path, d)
        try:
            stat = os.stat(dir_path)
            file_info = {
                "이름": d,
                "타입": "폴더",
                # "최종 수정일": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                # "전체 경로": dir_path
            }
            file_list.append(file_info)
        except Exception as e:
            print(f"폴더 오류: {dir_path} - {e}")

    # 파일 정보 저장
    for f in files:
        file_path = os.path.join(folder_path, f)
        try:
            stat = os.stat(file_path)
            file_info = {
                "이름": f,
                "타입": "파일",
                # "최종 수정일": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                # "전체 경로": file_path
            }
            file_list.append(file_info)
        except Exception as e:
            print(f"파일 오류: {file_path} - {e}")

# CSV로 저장
if file_list:
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=file_list[0].keys())
        writer.writeheader()
        writer.writerows(file_list)

    print(f"파일 + 폴더 목록이 {output_csv}에 저장되었습니다.")
else:
    print("저장할 정보가 없습니다.")
