from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from app_config.auth_config import secret_key, algorithm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的 Token 或用户未认证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        playload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = playload.get("sub")
        if username is None:
            raise credentials_exception
    except JWSError:
        raise credentials_exception
