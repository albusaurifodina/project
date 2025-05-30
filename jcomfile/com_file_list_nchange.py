'''
com_file_list_nchange.py 파일
폴더 속 파일과 폴더 정보를 리스트로 추출 & 이름바꾸기

dir_name = "project" # 시작 폴더 경로 설정
root_dir = f"./../../{dir_name}"  # 원하는 경로로 바꿔주세요
output_csv = f"./../csvlist/etc/{dir_name}_list.csv"
'''
import datetime
import os
import csv

dir_name = "day&" # 시작 폴더 경로 설정
root_dir = f"./../../../0_NOTE/day&/"  # 원하는 경로로 바꿔주세요
output_csv = f"./../../../0_NOTE/{dir_name}/{dir_name}.csv"
exclude_dirs = {'.git', '__pycache__', '.ipynb_checkpoints', 'venv', '.venv', 'node_modules', '.vscode', '.idea'}
include_extensions = {'.jpg', '.png', '.py', '.csv', '.txt'}  # 원하는 확장자
include_keywords = {'프로젝트_202504'} # 파일명에 포함된 키워드

# 이름 변경 설정
rename_enabled = True
rename_mode = "replace"  # "prefix", "suffix", "replace"
rename_value = ""  # 접두사/접미사 혹은 교체할 단어
replace_from = "프로젝트_202504"       # replace 모드에서 바꿀 단어
replace_to = "04.txt"         # replace 모드에서 교체할 단어

# 결과 저장 리스트
file_list = []

# 탐색 및 필터링
for folder_path, dirs, files in os.walk(root_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]

    for file_name in files:
        ext = os.path.splitext(file_name)[1].lower()

        if include_extensions and ext not in include_extensions:
            continue
        if include_keywords and not any(kw in file_name for kw in include_keywords):
            continue

        original_full_path = os.path.join(folder_path, file_name)
        new_file_name = file_name

        # 이름 변경
        if rename_enabled:
            if rename_mode == "prefix":
                new_file_name = rename_value + file_name
            elif rename_mode == "suffix":
                name, ext = os.path.splitext(file_name)
                new_file_name = name + rename_value + ext
            elif rename_mode == "replace":
                new_file_name = file_name.replace(replace_from, replace_to)

            new_full_path = os.path.join(folder_path, new_file_name)

            try:
                os.rename(original_full_path, new_full_path)
                print(f"이름 변경: {file_name} -> {new_file_name}")
            except Exception as e:
                print(f"이름 변경 실패: {file_name} - {e}")
                continue
        else:
            new_full_path = original_full_path

        try:
            stat = os.stat(new_full_path)
            file_info = {
                "파일명": new_file_name,
                # "파일 크기(Bytes)": stat.st_size,
                # "최종 수정일": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                # "전체 경로": new_full_path
            }
            file_list.append(file_info)
        except Exception as e:
            print(f"오류: {new_full_path} - {e}")

# CSV 저장
if file_list:
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, mode='w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=file_list[0].keys())
        writer.writeheader()
        writer.writerows(file_list)

    print(f"필터링된 파일 목록이 {output_csv}에 저장되었습니다.")
else:
    print("조건에 맞는 파일이 없습니다.")

