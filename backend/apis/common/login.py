# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders

from utils import resp_200, resp_400, resp_500, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user
from backend.crud import toLogin
from backend.scheams import Token, Result
from backend.db import MyRedis

router = APIRouter()

@router.post(path='/system/login', summary='后台登录')
async def login_access_token(request: Request, db: AsyncSession = Depends(get_db), from_data: OAuth2PasswordRequestForm = Depends()):
    token = await toLogin.go(db, request=request, form_data={"username": from_data.username, "password": from_data.password})
    if token: return resp_200(data=token, msg="登录成功")
    return ErrorUser()

@router.post("/logout", response_model=Result, summary="退出登录")
async def logout_token(request: Request, redis: MyRedis = Depends(get_redis)):
    if await toLogin.out(request=request, redis=redis): return resp_200(msg="已退出登录")
