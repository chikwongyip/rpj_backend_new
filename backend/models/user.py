from fastapi import Form
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str = Form(..., min_length=3, max_length=20)
    password: str = Form(..., min_length=8)
    email: EmailStr = Form(...)


class UserLogin(BaseModel):
    username: str = Form(..., min_length=3, max_length=20)
    password: str = Form(..., min_length=8)
    token: Optional[str] = None
    refresh_token: Optional[str] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseModel):
    refresh_token: str
