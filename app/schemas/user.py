from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """사용자 생성 스키마"""
    password: str


class UserLogin(BaseModel):
    """사용자 로그인 스키마"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """사용자 업데이트 스키마"""
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    id: int
    is_active: bool
    is_verified: bool
    is_oauth: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

