# 워드클라우드 시각화 스크립트
# 키워드 기반 군집 분석 결과를 바탕으로 각 군집별 워드클라우드를 생성합니다.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import konlpy
from konlpy.tag import Okt
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# seaborn 스타일 설정 및 한글 폰트 설정
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_clustered_data():
    """
    키워드 기반 군집 분석 결과를 로드하는 함수
    """
    print("=== 키워드 기반 군집 분석 데이터 로드 중... ===")
    
    try:
        df = pd.read_csv('data/analysis/keyword_clustered_google_play_reviews.csv')
        print(f"✅ 데이터 로드 완료: {len(df):,}행, {len(df.columns)}컬럼")
        return df
    except FileNotFoundError:
        print("❌ keyword_clustered_google_play_reviews.csv 파일을 찾을 수 없습니다.")
        print("먼저 keyword_based_clustering.py를 실행하여 데이터를 분석해주세요.")
        return None

okt = Okt()

def extract_pos_words(text_series, include_pos=('Noun','Verb')):
    joined = ' '.join(text_series.fillna(''))
    tokens = []
    for sent in joined.split('\n'):
        try:
            tokens.extend(okt.pos(sent, stem=True))
        except Exception:
            continue
    words = [w for w, p in tokens if p in include_pos and len(w) > 1]
    return words

def create_wordcloud_for_cluster(cluster_data, cluster_name, max_words=100, include_pos=('Noun','Verb')):
    """
    특정 군집에 대한 워드클라우드를 생성하는 함수
    """
    words = extract_pos_words(cluster_data['review_cleaned'], include_pos=include_pos)
    if not words:
        return None

    word_freq = Counter(words)
    # 기능 관련 키워드 가중치 부여(강조)
    feature_terms = {
        '기능','통화','전화','녹음','업데이트','호출','연동','설정','메뉴','음성','읽기','블루투스','연결','백업','복원','호환'
    }
    for w in list(word_freq.keys()):
        if w in feature_terms:
            word_freq[w] = int(word_freq[w] * 1.5) + 1
    
    # 너무 짧은 단어 제거 (1-2글자)
    word_freq = {word: count for word, count in word_freq.items() if len(word) > 2}
    
    # 상위 단어만 선택
    top_words = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:max_words])
    
    if not top_words:
        return None
    
    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/malgun.ttf',  # Windows 한글 폰트 경로
        width=800,
        height=600,
        background_color='white',
        colormap='viridis',
        max_words=max_words,
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(top_words)
    
    return wordcloud, top_words

def create_all_wordclouds(df):
    """
    앱별(각 앱 하나의 이미지) 명사 전용 워드클라우드 생성
    """
    print("\n=== 앱별 워드클라우드 생성 중... ===")

    apps = df['app_name'].unique()
    for app in apps:
        app_df = df[df['app_name'] == app]
        print(f"🔄 {app} 앱 워드클라우드 생성 중... ({len(app_df):,}개 리뷰)")

        result = create_wordcloud_for_cluster(app_df, app, max_words=150, include_pos=('Noun',))
        if result is None:
            print(f"  ⚠️  {app}: 워드클라우드를 생성할 수 없습니다.")
            continue

        wordcloud, top_words = result

        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'{app} 앱 워드클라우드\n({len(app_df):,}개 리뷰)', fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')

        top_list = list(top_words.items())[:12]
        word_text = '\n'.join([f'{word}: {count}' for word, count in top_list])
        plt.text(0.02, 0.98, word_text, transform=plt.gca().transAxes,
                 fontsize=12, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

        safe_app = re.sub(r'[^가-힣a-zA-Z0-9_\-]+', '_', app)
        filename = f'results/wordcloud_app_{safe_app}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✅ {filename} 저장 완료")
        plt.close()

    return None

def create_individual_wordclouds(df):
    """
    각 군집별로 개별 워드클라우드를 생성하는 함수
    """
    print("\n=== 개별 워드클라우드 생성 중... ===")
    
    clusters = df['cluster'].unique()
    
    for cluster_name in clusters:
        cluster_data = df[df['cluster'] == cluster_name]
        
        print(f"🔄 {cluster_name} 개별 워드클라우드 생성 중...")
        
        result = create_wordcloud_for_cluster(cluster_data, cluster_name, max_words=150, include_pos=('Noun','Verb'))
        
        if result is not None:
            wordcloud, top_words = result
            
            # 개별 워드클라우드 생성
            plt.figure(figsize=(12, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title(f'{cluster_name} 군집 워드클라우드\n({len(cluster_data):,}개 리뷰)', 
                     fontsize=16, fontweight='bold', pad=20)
            plt.axis('off')
            
            # 상위 15개 단어 표시
            top_10_words = list(top_words.items())[:15]
            word_text = '\n'.join([f'{word}: {count}' for word, count in top_10_words])
            plt.text(0.02, 0.98, word_text, transform=plt.gca().transAxes, 
                    fontsize=12, verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
            
            # 파일 저장
            filename = f'results/wordcloud_{cluster_name}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"  ✅ {filename} 저장 완료")
            
            plt.show()
        else:
            print(f"  ⚠️  {cluster_name} 군집에 대한 워드클라우드를 생성할 수 없습니다.")

def analyze_keyword_patterns(df):
    """
    군집별 키워드 패턴을 분석하는 함수
    """
    print("\n=== 군집별 키워드 패턴 분석 중... ===")
    
    keyword_analysis = {}
    
    for cluster_name in df['cluster'].unique():
        cluster_data = df[df['cluster'] == cluster_name]
        
        # 리뷰 텍스트 결합
        all_text = ' '.join(cluster_data['review_cleaned'].fillna(''))
        
        # 한국어 단어 추출
        korean_words = re.findall(r'[가-힣]+', all_text)
        
        # 단어 빈도 계산
        word_freq = Counter(korean_words)
        
        # 너무 짧은 단어 제거
        word_freq = {word: count for word, count in word_freq.items() if len(word) > 2}
        
        # 상위 20개 단어
        top_words = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20])
        
        keyword_analysis[cluster_name] = {
            'total_words': len(korean_words),
            'unique_words': len(word_freq),
            'top_keywords': top_words,
            'review_count': len(cluster_data),
            'avg_score': cluster_data['score'].mean(),
            'avg_word_count': cluster_data['word_count'].mean()
        }
    
    # 분석 결과 출력
    print(f"\n📊 군집별 키워드 분석 결과:")
    for cluster_name, analysis in keyword_analysis.items():
        print(f"\n🏷️  {cluster_name}:")
        print(f"  - 리뷰 수: {analysis['review_count']:,}개")
        print(f"  - 총 단어 수: {analysis['total_words']:,}개")
        print(f"  - 고유 단어 수: {analysis['unique_words']:,}개")
        print(f"  - 평균 평점: {analysis['avg_score']:.2f}")
        print(f"  - 평균 단어 수: {analysis['avg_word_count']:.1f}")
        print(f"  - 상위 키워드: {', '.join(list(analysis['top_keywords'].keys())[:5])}")
    
    return keyword_analysis

def save_keyword_analysis(keyword_analysis):
    """
    키워드 분석 결과를 저장하는 함수
    """
    print("\n=== 키워드 분석 결과 저장 중... ===")
    
    # 상세 분석 결과를 DataFrame으로 변환
    analysis_data = []
    
    for cluster_name, analysis in keyword_analysis.items():
        # 상위 키워드를 문자열로 변환
        top_keywords_str = ', '.join([f"{word}({count})" for word, count in 
                                    list(analysis['top_keywords'].items())[:10]])
        
        analysis_data.append({
            '군집명': cluster_name,
            '리뷰수': analysis['review_count'],
            '총단어수': analysis['total_words'],
            '고유단어수': analysis['unique_words'],
            '평균평점': round(analysis['avg_score'], 2),
            '평균단어수': round(analysis['avg_word_count'], 1),
            '상위키워드': top_keywords_str
        })
    
    # DataFrame 생성 및 저장
    analysis_df = pd.DataFrame(analysis_data)
    analysis_df = analysis_df.sort_values('리뷰수', ascending=False)
    
    output_file = 'data/analysis/wordcloud_keyword_analysis.csv'
    analysis_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ 키워드 분석 결과가 {output_file}에 저장되었습니다.")
    
    return analysis_df

def main():
    """
    메인 실행 함수
    """
    try:
        print("=== 워드클라우드 시각화 시작 ===")
        
        # 1. 데이터 로드
        df = load_clustered_data()
        if df is None:
            return
        
        # 2. 키워드 패턴 분석
        keyword_analysis = analyze_keyword_patterns(df)
        
        # 3. 앱별 워드클라우드 생성 (명사 전용)
        print("\n=== 앱별 워드클라우드 생성 ===")
        create_all_wordclouds(df)
        
        # 5. 분석 결과 저장
        analysis_df = save_keyword_analysis(keyword_analysis)
        
        print(f"\n워드클라우드 시각화가 완료되었습니다!")
        print(f"📊 총 {len(df['cluster'].unique())}개 군집에 대한 워드클라우드가 생성되었습니다.")
        print(f"📈 분석된 리뷰 수: {len(df):,}개")
        
        # 주요 인사이트 출력
        print(f"\n주요 인사이트:")
        top_clusters = analysis_df.head(3)
        for i, (_, row) in enumerate(top_clusters.iterrows(), 1):
            print(f"  {i}. {row['군집명']}: {row['리뷰수']:,}개 리뷰, {row['고유단어수']:,}개 고유 단어")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
