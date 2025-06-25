from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from app_config.auth_config import secret_key, algorithm, access_token_expire_minutes, refresh_token_expire_days
# 配置密码哈希策略
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """生成密码哈希值"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配哈希"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str):
    expires = datetime.utcnow()+timedelta(minutes=access_token_expire_minutes)
    playload = {"sub": username, "exp": expires}
    return jwt.encode(playload, secret_key, algorithm)


def create_refresh_token(username: str):
    expires = datetime.utcnow()+timedelta(days=refresh_token_expire_days)
    playload = {"sub": username, "exp": expires}
    return jwt.encode(playload, secret_key, algorithm)


def verify_token(token: str):
    try:
        playload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return playload
    except JWTError:
        return None
