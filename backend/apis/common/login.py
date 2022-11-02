# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders

from utils import resp_200, resp_400, resp_500, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user
from backend.core import verify_password, get_password_hash
from backend.crud import toLogin
from backend.scheams import Token, Result
from backend.db import MyRedis

router = APIRouter()


@router.post(
    path='/system/login',
    response_model=Result,
    summary="后台登录"
)
async def login_access_token(
        request: Request,
        db: AsyncSession = Depends(get_db),
        from_data: OAuth2PasswordRequestForm = Depends()
):
    passwords_match = verify_password(from_data.password, get_password_hash(from_data.password))
    if passwords_match:
        token = await toLogin.go(
            db, request, form_data={"username": from_data.username, "password": from_data.password}
        )
        if token:
            return resp_200(data=token, msg="登录成功")
        return resp_200(msg="账户或密码错误")
    return ErrorUser()


@router.post(
    path="/system/logout",
    response_model=Result,
    summary="退出登录"
)
async def logout_token(
        request: Request, db: AsyncSession = Depends(get_db),
        redis: MyRedis = Depends(get_redis)
):
    await toLogin.out(db, request, redis)
    return resp_200(msg="已退出登录")
