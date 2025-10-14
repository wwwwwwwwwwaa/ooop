# 인증 시스템 API

FastAPI를 사용한 일반 로그인 및 구글 OAuth 로그인 시스템입니다.

## 주요 기능

- ✅ **일반 로그인**: 이메일/비밀번호 기반 회원가입 및 로그인
- ✅ **구글 OAuth 로그인**: 구글 계정으로 간편 로그인
- ✅ **JWT 토큰 인증**: 안전한 토큰 기반 인증
- ✅ **비밀번호 해싱**: Bcrypt를 사용한 안전한 비밀번호 저장

## 기술 스택

- **FastAPI**: 빠르고 현대적인 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite**: 데이터베이스 (프로덕션에서는 PostgreSQL 권장)
- **JWT**: 토큰 기반 인증
- **Authlib**: OAuth 2.0 클라이언트
- **Passlib**: 비밀번호 해싱

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# Database
DATABASE_URL=sqlite:///./auth.db

# JWT Settings (반드시 변경하세요!)
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth (구글 클라우드 콘솔에서 발급)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

# Application
APP_URL=http://localhost:8000
```

### 3. 구글 OAuth 설정

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성
3. "APIs & Services" > "Credentials"로 이동
4. "OAuth 2.0 Client IDs" 생성
5. 승인된 리디렉션 URI에 `http://localhost:8000/auth/google/callback` 추가
6. Client ID와 Client Secret을 `.env` 파일에 추가

### 4. 서버 실행

```bash
uvicorn app.main:app --reload
```

서버가 실행되면 다음 주소로 접속할 수 있습니다:
- API 서버: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

## API 엔드포인트

### 회원가입 및 로그인

#### 1. 회원가입
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "홍길동"
}
```

#### 2. 일반 로그인 (JSON 형식)
```http
POST /auth/login/json
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

응답:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. 일반 로그인 (Form 형식 - OAuth2 표준)
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

### 구글 로그인

#### 1. 구글 로그인 시작
브라우저에서 다음 URL로 접속:
```
http://localhost:8000/auth/google
```

구글 로그인 페이지로 리다이렉트됩니다.

#### 2. 콜백 (자동 처리)
구글 인증 후 자동으로 `/auth/google/callback`이 호출되며, 토큰이 발급됩니다.

### 사용자 정보

#### 내 정보 조회
```http
GET /auth/me
Authorization: Bearer {access_token}
```

응답:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "홍길동",
  "is_active": true,
  "is_verified": false,
  "is_oauth": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 프로젝트 구조

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 설정 관리
│   ├── database.py          # 데이터베이스 연결
│   ├── api/
│   │   ├── __init__.py
│   │   └── auth.py          # 인증 라우터
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # 보안 유틸리티 (JWT, 비밀번호 해싱)
│   │   └── deps.py          # 의존성 (현재 사용자 가져오기)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # 사용자 모델
│   └── schemas/
│       ├── __init__.py
│       ├── user.py          # 사용자 스키마
│       └── token.py         # 토큰 스키마
├── requirements.txt         # 의존성 목록
├── env.example             # 환경 변수 예시
└── README.md               # 프로젝트 문서
```

## 보안 고려사항

### 프로덕션 배포 전 체크리스트

1. **SECRET_KEY 변경**: 강력하고 무작위한 키로 변경
   ```python
   # Python으로 생성
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **CORS 설정**: `allow_origins`를 특정 도메인만 허용하도록 변경
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

3. **데이터베이스**: SQLite 대신 PostgreSQL 사용
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```

4. **HTTPS**: 프로덕션에서는 반드시 HTTPS 사용

5. **환경 변수 보안**: `.env` 파일을 Git에 커밋하지 말 것

## 사용 예시

### Python으로 API 호출

```python
import requests

# 회원가입
response = requests.post(
    "http://localhost:8000/auth/register",
    json={
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "테스트 사용자"
    }
)
print(response.json())

# 로그인
response = requests.post(
    "http://localhost:8000/auth/login/json",
    json={
        "email": "test@example.com",
        "password": "testpassword"
    }
)
token = response.json()["access_token"]

# 내 정보 조회
response = requests.get(
    "http://localhost:8000/auth/me",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
```

### JavaScript로 API 호출

```javascript
// 회원가입
const registerResponse = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'testpassword',
    full_name: '테스트 사용자'
  })
});

// 로그인
const loginResponse = await fetch('http://localhost:8000/auth/login/json', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'testpassword'
  })
});
const { access_token } = await loginResponse.json();

// 내 정보 조회
const meResponse = await fetch('http://localhost:8000/auth/me', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});
const user = await meResponse.json();
console.log(user);
```

## 문제 해결

### 구글 로그인이 작동하지 않는 경우

1. 구글 클라우드 콘솔에서 OAuth 2.0 Client ID가 제대로 설정되었는지 확인
2. 리디렉션 URI가 정확히 일치하는지 확인
3. `.env` 파일에 올바른 Client ID와 Secret이 입력되었는지 확인

### 데이터베이스 초기화

데이터베이스를 초기화하려면 `auth.db` 파일을 삭제하고 서버를 다시 시작하세요:

```bash
rm auth.db
uvicorn app.main:app --reload
```

## 라이선스

MIT License
