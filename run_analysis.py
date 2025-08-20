#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
앱 리뷰 크롤링 및 분석 메인 실행 스크립트

이 스크립트는 전체 분석 파이프라인을 순차적으로 실행합니다:
1. 데이터 전처리
2. 키워드 기반 군집화
3. 워드클라우드 시각화
4. 최종 결과 생성

사용법:
    python run_analysis.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """섹션 헤더를 출력하는 함수"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_step(step_num, description):
    """단계별 진행상황을 출력하는 함수"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def _safe_decode(output_bytes: bytes) -> str:
    """Windows 콘솔 인코딩 이슈를 회피하며 안전하게 디코딩"""
    if output_bytes is None:
        return ''
    for enc in ('utf-8', 'cp949', 'euc-kr', 'latin1'):
        try:
            return output_bytes.decode(enc, errors='ignore')
        except Exception:
            continue
    return output_bytes.decode('utf-8', errors='ignore')


def run_script(script_path, description):
    """Python 스크립트를 실행하는 함수"""
    try:
        print(f"🔄 {description} 실행 중...")
        start_time = time.time()

        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        result = subprocess.run([sys.executable, script_path], capture_output=True, env=env)

        execution_time = time.time() - start_time

        stdout_text = _safe_decode(result.stdout)
        stderr_text = _safe_decode(result.stderr)

        if result.returncode == 0:
            print(f"✅ {description} 완료 (소요시간: {execution_time:.1f}초)")
            if stdout_text:
                print("📤 출력:")
                print(stdout_text[-800:])  # 마지막 800자만 출력
        else:
            print(f"❌ {description} 실패")
            if stderr_text:
                print("📤 오류:")
                print(stderr_text)
            return False

    except Exception as e:
        print(f"❌ 스크립트 실행 중 오류 발생: {str(e)}")
        return False

    return True

def check_dependencies():
    """필요한 파일들이 존재하는지 확인하는 함수"""
    print_step(0, "의존성 및 파일 확인")
    
    required_files = [
        'data_analysis/data_processing_pipeline.py',
        'data_analysis/keyword_based_clustering.py',
        'data_visualization/wordcloud_visualization.py'  
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 다음 파일들이 누락되었습니다:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ 모든 필요한 파일이 존재합니다.")
    return True

def check_data_files():
    """데이터 파일들이 존재하는지 확인하는 함수"""
    print_step(0, "데이터 파일 확인")
    
    # 기본 데이터 파일 확인
    data_files = [
        'data/raw/combined_google_play_reviews.csv',
        'data/processed/preprocessed_google_play_reviews.csv'
    ]
    
    existing_files = []
    for file_path in data_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
    
    if not existing_files:
        print("⚠️  데이터 파일이 없습니다. 먼저 리뷰 크롤링을 실행해주세요.")
        print("   python scripts/Google_play_app_review_crawler.py")
        return False
    
    print("✅ 데이터 파일 확인 완료:")
    for file_path in existing_files:
        file_size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
        print(f"   - {file_path} ({file_size:.1f} MB)")
    
    return True

def main():
    """메인 실행 함수"""
    print_header("앱 리뷰 크롤링 및 분석 파이프라인")
    print("📅 시작 시간:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # 1. 의존성 확인
    if not check_dependencies():
        print("\n❌ 의존성 확인 실패. 프로젝트 구조를 확인해주세요.")
        return
    
    # 2. 데이터 파일 확인
    if not check_data_files():
        print("\n❌ 데이터 파일 확인 실패. 먼저 데이터를 준비해주세요.")
        return
    
    # 3. 데이터 전처리
    print_step(1, "데이터 전처리")
    if not run_script('data_analysis/data_processing_pipeline.py', '데이터 전처리'):
        print("\n❌ 데이터 전처리 실패. 분석을 중단합니다.")
        return
    
    # 4. 키워드 기반 군집화
    print_step(2, "키워드 기반 군집화")
    if not run_script('data_analysis/keyword_based_clustering.py', '키워드 기반 군집화'):
        print("\n❌ 키워드 기반 군집화 실패. 분석을 중단합니다.")
        return
    
    # 5. 워드클라우드 시각화
    print_step(3, "워드클라우드 시각화")
    if not run_script('data_visualization/wordcloud_visualization.py', '워드클라우드 시각화'):
        print("\n⚠️  워드클라우드 시각화 실패했지만 계속 진행합니다.")
    

    # 6. 결과 요약
    print_step(6, "결과 요약")
    print("🎉 분석 파이프라인이 성공적으로 완료되었습니다!")
    
    # 생성된 파일들 확인
    result_files = [
        'data/processed/preprocessed_google_play_reviews.csv',
        'data/analysis/keyword_clustered_google_play_reviews.csv',
        'results/keyword_based_clustering_visualizations.png',
        'data/analysis/vi_app_counts.csv',
        'data/analysis/vi_cluster_summary.csv',
        'data/analysis/cluster_examples.md',
        'data/analysis/cluster_sentiment_keywords.md',
    ]
    
    print("\n📁 생성된 결과 파일들:")
    for file_path in result_files:
        if Path(file_path).exists():
            file_size = Path(file_path).stat().st_size
            if file_size > 1024 * 1024:  # MB
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            else:
                size_str = f"{file_size / 1024:.1f} KB"
            print(f"   ✅ {file_path} ({size_str})")
        else:
            print(f"   ❌ {file_path} (생성되지 않음)")
    
    print(f"\n📅 완료 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 다음 단계:")
    print("   1. 최종_인사이트_보고서.md 파일을 확인하세요")
    print("   2. 생성된 시각화 파일들을 검토하세요")
    print("   3. 필요시 추가 분석을 진행하세요")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 분석이 중단되었습니다.")
    except Exception as e:
        print(f"\n\n❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
        import traceback
        traceback.print_exc()
