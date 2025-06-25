from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = Field(default=None, description="数据内容")

    # 快速生成相应方法
    @classmethod
    def success(cls, data: T = None, message: str = "成功"):
        return cls(code=0, message=message, data=data)

    @classmethod
    def error(cls, code: int = 1, message: str = "失败"):
        return cls(code=code, message=message, data=None)
