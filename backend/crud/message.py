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
from backend.scheams import Result, Token, MessageStructure
from backend.models import Message
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis
from utils import resp_200, SetRedis, by_ip_get_address


class CRUDMessage(CRUDBase[Message, MessageStructure]):

    async def getQuery(self, db: AsyncSession, query_obj: dict, orderBy: str = None,
                       orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                       ) -> list:
        """ 根据查询条件获取 """
        result = None
        if any([query_obj["read_status"], query_obj["content_type"]]) and query_obj["read_status"] and query_obj[
            "content_type"] != "all":
            if orderType == "descending":
                sql = select(self.model).where(self.model.read_status.like('%' + query_obj["read_status"] + '%'),
                                               self.model.content.like('%' + query_obj["content_type"] + '%')) \
                    .offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.read_status.like('%' + query_obj["read_status"] + '%'),
                                               self.model.content.like('%' + query_obj["content_type"] + '%')) \
                    .offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"]) \
                    .offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"]) \
                    .offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model).offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        print(result)
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}


getMessage = CRUDMessage(Message)
