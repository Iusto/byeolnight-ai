#!/usr/bin/env python3
"""
등록된 뉴스 게시글 확인
"""
import requests
from config import SPRING_SERVER_URL

def check_recent_posts():
    """최근 등록된 게시글 확인"""
    print("=== 최근 등록된 뉴스 확인 ===")
    
    # 스프링 서버에 게시글 목록 API가 있다면 사용
    # 예시: GET /api/public/posts?category=NEWS&limit=5
    
    try:
        # 실제 API 엔드포인트에 맞게 수정 필요
        response = requests.get(f"{SPRING_SERVER_URL}/api/public/posts", 
                              params={"category": "NEWS", "limit": 5}, 
                              timeout=10)
        
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ 최근 뉴스 {len(posts)}개:")
            for post in posts:
                print(f"  - {post.get('title', 'N/A')}")
        else:
            print(f"❌ 게시글 조회 실패: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API 호출 실패: {e}")
        print("💡 스프링 서버 관리자 페이지에서 직접 확인하세요.")

def send_simple_test():
    """간단한 테스트 뉴스 전송"""
    print("\n=== 간단한 테스트 뉴스 전송 ===")
    
    test_news = {
        "title": f"[테스트] 뉴스 등록 확인 테스트",
        "content": "이 뉴스가 보이면 시스템이 정상 작동하는 것입니다."
    }
    
    try:
        response = requests.post(
            f"{SPRING_SERVER_URL}/api/public/ai/news",
            json=test_news,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 테스트 뉴스 전송 성공!")
            print("💡 스프링 서버 뉴스 게시판을 확인하세요.")
        else:
            print(f"❌ 테스트 뉴스 전송 실패: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

if __name__ == "__main__":
    send_simple_test()
    check_recent_posts()
    
    print("\n=== 확인 방법 ===")
    print("1. 스프링 서버 웹 인터페이스에서 뉴스 게시판 확인")
    print("2. 데이터베이스에서 posts 테이블 확인")
    print("3. 스프링 서버 로그에서 성공 메시지 확인")