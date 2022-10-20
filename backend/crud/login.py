# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, celery
from backend.scheams import Result, Token, Account, Login, AccountUpdate
from backend.models import Admin
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis
from utils import resp_200, SetRedis, by_ip_get_address


class CRUBLogin(CRUDBase[Admin, Account]):

    async def go(self, db: AsyncSession, request: Request, form_data: dict) -> dict:
        sql = select(self.model).where(self.model.username == form_data['username'],
                                       self.model.password == form_data['password'])
        _user = await db.scalars(sql)
        user_info = jsonable_encoder(_user.first())
        if user_info:
            access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_access_token(user_info, access_token_expires)
            set_ipconfig = update(self.model).where(self.model.id == user_info['id']).values(
                login_ip=request.client.host)
            await db.execute(set_ipconfig)
            await db.commit()
            try:
                await request.app.state.redis.incr('visit_num')  # 用户访问量 自增1
                await request.app.state.redis.set(token, json.dumps(user_info), access_token_expires)
            except Exception as e:
                raise SetRedis(f"Redis存储 token 失败！-- {e}")
            return {"token": token}

    async def out(self, db: AsyncSession, request: Request, redis: MyRedis = Depends(get_redis)) -> bool:
        if 'authorization' in request.headers.keys():
            token = request.headers.get('authorization')[7:]  # 去除token前面的 Bearer
            await redis.delete(token)


toLogin = CRUBLogin(Admin)
