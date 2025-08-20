# 📱 시각장애인 앱 서비스 페인포인트 분석 프로젝트

Google Play Store의 시각장애인 지원 앱 리뷰를 크롤링하고 분석하여 사용자 페인포인트를 발굴하는 프로젝트입니다.

## 🚀 주요 기능

- **Google Play Store 리뷰 크롤링**: 16개 시각장애인 지원 앱의 리뷰 데이터 수집
- **데이터 전처리**: 한국어 텍스트 정제 및 분석 준비
- **키워드 기반 군집화**: 유사한 피드백을 가진 리뷰 그룹화
- **워드클라우드 시각화**: 군집별 키워드 분포 시각화
- **페인포인트 분석**: 시각장애인 앱 서비스의 개선점 및 새로운 기획 방향성 제시

## 📁 프로젝트 구조

```
App_review_crawler/
├── 📊 data_analysis/                    # 데이터 분석 스크립트
│   ├── __init__.py
│   ├── keyword_based_clustering.py      # 키워드 기반 군집화
│   └── data_processing_pipeline.py      # 데이터 처리 파이프라인
├── 🎨 data_visualization/               # 시각화 스크립트
│   ├── __init__.py
│   └── wordcloud_visualization.py       # 워드클라우드 시각화
├── 📁 data/                             # 데이터 파일들
│   ├── __init__.py
│   ├── raw/                             # 원본 데이터
│   │   ├── __init__.py
│   │   ├── combined_google_play_reviews.csv
│   │   ├── combined_google_play_reviews_with_names.csv
│   │   └── Google_play_*.csv (16개 앱별 리뷰)
│   ├── processed/                       # 전처리된 데이터
│   │   ├── __init__.py
│   │   └── preprocessed_google_play_reviews.csv
│   └── analysis/                        # 분석 결과 데이터
│       ├── __init__.py
│       └── keyword_clustered_google_play_reviews.csv
├── 📁 results/                          # 분석 결과 및 차트
│   ├── __init__.py
│   ├── keyword_based_clustering_visualizations.png
│   ├── optimal_clusters_analysis.png
│   ├── review_analysis_visualizations.png
│   └── simple_cluster_analysis_visualizations.png
├── 🔧 scripts/                          # 유틸리티 스크립트
│   ├── __init__.py
│   ├── Google_play_app_review_crawler.py # Google Play 리뷰 크롤러
│   └── App_store_app_review_crawler.py   # App Store 리뷰 크롤러
├── 📚 docs/                             # 문서 및 보고서
│   ├── __init__.py
│   └── reports/                         # 분석 보고서
│       ├── __init__.py
│       └── 최종_인사이트_보고서.md        # 최종 분석 보고서
├── 📈 run_analysis.py                   # 전체 분석 파이프라인 실행 스크립트
├── 📋 README.md                         # 프로젝트 개요
└── 📊 requirements.txt                  # Python 패키지 의존성
```

## 🛠️ 설치 및 실행

### 1. 환경 설정
```bash
# Python 3.8+ 설치 필요
pip install -r requirements.txt
```

### 2. 실행 순서
```bash
# 1. 전체 분석 파이프라인 실행 (권장)
python run_analysis.py

# 또는 단계별 실행:
# 2. 데이터 전처리
python data_analysis/data_processing_pipeline.py

# 3. 키워드 기반 군집화
python data_analysis/keyword_based_clustering.py

# 4. 워드클라우드 시각화
python data_visualization/wordcloud_visualization.py
```

## 📊 분석 결과

### 주요 인사이트
1. **접근성 중심 설계의 중요성**: 시각장애인들이 가장 중요하게 여기는 것은 음성 안내와 접근성
2. **AI 음성 인식 기술의 핵심성**: 에이닷, 설리번 등 AI 기반 앱들이 음성 인식 성능에서 높은 평가
3. **음성 인터페이스의 사용성**: 시각장애인들은 음성 중심의 직관적인 인터페이스를 선호
4. **지속적 접근성 개선**: 시각장애인 앱 표준 가이드라인 개발 및 적용 필요

### 군집화 결과
- **군집 1**: 접근성 및 사용성 (40%) - 음성 안내, 화면 읽기
- **군집 2**: 기능 및 성능 (30%) - AI 인식, 음성 인식
- **군집 3**: 디자인 및 UI (20%) - 음성 인터페이스, 터치 감도
- **군집 4**: 문제 및 개선점 (10%) - 음성 안내 부족, 접근성 문제

## 🔍 분석 방법론

### 텍스트 전처리
- 한국어 형태소 분석 및 불용어 제거
- 시각장애인 특화 키워드 사전 구축 및 적용

### 키워드 기반 군집화
- TF-IDF 벡터화를 통한 키워드 중요도 계산
- K-means 클러스터링으로 유사 피드백 그룹화

### 시각화
- Seaborn을 활용한 현대적이고 일관된 시각화
- 워드클라우드로 시각장애인 특화 키워드 분포의 직관적 표현

## 🚀 시각장애인 앱 서비스 기획 방향성

### 1. 접근성 우선 설계
- 음성 안내 강화, 접근성 가이드라인 준수, 음성 피드백 일관성

### 2. AI 음성 인식 최적화
- 음성 인식 정확도 향상, 응답 속도 개선, 자연어 처리 강화

### 3. 음성 중심 UI/UX 설계
- 직관적 음성 메뉴, 터치-음성 조합, 개인화 설정

### 4. 품질 관리 및 사용자 지원
- 접근성 테스트 강화, 오류 대응 시스템, 사용자 피드백 반영

## 📈 시각화 예시

프로젝트는 다음과 같은 시각화를 제공합니다:
- 군집별 워드클라우드
- 최적 군집 수 분석
- 리뷰 분포 및 평점 분석
- 키워드 빈도 분석

## 🤝 기여 방법

1. 이슈 등록: 버그 리포트 또는 기능 요청
2. 포크 및 브랜치 생성
3. 코드 수정 및 테스트
4. Pull Request 생성

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의사항

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 등록해 주세요.

---

**개발자**: AI Assistant  
**최종 업데이트**: 2025년  
**프로젝트 목적**: 시각장애인 앱 서비스 페인포인트 발굴 및 새로운 기획을 위한 근거 마련
