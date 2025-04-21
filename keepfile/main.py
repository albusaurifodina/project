from utils import make_folder, imageListExtractor, save_image, makeImageTable

# 기본 설정
dataIn = "./images/"
contentId = 1095732
No = 1
Size = 10
service_key = 'azksr7Fgk8fnWawWSRq%2FRzde1JYejaLxXVlKfnCxECuPzkjiwupRnOOvJKZDEsLUwNDmI4J%2BYdJm4QcpiSAGRw%3D%3D'

# 이미지 저장 폴더 확인
make_folder(dataIn)

# 메인 실행
print('이미지 크롤링을 시작합니다...')
image_data = imageListExtractor(contentId, service_key, No, Size)

if image_data:
    items = image_data['response']['body']['items']['item']
    if isinstance(items, dict):
        items = [items]

    for item in items:
        img_url = item.get('originimgurl')
        if img_url:
            save_image(img_url, dataIn)

    # 데이터프레임 생성
    image_df = makeImageTable(image_data)

    # CSV 저장
    filename = 'images/project.get_image_list.csv'
    image_df.to_csv(filename, index=False, encoding='utf-8')
    print(f"{filename} 파일이 저장되었습니다.")
else:
    print(" 데이터를 받아오지 못했습니다.")
