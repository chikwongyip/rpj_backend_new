from fastapi import APIRouter
from models.user import UserLogin, UserCreate, RefreshToken
from models.common import BaseResponse
from uitls.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from schemas.user import Users
from db.db import get_db

router = APIRouter(prefix='/admin/users', tags=['用户管理'])


@router.post('/login')
async def login(user: UserLogin):
    with get_db() as session:
        db_user = session.query(Users).filter_by(
            name=user.username).first()

    res = verify_password(user.password, db_user.hashed_password)

    if res:
        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        data = {"token_type": "bearer",
                "access_token": access_token, "refresh_token": refresh_token}

        return BaseResponse.success(data=data)
    else:

        return BaseResponse.error(code=1, message="登录失败")


@router.post('/regist')
async def regist(user: UserCreate):
    with get_db() as session:

        hashed_password = hash_password(user.password)
        new_user = Users(
            name=user.username, hashed_password=hashed_password, email=user.email)
        res = session.add(new_user)
        session.commit()
    return res


@router.post("/refresh_token")
async def refresh_token(request: RefreshToken):
    playload = verify_token(request.refresh_token)
    if not playload:
        return BaseResponse.error(code=401, message="无效 refresh token")
    username = playload.get("sub")
    if not username:
        return BaseResponse.error(code=401, message="Token 数据异常")
    access_token = create_access_token(username)
    return BaseResponse.success(data={"access_token": access_token})
