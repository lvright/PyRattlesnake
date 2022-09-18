# -*- coding: utf-8 -*-

from typing import AsyncGenerator
from fastapi import Depends, Security, HTTPException
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
import math

from backend.core import check_jwt_token, setting
from backend.db import async_session, MyRedis
from backend.scheams import TokenData, Account
from utils import UserNotExist, PermissionNotEnough
from utils.permission_assign import handle_oauth2_scopes  # by_scopes_get_crud

get_token = OAuth2PasswordBearer(tokenUrl=f"{setting.API_PREFIX}/login", scopes=handle_oauth2_scopes())

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """ sql连接会话 """
    async with async_session() as session:
        yield session

async def get_redis(request: Request) -> MyRedis:
    """ redis连接对象 """
    return await request.app.state.redis

async def get_current_user(
        security_scopes: SecurityScopes,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(get_token)
):
    """ 得到当前用户(docs接口文档) """
    payload = await check_jwt_token(token)  # 检验token是否过期
    token_scopes = payload.get("scopes", [])  # 得不到值,返回[]
    token_data = TokenData(scopes=token_scopes, sub=payload.get("sub"))  # token存储的用户权限
    crud_obj = by_scopes_get_crud(token_scopes)  # 验证用户是否存在
    user = await crud_obj.get(db, id=payload.get("sub"))
    if not user:
        raise UserNotExist()
    for scope in security_scopes.scopes:  # 勾选的用户权限
        if scope not in token_data.scopes:
            raise PermissionNotEnough('权限不足,拒绝访问')
    return user

def get_current_active_user(current_user: Account = Security(get_current_user, scopes=["admin"])):
    """ 得到当前登录用户 """
    if not admin.is_active_def(current_user):
        raise HTTPException(status_code=400, detail="用户未登录！！！")
    return current_user

def page_total(page: int, size: int):
    """ 分页计算总页数 """
    return math.ceil(page / size)
