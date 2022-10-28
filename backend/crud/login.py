# -*- coding: utf-8 -*-

import json
from datetime import timedelta

from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_redis
from backend.core import setting, create_access_token
from backend.crud import CRUDBase
from backend.db import MyRedis
from backend.models import Admin, LoginLog
from backend.scheams import Account
from utils import SetRedis, by_ip_get_address, logger


class CRUBLogin(CRUDBase[Admin, Account]):

    async def go(self, db: AsyncSession, request: Request, form_data: dict) -> dict:
        sql = select(self.model).where(
            self.model.username == form_data['username'],
            self.model.password == form_data['password']
        )
        _user = await db.scalars(sql)
        user_info = jsonable_encoder(_user.first())
        if user_info:
            access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_access_token(user_info, access_token_expires)
            set_ipconfig = update(self.model)\
                .where(self.model.id == user_info['id'])\
                .values(login_ip=request.client.host)
            set_login_log = insert(LoginLog).values({
                "username": user_info["username"],
                "ip": request.client.host,
                "ip_location": by_ip_get_address(request.client.host)
            })
            await db.execute(set_login_log)
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
