import os
import csv
from datetime import datetime

# 시작 폴더 경로 설정
root_dir = r".."  # 원하는 경로로 바꿔주세요
output_csv = f"./list/etc/list_project_file_20250417.csv"

# 결과 저장 리스트
file_list = []

# 폴더 탐색
for folder_path, dirs, files in os.walk(root_dir):
    for file_name in files:
        full_path = os.path.join(folder_path, file_name)
        try:
            stat = os.stat(full_path)
            file_info = {
                "파일명": file_name,
                # "파일 크기(Bytes)": stat.st_size,
                # "최종 수정일": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                # "전체 경로": full_path
            }
            file_list.append(file_info)
        except Exception as e:
            print(f"오류: {full_path} - {e}")

# CSV로 저장
with open(output_csv, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=file_list[0].keys())
    writer.writeheader()
    writer.writerows(file_list)

print(f"파일 목록이 {output_csv}에 저장되었습니다.")
