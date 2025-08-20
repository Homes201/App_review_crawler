# 📁 프로젝트 폴더 구조 상세 설명

## 🎯 프로젝트 개요
시각장애인 앱 서비스의 사용자 경험을 분석하여 페인포인트를 발굴하고, 새로운 기획을 위한 근거를 마련하는 프로젝트입니다.

## 📂 폴더 구조 상세

### 🔧 루트 디렉토리
```
App_review_crawler/
├── 📋 README.md                    # 프로젝트 개요 및 사용법
├── 📊 requirements.txt             # Python 패키지 의존성
├── 📈 run_analysis.py             # 전체 분석 파이프라인 실행 스크립트
└── 📁 PROJECT_STRUCTURE.md        # 이 파일 (폴더 구조 설명)
```

### 📊 data_analysis/ - 데이터 분석 스크립트
```
data_analysis/
├── __init__.py                     # Python 패키지 초기화
├── keyword_based_clustering.py     # 키워드 기반 군집화 분석
└── data_processing_pipeline.py     # 데이터 전처리 파이프라인
```

**주요 기능:**
- `keyword_based_clustering.py`: TF-IDF 기반 키워드 분석 및 K-means 군집화
- `data_processing_pipeline.py`: 한국어 텍스트 정제, 불용어 제거, 데이터 정규화

### 🎨 data_visualization/ - 시각화 스크립트
```
data_visualization/
├── __init__.py                     # Python 패키지 초기화
└── wordcloud_visualization.py     # 워드클라우드 시각화 생성
```

**주요 기능:**
- `wordcloud_visualization.py`: 군집별 키워드 워드클라우드 생성
- Seaborn 기반 현대적 시각화 스타일 적용

### 📁 data/ - 데이터 파일들
```
data/
├── __init__.py                     # Python 패키지 초기화
├── raw/                           # 원본 데이터
│   ├── __init__.py
│   ├── combined_google_play_reviews.csv           # 통합 리뷰 데이터
│   ├── combined_google_play_reviews_with_names.csv # 앱명 포함 통합 데이터
│   └── Google_play_*.csv                          # 16개 앱별 개별 리뷰 파일
├── processed/                     # 전처리된 데이터
│   ├── __init__.py
│   └── preprocessed_google_play_reviews.csv       # 전처리 완료된 데이터
└── analysis/                      # 분석 결과 데이터
    ├── __init__.py
    └── keyword_clustered_google_play_reviews.csv  # 군집화 결과 데이터
```

**데이터 설명:**
- **raw/**: 크롤링된 원본 리뷰 데이터 (110,000+ 개 리뷰)
- **processed/**: 텍스트 정제, 불용어 제거 등 전처리 완료된 데이터
- **analysis/**: 키워드 기반 군집화 분석 결과 데이터

### 📁 results/ - 분석 결과 및 차트
```
results/
├── __init__.py                     # Python 패키지 초기화
├── keyword_based_clustering_visualizations.png    # 군집화 시각화
├── optimal_clusters_analysis.png                  # 최적 군집 수 분석
├── review_analysis_visualizations.png             # 리뷰 분석 시각화
└── simple_cluster_analysis_visualizations.png     # 단순 군집 분석 시각화
```

**시각화 설명:**
- **keyword_based_clustering_visualizations.png**: 4개 군집별 특성 시각화
- **optimal_clusters_analysis.png**: 엘보우 메서드로 최적 군집 수 결정
- **review_analysis_visualizations.png**: 리뷰 분포 및 평점 분석
- **simple_cluster_analysis_visualizations.png**: 기본 군집 분석 결과

### 🔧 scripts/ - 유틸리티 스크립트
```
scripts/
├── __init__.py                     # Python 패키지 초기화
├── Google_play_app_review_crawler.py  # Google Play Store 리뷰 크롤러
└── App_store_app_review_crawler.py    # App Store 리뷰 크롤러
```

**주요 기능:**
- **Google_play_app_review_crawler.py**: 16개 시각장애인 앱의 리뷰 수집
- **App_store_app_review_crawler.py**: iOS 앱 리뷰 수집 (향후 확장용)

### 📚 docs/ - 문서 및 보고서
```
docs/
├── __init__.py                     # Python 패키지 초기화
└── reports/                        # 분석 보고서
    ├── __init__.py
    └── 최종_인사이트_보고서.md      # 시각장애인 앱 서비스 페인포인트 분석 보고서
```

**문서 설명:**
- **최종_인사이트_보고서.md**: 110,000+ 리뷰 분석을 통한 핵심 인사이트 및 기획 방향성

## 🚀 실행 순서

### 1. 전체 파이프라인 실행 (권장)
```bash
python run_analysis.py
```

### 2. 단계별 실행
```bash
# 데이터 전처리
python data_analysis/data_processing_pipeline.py

# 키워드 기반 군집화
python data_analysis/keyword_based_clustering.py

# 워드클라우드 시각화
python data_visualization/wordcloud_visualization.py
```

## 📊 데이터 흐름

```
1. 크롤링 → data/raw/ (원본 데이터)
2. 전처리 → data/processed/ (정제된 데이터)
3. 분석 → data/analysis/ (군집화 결과)
4. 시각화 → results/ (차트 및 그래프)
5. 보고서 → docs/reports/ (최종 인사이트)
```

## 🔍 분석 방법론

### 텍스트 전처리
- 한국어 형태소 분석
- 시각장애인 특화 키워드 사전 적용
- 불용어 제거 및 정규화

### 군집화 분석
- TF-IDF 벡터화
- K-means 클러스터링
- 엘보우 메서드로 최적 군집 수 결정

### 시각화
- Seaborn 기반 현대적 디자인
- 워드클라우드로 키워드 분포 표현
- 군집별 특성 비교 분석

## 💡 주요 인사이트

### 군집별 특성
1. **접근성 및 사용성 (40%)**: 음성 안내, 화면 읽기
2. **기능 및 성능 (30%)**: AI 인식, 음성 인식
3. **디자인 및 UI (20%)**: 음성 인터페이스, 터치 감도
4. **문제 및 개선점 (10%)**: 음성 안내 부족, 접근성 문제

### 기획 방향성
- **접근성 우선 설계**: 음성 안내 강화, 가이드라인 준수
- **AI 음성 인식 최적화**: 정확도 향상, 응답 속도 개선
- **음성 중심 UI/UX**: 직관적 메뉴, 터치-음성 조합
- **품질 관리 강화**: 접근성 테스트, 오류 대응 시스템

## 📝 파일 명명 규칙

### 데이터 파일
- `combined_*`: 통합된 데이터
- `preprocessed_*`: 전처리 완료된 데이터
- `*_clustered_*`: 군집화 분석 결과

### 시각화 파일
- `*_visualizations.png`: 복합 시각화 결과
- `*_analysis.png`: 특정 분석 결과

### 스크립트 파일
- `*_pipeline.py`: 데이터 처리 파이프라인
- `*_clustering.py`: 군집화 분석
- `*_visualization.py`: 시각화 생성

## 🔧 유지보수 및 확장

### 새로운 앱 추가
1. `scripts/Google_play_app_review_crawler.py`에 앱 ID 추가
2. 크롤링 실행하여 `data/raw/`에 데이터 추가
3. 전체 파이프라인 재실행

### 새로운 분석 기법 추가
1. `data_analysis/` 폴더에 새로운 스크립트 추가
2. `run_analysis.py`에 새로운 단계 추가
3. 결과를 `data/analysis/`에 저장

### 새로운 시각화 추가
1. `data_visualization/` 폴더에 새로운 스크립트 추가
2. 결과를 `results/` 폴더에 저장
3. `docs/reports/`에 분석 결과 문서화

---

**문서 작성일**: 2025년  
**프로젝트 버전**: 1.0  
**문서 담당**: AI Assistant
