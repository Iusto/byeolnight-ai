#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def count_observatories():
    """천문대 개수를 확인하는 함수"""
    
    # KASI 천문대들 (3개)
    kasi_observatories = [
        "한국천문연구원 본원",
        "보현산천문대", 
        "소백산천문대"
    ]
    
    # 공립 과학관 및 천문대 (3개)
    public_observatories = [
        "국립과천과학관",
        "서울시립과학관",
        "부산과학관"
    ]
    
    # 지역 천문대 및 과학관 (14개)
    regional_observatories = [
        "영월별마로천문대",
        "화천조경철천문대", 
        "안성맞춤천문과학관",
        "양주시민천문대",
        "김해천문대",
        "대전시민천문대",
        "광주과학관",
        "울산과학관", 
        "인천어린이과학관",
        "제주별빛누리공원",
        "충북과학기술혁신원 천문대",
        "전남과학교육원 천문대",
        "경북과학교육원 천문대"
    ]
    
    total_count = len(kasi_observatories) + len(public_observatories) + len(regional_observatories)
    
    print("=== 전국 천문대 현황 ===")
    print(f"KASI 천문대: {len(kasi_observatories)}개")
    print(f"공립 과학관: {len(public_observatories)}개") 
    print(f"지역 천문대: {len(regional_observatories)}개")
    print(f"총 천문대 수: {total_count}개")
    print()
    
    if total_count >= 15:
        print("[성공] 목표 달성! 15개 이상의 천문대가 등록되었습니다.")
    else:
        print(f"[실패] 목표 미달성. {15 - total_count}개 더 필요합니다.")
    
    print("\n=== 등록된 천문대 목록 ===")
    all_observatories = kasi_observatories + public_observatories + regional_observatories
    for i, obs in enumerate(all_observatories, 1):
        print(f"{i:2d}. {obs}")
    
    return total_count

if __name__ == "__main__":
    count_observatories()