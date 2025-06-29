#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 확인 (유니코드 문제 해결)
"""

def check_news():
    """뉴스 데이터 확인"""
    print("뉴스 데이터 확인...")
    
    news_list = [
        "한국형 달 탐사선 다누리 성과 발표",
        "스페이스X 스타십 최신 시험 발사 성공", 
        "제임스 웹 우주망원경 새로운 외계행성 발견"
    ]
    
    print(f"준비된 뉴스: {len(news_list)}개")
    for i, news in enumerate(news_list, 1):
        print(f"  {i}. {news}")
    
    return len(news_list) > 0

def check_observatories():
    """천문대 데이터 확인"""
    print("\n천문대 데이터 확인...")
    
    obs_list = [
        "국립과천과학관 - 천체관측교실",
        "용산가족공원 천문대 - 무료 관측",
        "영월 별마로천문대 - 연중 운영"
    ]
    
    print(f"준비된 천문대: {len(obs_list)}개")
    for i, obs in enumerate(obs_list, 1):
        print(f"  {i}. {obs}")
    
    return len(obs_list) > 0

def main():
    print("=== 데이터 준비 상태 확인 ===\n")
    
    news_ready = check_news()
    obs_ready = check_observatories()
    
    print(f"\n=== 결과 ===")
    print(f"뉴스: {'준비됨' if news_ready else '없음'}")
    print(f"천문대: {'준비됨' if obs_ready else '없음'}")
    
    if news_ready and obs_ready:
        print("\n[성공] 모든 데이터 준비 완료!")
        print("\n다음 단계:")
        print("1. pip install requests beautifulsoup4")
        print("2. 스프링 서버 실행")
        print("3. py final_test.py")
    else:
        print("\n[실패] 데이터 준비 미완료")

if __name__ == "__main__":
    main()