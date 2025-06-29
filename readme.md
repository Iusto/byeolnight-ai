# 🌌 Byeolnight AI

FastAPI 기반으로 동작하는 **별 헤는 밤 AI 서버**입니다.  
뉴스 크롤링, 추천 시스템, 자연어 처리 등 다양한 AI 기능을 제공합니다.

---

## ✅ 현재 기능

### 🔭 뉴스 크롤링
- `Science Times`에서 우주 뉴스 2건을 매일 가져와 Spring 서버에 제공
- `/news` API 호출 시 JSON 형식 뉴스 반환

---

## 🚀 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행
uvicorn main:app --reload
