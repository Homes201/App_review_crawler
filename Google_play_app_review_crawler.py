
from google_play_scraper import Sort, reviews_all
import pandas as pd
import tqdm

# 입력할 앱 리스트 선정 - 직접 입력창에 넣어 사용 앱 이름 구글 플레이 > 앱 이름 검색 > 상단 url 주소 id값 확인 ex) https://play.google.com/store/apps/details?id=com.friendscube.somoim


# 구글 스토어 크롤링 
def scrape_reviews(app_name, output_file="app_reviews.csv"):

    print(f"{app_name}의 리뷰를 가져오는 중....")

    # 크롤링 대상 앱 정보
    app_operation = reviews_all(
        app_name,  # 앱 이름,
        sleep_milliseconds=0, # defaults to 20,
        lang='ko',          # 언어 설정,
        country='kr',       # 국가 설정,
        sort=Sort.NEWEST,   # 정렬 기준,
    )

    reviews_list = []

    # 리뷰 데이터 수집,
    for review in tqdm.tqdm(app_operation):
        review_dic = {
            "app_name" : app_name,
            "review_id" : review['reviewId'],
            "review" : review['content'],
            "score" : review['score'],
            "thumb_up_count" : review['thumbsUpCount'],
            "datetime" : review['at'],
            "app_version" : review['appVersion'] # 해당 내용으로 앱 버전에 따른 사용자들의 평판 변화 확인 가능
        }
        reviews_list.append(review_dic)
        

    # pandas 프레임워크로 변환
    reviews_df = pd.DataFrame(reviews_list)

    #csv 형식으로 저장
    reviews_df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"리뷰 데이터가 '{output_file}'파일로 저장되었습니다.")


if __name__ == "__main__" :
        
    app_name= input("Google play 스토어 앱 패키지 명을 입력하세요: ex) com.dodreamlibapp  : ").strip()
    
    #사용자 입력 받기
    if app_name :
        scrape_reviews(app_name, output_file=f"Google_play_{app_name}_reviews.csv")

    else :
        print("앱 패키지명을 입력해야 합니다.")
            

# 자세한 사항은 해당 웹사이트 참고 : https://pypi.org/project/google-play-scraper/