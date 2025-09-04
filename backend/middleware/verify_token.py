import time
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from models.common import BaseResponse
from app_config.auth_config import secret_key, algorithm
from fastapi.responses import JSONResponse

# JWT 验证中间件


async def jwt_middleware(request: Request, call_next):
    # 跳过不需要验证的路由
    return await call_next(request)
    if request.url.path in ["/login", "/docs", "/openapi.json", "/admin/company/info", "/admin/company/edit", "/admin/brand/add"]:
        return await call_next(request)

    # 获取 Authorization 头
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"code": 2, "message": "缺少或无效的 Authorization 头"},
            headers={"WWW-Authenticate": "Bearer"}
        )
    # 提取 token
    token = auth_header[len("Bearer "):]

    try:
        # 解码 JWT
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if not username:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"code": 2, "detail": "无效的 token：缺少用户名"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        if "exp" in payload and payload['exp'] < time.time():
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"code": 2, "detail": "token 已过期"},
                headers={"WWW-Authenticate": "Bearer"}
            )

        # 将用户信息注入 request.state
        request.state.user = username

    except JWTError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"code": 2, "detail": "无法验证 token"},
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 继续处理请求
    response = await call_next(request)
    return response
