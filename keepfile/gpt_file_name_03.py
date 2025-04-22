'''
gpt_file_name_03.py # 화일이름 한글변환 저장 gpt 팁
나중을 위한 준비 팁: 1. 한글 키워드 ➝ 이니셜로 변환 # 진짜 꿀팁
'''
def to_initial(keyword):
    table = {
        '물놀이': 'ML',
        '서핑': 'SF',
        '수상레저': 'SR',
        '래프팅': 'RF',
        # 필요한 만큼 계속 추가!
    }
    return table.get(keyword, 'ETC')  # 못 찾으면 'ETC'

initial = to_initial(search_keyword)
filename = f"{initial}_{conid}_{img_hash}.jpg"

'''
2. 변환 리스트 저장용 CSV 만들기
'''
import csv
def log_image_data(csv_path, original_keyword, initial, conid, filename):
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([original_keyword, initial, conid, filename])