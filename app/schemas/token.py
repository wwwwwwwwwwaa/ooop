from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """토큰 응답 스키마"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰 데이터 스키마"""
    email: Optional[str] = None

