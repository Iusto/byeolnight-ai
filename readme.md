# 🌟 Byeolnight AI 우주 뉴스 크롤링 시스템

한국인을 위한 **우주 뉴스 전문 크롤링 시스템**입니다. 구글 뉴스 RSS를 활용하여 최신 우주 관련 뉴스를 수집하고, AI 요약과 함께 스프링 서버로 전송합니다.

## 🎯 주요 특징
- **실시간 뉴스 수집**: 구글 뉴스 RSS 기반 최신 우주 뉴스
- **AI 요약 시스템**: 뉴스별 맞춤형 AI 요약 생성
- **원문 내용 추출**: 실제 기사 본문과 이미지 수집
- **캐시 방지**: 매번 다른 최신 뉴스 수집 보장
- **한국어 최적화**: 한국 언론사 특화 크롤링

## 🔧 핵심 기능

### 뉴스 수집 시스템
- **구글 뉴스 RSS**: 우주 관련 최신 뉴스 자동 수집
- **실제 기사 추출**: 구글 뉴스 리다이렉트를 통한 원문 수집
- **이미지 추출**: 기사 관련 이미지 자동 수집
- **중복 제거**: 동일 뉴스 필터링
- **날짜 필터링**: 최근 7일 이내 뉴스만 수집

### AI 요약 시스템
- **맞춤형 요약**: 뉴스 내용에 따른 구체적 요약
- **키워드 추출**: 우주 관련 핵심 키워드 자동 추출
- **품질 검증**: AI 기반 뉴스 품질 평가

### 자동 스케줄링
- **우주 뉴스**: 매일 오전 6시, 오후 12시
- APScheduler 기반 안정적 운영

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install requests beautifulsoup4 python-dateutil fastapi uvicorn apscheduler urllib3 feedparser
```

또는

```bash
pip install -r requirements.txt
```

### 2. 설정 파일 수정
`config.py` 파일에서 스프링 서버 설정:
```python
SPRING_SERVER_URL = "http://localhost:8080"
API_KEY = "your-api-key-here"
```

### 3. 테스트 실행
```bash
python final_test.py
```

### 4. FastAPI 서버 실행
```bash
python main.py
```

서버는 `http://localhost:9000`에서 실행됩니다.

## 📡 API 엔드포인트

### FastAPI 엔드포인트
- `GET /`: 서버 상태 확인
- `GET /health`: 헬스체크 및 스프링 서버 연결 상태
- `GET /status`: 스케줄러 상태 확인
- `POST /crawl-news`: 수동 뉴스 크롤링 실행

### 스프링 서버 연동
- **뉴스 엔드포인트**: `/api/admin/crawler/news`
- **데이터 형식**: JSON (title, content, type, authorId, category, source)

## ⚙️ 스프링 서버 설정

### 1. 봇 계정 설정
스프링 서버에 `newsbot` 계정이 존재해야 합니다.

### 2. API 키 설정
`CrawlerConfig`에서 API 키를 설정하고 FastAPI의 `config.py`와 일치시켜야 합니다.

### 3. Admin API 엔드포인트
`/api/admin/crawler/news` 엔드포인트가 활성화되어 있어야 합니다.

## 📊 로그 및 모니터링

### 로그 파일
- `logs/crawler.log`: 크롤링 실행 로그
- `logs/error.log`: 오류 로그

### 확인 가능한 정보
- 뉴스 수집 성공/실패 상태
- AI 요약 생성 결과
- 스프링 서버 전송 결과
- 스케줄러 실행 상태

## 🧪 테스트

### 전체 시스템 테스트
```bash
python final_test.py
```

### 수동 뉴스 크롤링
```bash
python -c "import asyncio; from crawler.news_only_crawler import crawl_news_only; asyncio.run(crawl_news_only())"
```

## 🔧 문제 해결

### 연결 오류 시
1. 스프링 서버 실행 상태 확인
2. API 키 일치 여부 확인
3. 방화벽/포트 설정 확인

### 크롤링 실패 시
1. 인터넷 연결 상태 확인
2. 구글 뉴스 RSS 접근 가능 여부 확인
3. User-Agent 차단 여부 확인

## 🌟 시스템 특징

### 캐시 방지 시스템
- 매번 다른 파라미터로 최신 뉴스 수집
- 랜덤 User-Agent 사용
- Cache-Control 헤더 적용

### AI 요약 품질
- 뉴스 내용별 맞춤형 요약
- 우주 관련 키워드 자동 추출
- 품질 검증을 통한 필터링

### 원문 추출 기술
- 구글 뉴스 리다이렉트 추적
- 한국 언론사 특화 크롤링
- 이미지 자동 수집

## 📁 프로젝트 구조

```
byeolnight-ai/
├── ai/                    # AI 요약 시스템
│   └── news_evaluator.py
├── crawler/               # 크롤링 엔진
│   ├── news_only_crawler.py
│   └── optimized_news_crawler.py
├── utils/                 # 유틸리티
│   ├── logger_setup.py
│   └── simple_sender.py
├── config.py             # 설정 파일
├── main.py              # FastAPI 서버
├── final_test.py        # 테스트 스크립트
└── requirements.txt     # 의존성
```