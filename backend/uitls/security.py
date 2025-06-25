from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
# 配置密码哈希策略
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-please-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Access Token 有效期短
REFRESH_TOKEN_EXPIRE_DAYS = 7     # Refresh Token 有效期长


def hash_password(password: str) -> str:
    """生成密码哈希值"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配哈希"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str):
    expires = datetime.utcnow()+timedelta(minutes=30)
    playload = {"sub": username, "exp": expires}
    return jwt.encode(playload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str):
    expires = datetime.utcnow()+timedelta(days=7)
    playload = {"sub": username, "exp": expires}
    return jwt.encode(playload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return get_user(playload['sub'])
    except JWTError:
        return None
    # def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    #     to_encode = data.copy()
    #     if expires_delta:
    #         expire = datetime.utcnow() + expires_delta
    #     else:
    #         expire = datetime.utcnow() + timedelta(minutes=15)
    #     to_encode.update({"exp": expire})
    #     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #     return encoded_jwt

    # def verify_refresh_token(refresh_token: str):
    #     try:
    #         payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    #         username: str = payload.get("sub")
    #         if username is None:
    #             return None
    #         # 验证是否与数据库中存储的 Refresh Token 一致
    #         user = fake_users_db.get(username)
    #         if user and user.refresh_token == refresh_token:
    #             return user
    #     except JWTError:
    #         return None
    #     return None
