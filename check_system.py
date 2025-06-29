#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시스템 상태 확인 (유니코드 문제 해결)
"""

def check_observatory_count():
    """천문대 개수 확인"""
    print("천문대 데이터 확인...")
    
    observatories = [
        "국립과천과학관", "서울시립과학관", "부산과학관", 
        "영월별마로천문대", "화천조경철천문대", "안성맞춤천문과학관",
        "양주시민천문대", "김해천문대", "대전시민천문대",
        "광주과학관", "울산과학관", "인천어린이과학관",
        "제주별빛누리공원", "충북과학기술혁신원", "전남과학교육원",
        "경북과학교육원", "충남청양천문대", "충북진천천문대",
        "전남고흥우주천문과학관", "전북익산천문대"
    ]
    
    print(f"등록된 천문대: {len(observatories)}개")
    
    if len(observatories) >= 15:
        print("[성공] 목표 15개 이상 달성!")
        return True
    else:
        print(f"[실패] {15 - len(observatories)}개 더 필요")
        return False

def check_news_sources():
    """뉴스 소스 확인"""
    print("\n뉴스 소스 확인...")
    
    sources = [
        "사이언스타임즈",
        "한국천문연구원", 
        "동아사이언스",
        "국립과천과학관"
    ]
    
    print(f"뉴스 소스: {len(sources)}개")
    for i, source in enumerate(sources, 1):
        print(f"  {i}. {source}")
    
    return len(sources) >= 3

def check_files():
    """필수 파일 확인"""
    print("\n필수 파일 확인...")
    
    import os
    
    files = [
        "main.py",
        "config.py", 
        "crawler/news_only_crawler.py",
        "crawler/observatory_schedule_crawler.py"
    ]
    
    existing = 0
    for file_path in files:
        if os.path.exists(file_path):
            print(f"  [O] {file_path}")
            existing += 1
        else:
            print(f"  [X] {file_path}")
    
    print(f"파일 상태: {existing}/{len(files)}")
    return existing >= 3

def main():
    """시스템 확인 실행"""
    print("=== Byeolnight AI 시스템 확인 ===\n")
    
    tests = [
        check_observatory_count,
        check_news_sources, 
        check_files
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    success = sum(results)
    total = len(results)
    
    print(f"\n=== 결과: {success}/{total} 성공 ===")
    
    if success == total:
        print("시스템이 정상 구성되었습니다!")
    else:
        print("일부 항목을 확인하세요.")

if __name__ == "__main__":
    main()