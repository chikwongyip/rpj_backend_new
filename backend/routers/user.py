from fastapi import APIRouter
from models.user import UserLogin, UserCreate
from models.common import Response
from uitls.security import hash_password, verify_password, create_access_token, create_refresh_token
from schemas.user import Users
from db.db import get_db

router = APIRouter(prefix='/admin/users', tags=['用户管理'])


@router.post('/login')
async def login(user: UserLogin):
    with get_db() as session:
        db_user = session.query(Users).filter_by(
            name=user.username).first()

    res = verify_password(user.password, db_user.hashed_password)
    res = Response()
    if res:
        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)
        res.code = 0
        res.message = "登录成功"
        res.data = {"username": user.username,
                    "access_token": access_token, "refresh_token": refresh_token}

        return res
    else:
        res.code = 1
        res.message = "登录失败"
        res.data = ""
        return res


@router.post('/regist')
async def regist(user: UserCreate):
    with get_db() as session:

        hashed_password = hash_password(user.password)
        new_user = Users(
            name=user.username, hashed_password=hashed_password, email=user.email)
        res = session.add(new_user)
        session.commit()
    return res
