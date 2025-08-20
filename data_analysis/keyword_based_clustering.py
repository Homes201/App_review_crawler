# 키워드 기반 군집 생성 및 라벨링 스크립트
# 리뷰 내용의 키워드를 분석하여 사용자 니즈를 파악할 수 있는 상위 분류로 묶습니다.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# seaborn 스타일 설정 및 한글 폰트 설정
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_and_clean_data():
    """
    데이터를 로드하고 정리하는 함수
    
    전처리 과정:
    1. CSV 파일 로드
    2. None 값 처리 (빈 문자열로 변환)
    3. 빈 리뷰 제거 (길이가 0인 리뷰)
    4. 단어 수가 3개 미만인 리뷰 제거 (의미있는 분석을 위해)
    
    이유: 데이터 품질을 향상시키고 의미있는 분석을 위한 최소 기준 설정
    """
    print("=== 데이터 로드 및 정리 중... ===")
    
    # 데이터 로드
    df = pd.read_csv('data/processed/preprocessed_google_play_reviews.csv')
    print(f"✅ 파일 로드 완료: {len(df):,}행, {len(df.columns)}컬럼")
    
    # None 값 처리
    df['review_cleaned'] = df['review_cleaned'].fillna('')
    
    # 빈 문자열 제거
    df = df[df['review_cleaned'].str.len() > 0].reset_index(drop=True)
    
    # 단어 수가 3개 이상인 리뷰만 선택
    df = df[df['word_count'] >= 3].reset_index(drop=True)
    
    print(f"✅ 정리된 리뷰 수: {len(df):,}개")
    
    return df

def extract_keywords_for_clustering(df):
    """
    군집화를 위한 키워드를 추출하는 함수
    """
    print("\n=== 군집화용 키워드 추출 중... ===")
    
    # 상위 7개 분류 키워드 패턴 정의 (요청 반영)
    keyword_patterns = {
        '기능 및 성능': ['정확', '오류', '에러', '버그', '인식', '검색', '지원', '속도', '느리', '빠르', '안정', '실행', '크래시', '지연', '로딩', '작동', '실패'],
        '사용성 및 편의성': ['ui', 'ux', '편리', '직관', '접근성', '조작', '메뉴', '설정', '사용하기', '복잡', '불편', '가이드', '도움말', '네비', '네비게이션'],
        '학습 및 교육적 가치': ['점자', '공부', '학습', '교육', '교재', '튜토리얼', '연습', '훈련', '자기계발', '학습지원'],
        '서비스 범위 및 한계': ['언어', '범위', '지원', '한정', '제한', '지역', '국가', '기능만', '확장', '서비스', '기기', '호환'],
        '긍정적 경험 / 만족도': ['좋다', '최고', '감사', '추천', '유용', '도움', '만족', '편하', '고맙', '좋아요', '훌륭'],
        '개선 요청 및 제안': ['추가', '개선', '업데이트', '요청', '필요', '제안', '부탁', '원하', '만들', '지원해', '수정'],
        '기타': []
    }
    
    # 각 리뷰에 대해 키워드 매칭 점수 계산
    print("🔄 키워드 매칭 점수 계산 중...")
    
    cluster_scores = {}
    for cluster_name, keywords in keyword_patterns.items():
        cluster_scores[cluster_name] = []
    
    for idx, row in df.iterrows():
        review_text = row['review_cleaned'].lower()
        
        # 각 군집에 대한 점수 계산
        for cluster_name, keywords in keyword_patterns.items():
            score = sum(1 for keyword in keywords if keyword in review_text)
            cluster_scores[cluster_name].append(score)
    
    # 점수를 DataFrame에 추가
    for cluster_name, scores in cluster_scores.items():
        df[f'score_{cluster_name}'] = scores
    
    print(f"✅ 키워드 매칭 점수 계산 완료")
    
    return df, keyword_patterns

def assign_clusters(df):
    """
    키워드 점수를 기반으로 군집을 할당하는 함수
    """
    print("\n=== 군집 할당 중... ===")
    
    # 점수 컬럼들 찾기
    score_columns = [col for col in df.columns if col.startswith('score_')]
    
    # 각 리뷰에 대해 가장 높은 점수의 군집 할당
    df['cluster'] = df[score_columns].idxmax(axis=1).str.replace('score_', '')
    
    # 점수가 모두 0인 경우 '기타'로 분류
    df.loc[df[score_columns].sum(axis=1) == 0, 'cluster'] = '기타'
    
    # 군집별 크기 확인
    cluster_sizes = df['cluster'].value_counts()
    print(f"\n📊 군집별 크기:")
    for cluster_name, size in cluster_sizes.items():
        percentage = (size / len(df)) * 100
        print(f"  {cluster_name}: {size:,}개 ({percentage:.1f}%)")
    
    return df

def analyze_clusters(df):
    """
    군집 분석 결과를 분석하는 함수
    """
    print("\n=== 군집 분석 결과 분석 중... ===")
    
    # 군집별 주요 키워드 추출
    print(f"\n🔍 군집별 주요 키워드:")
    
    for cluster_name in df['cluster'].unique():
        cluster_mask = df['cluster'] == cluster_name
        cluster_texts = df[cluster_mask]['review_cleaned'].str.cat(sep=' ')
        
        if cluster_texts:
            # 단어 빈도 계산
            words = re.findall(r'[가-힣]+', cluster_texts)
            word_freq = pd.Series(words).value_counts().head(10)
            
            print(f"\n  🏷️  {cluster_name} (크기: {len(df[cluster_mask]):,}개):")
            for i, (word, count) in enumerate(word_freq.head(5).items(), 1):
                print(f"    {i}. {word}: {count}회")
    
    return df

def create_visualizations(df):
    """
    군집화 결과를 시각화하는 함수
    
    시각화 기법:
    1. 파이 차트: 군집별 크기 분포 (비율을 직관적으로 표현)
    2. 막대 차트: 군집별 평균 평점 및 단어 수 (수치 비교)
    3. 교차표: 감정별 군집 분포 (범주형 변수 간 관계)
    4. 박스플롯: 리뷰 길이 분포 (분포 형태와 이상치 확인)
    
    seaborn 사용 이유: matplotlib보다 현대적이고 일관된 디자인, 통계적 시각화에 최적화
    """
    print("\n=== 시각화 생성 중... ===")
    
    # seaborn 스타일 설정
    sns.set_palette("husl")
    plt.figure(figsize=(18, 12))
    
    # 1. 군집별 크기 분포 (상위 8개, 가로 막대)
    plt.subplot(2, 3, 1)
    cluster_sizes = df['cluster'].value_counts().head(8).sort_values()
    ax1 = sns.barplot(x=cluster_sizes.values, y=cluster_sizes.index, palette="crest")
    ax1.set_title('군집별 크기 (상위 8)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('리뷰 수')
    ax1.set_ylabel('군집')
    for c in ax1.containers:
        ax1.bar_label(c, fmt='%d', label_type='edge', padding=2)
    
    # 2. 군집별 평균 평점 (막대 차트)
    plt.subplot(2, 3, 2)
    cluster_scores = df.groupby('cluster')['score'].mean().sort_values(ascending=False).head(10)
    ax2 = sns.barplot(x=cluster_scores.values, y=cluster_scores.index, palette="viridis")
    ax2.set_title('군집별 평균 평점 (상위 10)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('평균 평점')
    ax2.set_ylabel('군집')
    for c in ax2.containers:
        ax2.bar_label(c, fmt='%.2f', padding=2)
    
    # 3. 군집별 평균 단어 수 (막대 차트)
    plt.subplot(2, 3, 3)
    cluster_words = df.groupby('cluster')['word_count'].mean().sort_values(ascending=False).head(10)
    ax3 = sns.barplot(x=cluster_words.values, y=cluster_words.index, palette="mako")
    ax3.set_title('군집별 평균 단어 수 (상위 10)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('평균 단어 수')
    ax3.set_ylabel('군집')
    for c in ax3.containers:
        ax3.bar_label(c, fmt='%.1f', padding=2)
    
    # 4. 감정별 군집 분포 (교차표 히트맵)
    plt.subplot(2, 3, 4)
    top_clusters = df['cluster'].value_counts().head(8).index
    sentiment_cluster = pd.crosstab(df['sentiment'], df['cluster'])[top_clusters]
    sentiment_order = ['긍정', '중립', '부정']
    sentiment_cluster = sentiment_cluster.reindex(sentiment_order)
    sentiment_cluster_pct = sentiment_cluster.div(sentiment_cluster.sum(axis=0), axis=1) * 100
    ax4 = sns.heatmap(sentiment_cluster_pct, annot=True, fmt='.1f', cmap='YlOrRd',
                      cbar_kws={'label': '비율 (%)'})
    ax4.set_title('군집별 감정 분포 (상위 8 군집)', fontsize=14, fontweight='bold')
    ax4.set_xlabel('군집')
    ax4.set_ylabel('감정')
    
    # 5. 앱별 군집 분포 (상위 5개) - 히트맵
    plt.subplot(2, 3, 5)
    app_cluster = pd.crosstab(df['app_name'], df['cluster'])
    top_apps = app_cluster.sum(axis=1).nlargest(5).index
    top_clusters2 = app_cluster.sum(axis=0).nlargest(6).index
    app_cluster_pct = app_cluster.loc[top_apps, top_clusters2]
    app_cluster_pct = app_cluster_pct.div(app_cluster_pct.sum(axis=1), axis=0) * 100
    ax5 = sns.heatmap(app_cluster_pct, annot=True, fmt='.1f', cmap='Blues',
                      cbar_kws={'label': '비율 (%)'})
    ax5.set_title('앱별 군집 분포 (상위 앱/군집)', fontsize=14, fontweight='bold')
    ax5.set_xlabel('군집')
    ax5.set_ylabel('앱')
    
    # 6. 군집별 리뷰 길이 분포 (박스플롯)
    plt.subplot(2, 3, 6)
    top_clusters3 = df['cluster'].value_counts().head(8).index
    df_top = df[df['cluster'].isin(top_clusters3)]
    sns.boxplot(data=df_top, x='word_count', y='cluster', palette='Set3', fliersize=2, linewidth=1)
    plt.title('군집별 리뷰 길이 분포 (상위 8)', fontsize=14, fontweight='bold')
    plt.xlabel('단어 수')
    plt.ylabel('군집')
    
    plt.tight_layout()
    plt.savefig('results/keyword_based_clustering_visualizations.png', dpi=300, bbox_inches='tight')
    print("  ✅ 시각화가 저장되었습니다.")
    
    plt.show()

def save_results(df):
    """
    결과를 저장하는 함수
    """
    print("\n=== 결과 저장 중... ===")
    
    # 결과 저장
    output_file = 'data/analysis/keyword_clustered_google_play_reviews.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # 군집별 요약 통계
    cluster_summary = df.groupby('cluster').agg({
        'score': ['count', 'mean', 'std'],
        'word_count': ['mean', 'std'],
        'sentiment': lambda x: x.value_counts().index[0] if len(x) > 0 else 'N/A'
    }).round(2)
    
    cluster_summary.columns = ['리뷰수', '평균평점', '평점표준편차', '평균단어수', '단어수표준편차', '주요감정']
    cluster_summary = cluster_summary.sort_values('리뷰수', ascending=False)
    
    print(f"\n📊 군집별 요약 통계:")
    print(cluster_summary)
    
    # 요약 통계 저장
    summary_file = 'data/analysis/keyword_cluster_summary_statistics.csv'
    cluster_summary.to_csv(summary_file, encoding='utf-8-sig')
    
    # 군집별 상세 분석
    detailed_analysis = {}
    for cluster_name in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster_name]
        
        # 주요 키워드
        cluster_texts = cluster_data['review_cleaned'].str.cat(sep=' ')
        words = re.findall(r'[가-힣]+', cluster_texts)
        top_keywords = pd.Series(words).value_counts().head(10)
        
        # 앱별 분포
        app_distribution = cluster_data['app_name'].value_counts().head(5)
        
        detailed_analysis[cluster_name] = {
            '크기': len(cluster_data),
            '평균평점': cluster_data['score'].mean(),
            '평균단어수': cluster_data['word_count'].mean(),
            '주요키워드': top_keywords.to_dict(),
            '주요앱': app_distribution.to_dict()
        }
    
    # 상세 분석 저장
    detailed_file = 'data/analysis/keyword_cluster_detailed_analysis.csv'
    detailed_df = pd.DataFrame(detailed_analysis).T
    detailed_df.to_csv(detailed_file, encoding='utf-8-sig')
    
    print(f"\n💾 결과 파일들이 저장되었습니다:")
    print(f"  - {output_file}: 키워드 기반 군집 분석된 전체 데이터")
    print(f"  - {summary_file}: 군집별 요약 통계")
    print(f"  - {detailed_file}: 군집별 상세 분석")
    
    return df, cluster_summary, detailed_analysis

def main():
    """
    메인 실행 함수
    """
    try:
        print("=== 키워드 기반 리뷰 데이터 군집 분석 시작 ===")
        
        # 1. 데이터 로드 및 정리
        df = load_and_clean_data()
        
        # 2. 키워드 추출 및 점수 계산
        df, keyword_patterns = extract_keywords_for_clustering(df)
        
        # 3. 군집 할당
        df = assign_clusters(df)
        
        # 4. 군집 분석
        df = analyze_clusters(df)
        
        # 5. 시각화 생성
        create_visualizations(df)
        
        # 6. 결과 저장
        final_df, summary, detailed = save_results(df)
        
        print(f"\n키워드 기반 군집 분석이 완료되었습니다!")
        print(f"📊 총 군집 수: {len(df['cluster'].unique())}개")
        print(f"📈 분석된 리뷰 수: {len(final_df):,}개")
        
        # 주요 인사이트 출력
        print(f"\n주요 인사이트:")
        top_clusters = summary.head(5)
        for i, (cluster_name, stats) in enumerate(top_clusters.iterrows(), 1):
            print(f"  {i}. {cluster_name}: {stats['리뷰수']:,}개 리뷰, 평균 평점 {stats['평균평점']:.1f}")
        
        # 군집별 특징 요약
        print(f"\n🔍 군집별 주요 특징:")
        for cluster_name in ['기능성', '성능', '사용성', '안정성']:
            if cluster_name in detailed:
                info = detailed[cluster_name]
                print(f"  📱 {cluster_name}: {info['크기']:,}개 리뷰, 평균 평점 {info['평균평점']:.1f}")
                top_keywords = list(info['주요키워드'].keys())[:3]
                print(f"     주요 키워드: {', '.join(top_keywords)}")
        
    except FileNotFoundError:
        print("❌ data/processed/preprocessed_google_play_reviews.csv 파일을 찾을 수 없습니다.")
        print("먼저 text_preprocessing.py를 실행하여 데이터를 전처리해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
