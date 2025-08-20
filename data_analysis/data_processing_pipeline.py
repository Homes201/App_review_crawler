# 통합 데이터 처리 파이프라인 스크립트
# Google Play 리뷰 데이터를 통합, 전처리, 군집 분석하는 전체 과정을 자동화합니다.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def merge_google_play_reviews():
    """
    모든 Google Play 리뷰 CSV 파일을 통합하는 함수
    """
    print("=== Google Play 리뷰 파일 통합 중... ===")
    
    import glob
    import os
    
    csv_files = glob.glob("data/raw/Google_play_*.csv")
    print(f"📁 발견된 CSV 파일: {len(csv_files)}개")
    
    all_reviews = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            app_name_from_file = os.path.basename(file).replace("Google_play_", "").replace("_reviews.csv", "")
            
            if 'app_name' in df.columns:
                df['app_name'] = df['app_name'].fillna(app_name_from_file)
            else:
                df['app_name'] = app_name_from_file
            
            df['source_file'] = file
            all_reviews.append(df)
            print(f"  ✅ {file}: {len(df):,}개 리뷰")
            
        except Exception as e:
            print(f"  ❌ {file} 처리 실패: {e}")
    
    if all_reviews:
        combined_df = pd.concat(all_reviews, ignore_index=True)
        combined_df.to_csv("data/raw/combined_google_play_reviews.csv", index=False, encoding='utf-8-sig')
        print(f"\n✅ 통합 완료: {len(combined_df):,}개 리뷰")
        return combined_df
    else:
        print("❌ 통합할 데이터가 없습니다.")
        return None

def update_app_names(df):
    """
    앱 ID를 실제 앱 이름으로 대체하는 함수
    """
    print("\n=== 앱 이름 업데이트 중... ===")
    
    app_name_mapping = {
        'com.skt.nugu.apollo': '에이닷 (AI 개인비서)',
        'com.skt.prod.dialer': '에이닷 전화 (에이닷 전화)',
        'tuat.kr.sullivan': '설리번 플러스',
        'tuat.kr.sullivanlite': '설리번 라이트',
        'kr.tuat.sullivanfinder': '설리번 파인더',
        'com.sigonggan.pickforme': '픽포미 (Pick for Me)',
        'kr.go.seoul.mobile.seoulvoiceinfo': '소비재 정보 마당',
        'com.sigongan.sorialbum': '소리앨범 (Sori Album)',
        'com.medialife.news': '미디어생활 (Media Life)',
        'kr.or.bis': '모바일소리책 (소리책)',
        'appinventor.ai_epainos.point_upload': '시각장애인 점자번역 (점자 앱)',
        'com.bridge.noongil': '눈길 (점자 사진 번역기)',
        'kr.lbstech.spacedetect.geye': 'G-EYE+ (지아이 플러스 내비)',
        'com.google.android.apps.accessibility.reveal': '구글 룩아웃',
        'com.bemyeyes.bemyeyes': 'Be My Eyes'
    }
    
    df['app_id'] = df['app_name']
    
    for app_id, app_name in app_name_mapping.items():
        mask = df['app_id'] == app_id
        if mask.any():
            df.loc[mask, 'app_name'] = app_name
            print(f"  ✅ {app_id} → {app_name}")
    
    df.to_csv('data/raw/combined_google_play_reviews_with_names.csv', index=False, encoding='utf-8-sig')
    print(f"✅ 앱 이름 업데이트 완료")
    
    return df

def preprocess_reviews(df):
    """
    리뷰 텍스트를 전처리하는 함수
    """
    print("\n=== 리뷰 텍스트 전처리 중... ===")
    
    def clean_text(text):
        if pd.isna(text) or text == '':
            return ''
        text = str(text)
        text = re.sub(r'[^\w\s가-힣]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_korean_words(text):
        if not text:
            return []
        korean_pattern = r'[가-힣]+|[a-zA-Z]+|\d+'
        words = re.findall(korean_pattern, text)
        return [word for word in words if len(word) > 1]
    
    def remove_stopwords(words):
        # 한국어 불용어 리스트
        stopwords = {
            '이', '그', '저', '것', '수', '등', '때', '곳', '말', '일', '년', '월', '일', '시', '분',
            '가', '는', '을', '를', '이', '가', '도', '만', '에', '에서', '로', '으로', '와', '과',
            '의', '에', '게', '께', '한', '한', '는', '은', '도', '만', '도', '라', '며', '고',
            '아', '어', '요', '다', '니다', '습니다', '어요', '아요', '네요', '습니다', '니다',
            '있다', '없다', '하다', '되다', '있다', '없다', '좋다', '나쁘다', '크다', '작다',
            '많다', '적다', '빠르다', '느리다', '쉽다', '어렵다', '편하다', '불편하다'
        }
        return [word for word in words if word not in stopwords]
    
    df_processed = df.copy()
    
    # 텍스트 정리
    df_processed['review_cleaned'] = df_processed['review'].apply(clean_text)
    df_processed = df_processed[df_processed['review_cleaned'] != ''].reset_index(drop=True)
    
    # 단어 추출
    df_processed['words'] = df_processed['review_cleaned'].apply(extract_korean_words)
    df_processed['words_filtered'] = df_processed['words'].apply(remove_stopwords)
    
    # 통계 정보
    df_processed['word_count'] = df_processed['words'].apply(len)
    df_processed['word_count_filtered'] = df_processed['words_filtered'].apply(len)
    
    # 리뷰 길이 분류
    df_processed['review_length_category'] = df_processed['word_count'].apply(
        lambda x: '매우 짧음' if x <= 5 else '짧음' if x <= 10 else '보통' if x <= 20 else '길음' if x <= 50 else '매우 길음'
    )
    
    # 감정 분류 (평점 기반)
    df_processed['sentiment'] = df_processed['score'].apply(
        lambda x: '긍정' if x >= 4 else '중립' if x == 3 else '부정'
    )
    
    print(f"✅ 전처리 완료: {len(df_processed):,}개 리뷰")
    
    # 결과 저장
    df_processed.to_csv('data/processed/preprocessed_google_play_reviews.csv', index=False, encoding='utf-8-sig')
    
    return df_processed

def create_preprocessing_visualizations(df):
    """
    전처리 결과를 시각화하는 함수
    """
    print("\n=== 전처리 결과 시각화 생성 중... ===")
    
    plt.figure(figsize=(18, 12))
    
    # 1. 리뷰 길이 분포
    plt.subplot(2, 3, 1)
    length_counts = df['review_length_category'].value_counts()
    plt.pie(length_counts.values, labels=length_counts.index, autopct='%1.1f%%')
    plt.title('리뷰 길이 분포')
    
    # 2. 감정 분포
    plt.subplot(2, 3, 2)
    sentiment_counts = df['sentiment'].value_counts()
    plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
    plt.title('감정 분포')
    
    # 3. 앱별 평균 단어 수
    plt.subplot(2, 3, 3)
    app_word_counts = df.groupby('app_name')['word_count'].mean().sort_values(ascending=False)
    plt.bar(range(len(app_word_counts)), app_word_counts.values)
    plt.xticks(range(len(app_word_counts)), app_word_counts.index, rotation=45, ha='right')
    plt.title('앱별 평균 단어 수')
    plt.ylabel('평균 단어 수')
    
    # 4. 평점별 평균 단어 수
    plt.subplot(2, 3, 4)
    score_word_counts = df.groupby('score')['word_count'].mean()
    plt.bar(score_word_counts.index, score_word_counts.values)
    plt.title('평점별 평균 단어 수')
    plt.xlabel('평점')
    plt.ylabel('평균 단어 수')
    
    # 5. 단어 수 분포 히스토그램
    plt.subplot(2, 3, 5)
    plt.hist(df['word_count'], bins=50, alpha=0.7, edgecolor='black')
    plt.title('단어 수 분포')
    plt.xlabel('단어 수')
    plt.ylabel('빈도')
    
    # 6. 평점 분포
    plt.subplot(2, 3, 6)
    score_counts = df['score'].value_counts().sort_index()
    plt.bar(score_counts.index, score_counts.values)
    plt.title('평점 분포')
    plt.xlabel('평점')
    plt.ylabel('리뷰 수')
    
    plt.tight_layout()
    plt.savefig('results/preprocessing_visualizations.png', dpi=300, bbox_inches='tight')
    print("  ✅ 전처리 시각화가 저장되었습니다.")
    
    plt.show()

def perform_keyword_based_clustering(df):
    """
    키워드 기반 군집 분석을 수행하는 함수
    """
    print("\n=== 키워드 기반 군집 분석 중... ===")
    
    # 상위 7개 분류 키워드 패턴
    keyword_patterns = {
        '기능 및 성능': [
            '정확', '오류', '에러', '버그', '인식', '검색', '지원', '속도', '느리', '빠르', '안정', '실행', '크래시', '지연', '로딩', '작동', '실패'
        ],
        '사용성 및 편의성': [
            'ui', 'ux', '편리', '직관', '접근성', '조작', '메뉴', '설정', '사용하기', '복잡', '불편', '가이드', '도움말', '네비', '네비게이션'
        ],
        '학습 및 교육적 가치': [
            '점자', '공부', '학습', '교육', '교재', '튜토리얼', '연습', '훈련', '자기계발', '학습지원'
        ],
        '서비스 범위 및 한계': [
            '언어', '범위', '지원', '한정', '제한', '지역', '국가', '기능만', '확장', '서비스', '기기', '호환'
        ],
        '긍정적 경험 / 만족도': [
            '좋다', '최고', '감사', '추천', '유용', '도움', '만족', '편하', '고맙', '좋아요', '훌륭'
        ],
        '개선 요청 및 제안': [
            '추가', '개선', '업데이트', '요청', '필요', '제안', '부탁', '원하', '만들', '지원해', '수정'
        ],
        '기타': []
    }
    
    # 키워드 점수 계산
    print("🔄 키워드 매칭 점수 계산 중...")
    
    for cluster_name, keywords in keyword_patterns.items():
        scores = []
        for text in df['review_cleaned']:
            score = sum(1 for keyword in keywords if keyword in text.lower())
            scores.append(score)
        df[f'score_{cluster_name}'] = scores
    
    # 군집 할당
    score_columns = [col for col in df.columns if col.startswith('score_')]
    df['cluster'] = df[score_columns].idxmax(axis=1).str.replace('score_', '')
    df.loc[df[score_columns].sum(axis=1) == 0, 'cluster'] = '기타'
    
    # 군집별 통계
    cluster_sizes = df['cluster'].value_counts()
    print(f"\n📊 군집별 크기:")
    for cluster_name, size in cluster_sizes.items():
        percentage = (size / len(df)) * 100
        print(f"  {cluster_name}: {size:,}개 ({percentage:.1f}%)")
    
    # 결과 저장
    df.to_csv('data/analysis/keyword_clustered_google_play_reviews.csv', index=False, encoding='utf-8-sig')
    
    return df

def create_clustering_visualizations(df):
    """
    군집 분석 결과를 시각화하는 함수
    """
    print("\n=== 군집 분석 결과 시각화 생성 중... ===")
    
    plt.figure(figsize=(18, 12))
    
    # 1. 군집별 크기 분포
    plt.subplot(2, 3, 1)
    cluster_sizes = df['cluster'].value_counts()
    plt.pie(cluster_sizes.values, labels=cluster_sizes.index, autopct='%1.1f%%')
    plt.title('군집별 크기 분포')
    
    # 2. 군집별 평균 평점
    plt.subplot(2, 3, 2)
    cluster_scores = df.groupby('cluster')['score'].mean().sort_values(ascending=False)
    plt.bar(range(len(cluster_scores)), cluster_scores.values)
    plt.xticks(range(len(cluster_scores)), cluster_scores.index, rotation=45, ha='right')
    plt.title('군집별 평균 평점')
    plt.ylabel('평균 평점')
    
    # 3. 군집별 평균 단어 수
    plt.subplot(2, 3, 3)
    cluster_words = df.groupby('cluster')['word_count'].mean().sort_values(ascending=False)
    plt.bar(range(len(cluster_words)), cluster_words.values)
    plt.xticks(range(len(cluster_words)), cluster_words.index, rotation=45, ha='right')
    plt.title('군집별 평균 단어 수')
    plt.ylabel('평균 단어 수')
    
    # 4. 감정별 군집 분포
    plt.subplot(2, 3, 4)
    sentiment_cluster = pd.crosstab(df['sentiment'], df['cluster'])
    sentiment_cluster_pct = sentiment_cluster.div(sentiment_cluster.sum(axis=0), axis=1) * 100
    sentiment_cluster_pct.plot(kind='bar', ax=plt.gca())
    plt.title('군집별 감정 분포')
    plt.xlabel('감정')
    plt.ylabel('비율 (%)')
    plt.legend(title='군집', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 5. 앱별 군집 분포 (상위 5개)
    plt.subplot(2, 3, 5)
    app_cluster = pd.crosstab(df['app_name'], df['cluster'])
    top_apps = app_cluster.sum(axis=1).nlargest(5).index
    app_cluster_pct = app_cluster.loc[top_apps].div(app_cluster.loc[top_apps].sum(axis=0), axis=1) * 100
    app_cluster_pct.plot(kind='bar', ax=plt.gca())
    plt.title('군집별 앱 분포 (상위 5개)')
    plt.xlabel('앱')
    plt.ylabel('비율 (%)')
    plt.legend(title='군집', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    
    # 6. 군집별 리뷰 길이 분포
    plt.subplot(2, 3, 6)
    length_data = []
    length_labels = []
    for cluster_name in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster_name]['word_count']
        length_data.append(cluster_data.values)
        length_labels.append(cluster_name)
    
    plt.boxplot(length_data, labels=length_labels)
    plt.title('군집별 리뷰 길이 분포')
    plt.ylabel('단어 수')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('results/clustering_visualizations.png', dpi=300, bbox_inches='tight')
    print("  ✅ 군집 분석 시각화가 저장되었습니다.")
    
    plt.show()

def save_summary_statistics(df):
    """
    요약 통계를 저장하는 함수
    """
    print("\n=== 요약 통계 저장 중... ===")
    
    # 군집별 요약 통계
    cluster_summary = df.groupby('cluster').agg({
        'score': ['count', 'mean', 'std'],
        'word_count': ['mean', 'std'],
        'sentiment': lambda x: x.value_counts().index[0] if len(x) > 0 else 'N/A'
    }).round(2)
    
    cluster_summary.columns = ['리뷰수', '평균평점', '평점표준편차', '평균단어수', '단어수표준편차', '주요감정']
    cluster_summary = cluster_summary.sort_values('리뷰수', ascending=False)
    
    # 요약 통계 저장
    summary_file = 'data/analysis/cluster_summary_statistics.csv'
    cluster_summary.to_csv(summary_file, encoding='utf-8-sig')
    
    print(f"✅ 요약 통계가 {summary_file}에 저장되었습니다.")
    
    return cluster_summary

def generate_app_level_summary(df):
    """
    앱별 리뷰 수, 감성 비율, 상위 키워드 요약 생성 및 저장
    저장: data/analysis/app_level_summary.csv
    """
    print("\n=== 앱별 요약 통계 생성 중... ===")

    # 앱명은 사람이 읽기 쉬운 app_name 컬럼 사용, 원본 ID는 app_id로 유지된 상태
    app_groups = df.groupby('app_name', dropna=False)

    summary_rows = []
    for app, g in app_groups:
        total = len(g)
        pos = (g['sentiment'] == '긍정').sum()
        neu = (g['sentiment'] == '중립').sum()
        neg = (g['sentiment'] == '부정').sum()

        # 상위 키워드 (전처리된 words_filtered 컬럼 기준)
        try:
            all_words = [w for words in g.get('words_filtered', []) for w in (words if isinstance(words, list) else [])]
        except Exception:
            all_words = []
        top_keywords = pd.Series(all_words).value_counts().head(10)
        top_keywords_str = ', '.join([f"{k}({v})" for k, v in top_keywords.items()]) if not top_keywords.empty else ''

        summary_rows.append({
            '앱명': app,
            '총리뷰수': int(total),
            '긍정수': int(pos),
            '중립수': int(neu),
            '부정수': int(neg),
            '긍정비율(%)': round(pos / total * 100, 1) if total else 0.0,
            '부정비율(%)': round(neg / total * 100, 1) if total else 0.0,
            '상위키워드(Top10)': top_keywords_str
        })

    summary_df = pd.DataFrame(summary_rows).sort_values('총리뷰수', ascending=False)
    output_path = 'data/analysis/app_level_summary.csv'
    summary_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 앱별 요약 통계 저장: {output_path}")

    return summary_df

def main():
    """
    메인 실행 함수
    """
    try:
        print("=== 통합 데이터 처리 파이프라인 시작 ===")
        
        # 1. Google Play 리뷰 파일 통합
        df = merge_google_play_reviews()
        if df is None:
            return
        
        # 2. 앱 이름 업데이트
        df = update_app_names(df)
        
        # 3. 리뷰 텍스트 전처리
        df_processed = preprocess_reviews(df)
        
        # 4. 전처리 결과 시각화
        create_preprocessing_visualizations(df_processed)
        
        # 5. 키워드 기반 군집 분석
        df_clustered = perform_keyword_based_clustering(df_processed)
        
        # 6. 군집 분석 결과 시각화
        create_clustering_visualizations(df_clustered)
        
        # 7. 요약 통계 저장
        summary = save_summary_statistics(df_clustered)

        # 8. 앱별 요약 통계 저장
        app_summary = generate_app_level_summary(df_processed)
        
        print(f"\n통합 데이터 처리 파이프라인이 완료되었습니다!")
        print(f"📊 총 리뷰 수: {len(df_clustered):,}개")
        print(f"🏷️  총 군집 수: {len(df_clustered['cluster'].unique())}개")
        
        # 주요 인사이트 출력
        print(f"\n주요 인사이트:")
        top_clusters = summary.head(3)
        for i, (cluster_name, stats) in enumerate(top_clusters.iterrows(), 1):
            print(f"  {i}. {cluster_name}: {stats['리뷰수']:,}개 리뷰, 평균 평점 {stats['평균평점']:.1f}")
        
        print(f"\n생성된 파일들:")
        print(f"  - data/raw/combined_google_play_reviews.csv: 통합된 원본 데이터")
        print(f"  - data/raw/combined_google_play_reviews_with_names.csv: 앱 이름이 업데이트된 데이터")
        print(f"  - data/processed/preprocessed_google_play_reviews.csv: 전처리된 데이터")
        print(f"  - data/analysis/keyword_clustered_google_play_reviews.csv: 군집 분석된 데이터")
        print(f"  - data/analysis/cluster_summary_statistics.csv: 군집별 요약 통계")
        print(f"  - data/analysis/app_level_summary.csv: 앱별 요약 통계")
        print(f"  - results/preprocessing_visualizations.png: 전처리 결과 시각화")
        print(f"  - results/clustering_visualizations.png: 군집 분석 결과 시각화")
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
