import pandas as pd
from app_store_scraper import AppStore


# 앱스토어 크롤링 정의
def App_store_crawler(app_name : str = None, app_id : int = None, user_defined_app_name: str = None, output_file="app_reviews.csv"):


    # 앱 이름 or id 입력 시 조건
    if not app_name and not app_id :
        print("앱 이름이나 ID 중 하나는 반드시 입력해야 합니다.")
        return
    
    # 출력할 앱 이름 설정 (사용자가 지정한 이름이 있으면 우선 사용)
    display_name = user_defined_app_name if user_defined_app_name else app_name if app_name else str(app_id)
    print(f"{display_name}의 리뷰를 가져오는 중...")

    # 앱스토어 크롤링
    app = AppStore(country='kr', app_name = app_name, app_id = app_id)
    app.review()

    # 데이터 정리
    app_reviews = pd.DataFrame(app.reviews).sort_values('date', ascending=False).reset_index(drop=True)

    if user_defined_app_name:
        app_reviews['app_name'] = user_defined_app_name


    #csv 형식으로 저장
    app_reviews.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"리뷰 데이터가 '{output_file}'파일로 저장되었습니다.총{len(app_reviews)}건")
    
    return app_reviews


if __name__ == "__main__":
    
    #사용자 입력 받기
    app_name = input("앱 이름을 입력해주세요.(없으면 enter)").strip() or None # 해당 입력은 옵션
    app_id_input = input("앱 id를 입력해주세요.(없으면 enter)").strip() # 해당 입력은 옵션
    user_defined_app_name = input("저장할 앱 이름을 입력해주세요(없으면 enter)").strip() # 해당 입력도 옵션

    # 입력값 처리
    app_id = int(app_id_input) if app_id_input.isdigit() else None

    # 파일명 정의
    display_name = user_defined_app_name if user_defined_app_name else app_name if app_name else str(app_id)
    output_file_name = f"AppStore_{display_name}_reviews.csv"

    # 앱 이름 또는 앱 ID가 입력되었는지 확인 후 크롤링 실행
    if app_name or app_id :
        App_store_crawler(app_name, app_id, user_defined_app_name, output_file_name)

    else :
        print("앱 이름이나 id를 입력해야 합니다.")


# 자세한 내용은 여기 참조 https://pypi.org/project/app-store-scraper/
