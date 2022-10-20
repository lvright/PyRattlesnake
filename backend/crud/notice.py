# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, desc
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, celery
from backend.scheams import Result, Token, SystemNotification
from backend.models import Notification
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis
from utils import resp_200, SetRedis, by_ip_get_address


class CURDNotification(CRUDBase[Notification, SystemNotification]):

    async def getQuery(self, db: AsyncSession, query_obj: dict, orderBy: str = None,
                       orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                       ) -> list:
        """ 根据查询条件获取 """
        result = None
        if any([query_obj["title"], query_obj["type"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.title.like('%' + query_obj["title"] + '%'),
                                               self.model.type.like('%' + query_obj["type"] + '%')) \
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(
                    pageSize)
            else:
                sql = select(self.model).where(self.model.title.like('%' + query_obj["title"] + '%'),
                                               self.model.type.like('%' + query_obj["type"] + '%')) \
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(
                    pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(
                    pageSize)
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(
                    pageSize)
        else:
            sql = select(self.model).where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(
                orderBy).limit(pageSize)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}

    async def getQueryReclcle(self, db: AsyncSession, query_obj: dict, orderBy: str = None,
                              orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                              ) -> list:
        """ 根据查询条件获取 """
        result = None
        if any([query_obj["title"], query_obj["type"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.title.like('%' + query_obj["title"] + '%'),
                                               self.model.type.like('%' + query_obj["type"] + '%')) \
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(
                    pageSize)
            else:
                sql = select(self.model).where(self.model.title.like('%' + query_obj["title"] + '%'),
                                               self.model.type.like('%' + query_obj["type"] + '%')) \
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(
                    pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(
                    pageSize)
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(
                    pageSize)
        else:
            sql = select(self.model).where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(
                orderBy).limit(pageSize)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}


getNotification = CURDNotification(Notification)
