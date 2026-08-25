# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

"rpj" 网站的 FastAPI 管理后台（中文后台管理系统）。业务域包括：用户、企业信息、品牌、产品、产品图片、产品附件。文件上传至阿里云 OSS，数据存储在 MySQL（数据库名 `rpj`）。

## 常用命令

```bash
# 启动 MySQL 8.0 + Redis（端口 3306 / 6379）
cd service/compose && docker compose up -d

# 启动 API 服务 —— 必须在 backend/ 目录下执行（main.py 使用顶层导入，如 `from routers import ...`）
cd backend && uvicorn main:app --reload --port 8000
# Swagger 文档：http://localhost:8000/docs
```

本仓库**没有测试框架，也没有 lint/格式化配置**。根目录的 `test.py` 是一份被整体注释掉的 JWT 参考代码，不是测试文件（且 `test.*` 已被 gitignore）。

`requirement.txt` 不完整（只写了 `passlib[bcrypt]`）。根据代码导入推断，实际运行时依赖为：`fastapi`、`uvicorn`、`sqlalchemy`、`mysql-connector-python`、`python-jose`、`passlib[bcrypt]`、`oss2`、`python-multipart`、`email-validator`。

OSS 上传依赖环境变量 `OSS_ACCESS_KEY_ID` 和 `OSS_ACCESS_KEY_SECRET`（在 `backend/uitls/oss.py` 中读取）。

## 架构说明

### 模块命名与常规约定相反（重点）

本项目的目录命名与常见 FastAPI 项目约定**相反**，且部分包名存在刻意的拼写错误 —— 代码中的导入都使用了这些确切路径，**不要随手"修正"拼写**，除非同时改遍所有导入：

- `backend/models/` = **Pydantic** 模型（请求/响应结构），如 `models/product.py`
- `backend/schemas/` = **SQLAlchemy ORM** 模型（数据库表），如 `schemas/product.py`。每个 schema 文件各自声明独立的 `declarative_base()`，各表之间没有共享的 Base/metadata。
- `dependenice/`（不是 "dependencies"）= FastAPI 校验依赖
- `uitls/`（不是 "utils"）= 工具函数（OSS 客户端、文件名生成、密码/JWT 安全）
- `middleware/` = JWT 中间件

### 请求流程与代码约定

- 所有路由位于 `backend/routers/`，在 `backend/main.py` 中注册，统一使用 `/admin/...` 前缀。面向用户的提示文案和路由 tags 均为中文。
- **统一响应结构**：所有接口返回 `models/common.py::BaseResponse`（`{code, message, data}`），通过 `BaseResponse.success()` / `BaseResponse.error()` 构造。`code=0` 表示成功；业务失败以 HTTP 200 + 非零 `code` 返回，而不是 HTTP 错误状态码。
- **校验依赖模式**：`dependenice/` 中的依赖要么返回解析后的请求模型，要么返回 `BaseResponse.error(...)`；路由中先判断 `if items.code: return items` 再继续。部分依赖（如 `check_product_id`）改为抛出 `HTTPException` —— 两种风格并存。
- **单条/列表兼容的入参**：新增/更新的请求模型中 `data` 类型为 `Union[X, List[X]]`；路由内用 `isinstance(...)` 分支做归一化处理。

### 认证（JWT）

- Token 的生成/校验在 `uitls/security.py`（python-jose，HS256）；配置（密钥、access 30 分钟 / refresh 7 天）在 `app_config/auth_config.py`。
- **`middleware/verify_token.py` 目前在函数开头直接 `return await call_next(request)`，等于所有路由的 JWT 校验被整体禁用**，其后的免校验路径列表实际是死代码。`dependenice/user.py::get_current_user` 虽然存在，但未挂到任何路由上 —— 不要默认接口有鉴权保护。
- 登录/刷新接口：`/admin/users/login`、`/admin/users/refresh_token`。

### 数据库

- MySQL 连接信息硬编码在 `backend/db/config.py`（localhost:3306，库 `rpj`，用户 `docker_mysql`，明文密码）；会话依赖为 `db/db.py::get_db`（按请求创建的 generator）。
- **没有迁移工具（无 Alembic）**。表结构早期通过 SQL 脚本在外部维护（见 git 历史），改表需手动在 MySQL 中执行。
- Redis 由 docker-compose 提供，但代码中没有任何地方引用它。

### 文件上传

上传场景（品牌 logo、企业 logo、产品附件）使用 `uitls/oss.py::AliyunOSS` —— 通过 `run_in_executor` 对同步 `oss2` SDK 的异步封装。OSS key 由 `uitls/handle_filename.py::generate_filename()` 生成，以路由 prefix 作为路径前缀 + UUID。`uitls/oss2.py` 是一个独立的 V4 签名参考脚本，没有被任何代码导入。

## 已知的未完成/有问题的地方

- `routers/product.py`、`routers/product_image.py`、`routers/product_attachments.py` 中的 `/update` 接口直接遍历外层包装模型（`for item in product:`），并对 ORM 对象列表调用 `.update()` —— 这段逻辑跑不通。这些接口属于未完成状态，写新接口时不要照抄该模式。
- `schemas/user.py::Users.hashed_password` 是 `String(20)`，存不下 bcrypt 哈希。
- 部分 Pydantic 模型用 `Form(...)` 作为字段默认值（如 `models/user.py`），它们只能通过 `Depends(...)` 或 `as_form` 类方法模式使用（见 `models/brand.py`、`models/company.py`），不能作为 JSON body 使用。
