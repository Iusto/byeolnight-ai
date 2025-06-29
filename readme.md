# 🌟 Byeolnight AI 크롤링 시스템

천문학 관련 뉴스와 전국 천문대 일정을 자동으로 크롤링하여 스프링 서버로 전송하는 **FastAPI 기반 통합 크롤링 시스템**입니다.

## 🎯 주요 특징
- **분리형 크롤링**: 뉴스와 천문대 일정 독립 처리
- **전국 20개 천문대**: KASI, 공립과학관, 지역천문대 포함
- **자동 스케줄링**: APScheduler 기반 안정적 운영
- **이중 API 지원**: Public/Admin 엔드포인트

## 주요 기능

### 뉴스 소스
- **NASA RSS**: 미국 항공우주국 뉴스
- **ESA RSS**: 유럽우주국 뉴스  
- **한국천문연구원**: 보도자료 크롤링
- **사이언스타임즈**: 우주/병계 카테고리 크롤링

### 자동 스케줄링
- 매일 오전 6시, 오후 12시 자동 실행
- APScheduler를 사용한 안정적인 스케줄링

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 설정 파일 수정
`config.py` 파일에서 다음 설정을 확인/수정하세요:
```python
SPRING_SERVER_URL = "http://localhost:8080"
API_KEY = "your-api-key-here"  # 스프링 서버의 API 키와 일치해야 함
```

### 3. 스프링 서버 연결 테스트
```bash
python test_connection.py
```

### 4. FastAPI 서버 실행
```bash
python main.py
```

서버는 `http://localhost:9000`에서 실행됩니다.

## API 엔드포인트

### FastAPI 엔드포인트
- `GET /`: 서버 상태 확인
- `GET /health`: 헬스체크 및 스프링 서버 연결 상태
- `GET /status`: 스케줄러 상태 확인
- `POST /crawl-now`: 수동 크롤링 실행

### 스프링 서버 연동
- **Admin 엔드포인트**: `/api/admin/crawler/news` (API 키 필요)
- **Public 엔드포인트**: `/api/public/ai/news` (API 키 불필요)

## 스프링 서버 설정 요구사항

### 1. system 계정 생성
스프링 서버에 `system@byeolnight.com` 계정이 존재해야 합니다.

### 2. API 키 설정
`CrawlerConfig`에서 API 키를 설정하고 FastAPI의 `config.py`와 일치시켜야 합니다.

### 3. CORS 설정 (필요시)
FastAPI에서 스프링 서버로 요청을 보내므로 CORS 설정이 필요할 수 있습니다.

## 로그 확인

실행 중 로그를 통해 다음을 확인할 수 있습니다:
- 크롤링 성공/실패 상태
- 스프링 서버 전송 결과
- 스케줄러 실행 상태

## 문제 해결

### 연결 오류 시
1. 스프링 서버가 실행 중인지 확인
2. `test_connection.py`로 연결 테스트
3. API 키가 올바른지 확인
4. 방화벽/포트 설정 확인

### 크롤링 실패 시
1. 인터넷 연결 상태 확인
2. 대상 웹사이트 접근 가능 여부 확인
3. User-Agent 헤더 설정 확인