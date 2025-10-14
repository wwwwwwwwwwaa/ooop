from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth
from app.database import init_db
from app.config import settings

app = FastAPI(
    title="인증 시스템 API",
    description="일반 로그인 및 구글 OAuth 로그인 기능을 제공하는 API",
    version="1.0.0"
)

# 세션 미들웨어 추가 (OAuth에 필요)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    init_db()
    print("✅ 데이터베이스 초기화 완료")


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "인증 시스템 API에 오신 것을 환영합니다",
        "docs": "/docs",
        "endpoints": {
            "회원가입": "POST /auth/register",
            "일반 로그인 (Form)": "POST /auth/login",
            "일반 로그인 (JSON)": "POST /auth/login/json",
            "구글 로그인": "GET /auth/google",
            "내 정보": "GET /auth/me"
        }
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

