# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Annex
from backend.models import Attachment
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis

class CRUDAnnex(CRUDBase[Annex, Attachment]):

    async def getQuery(self, db: AsyncSession, query_obj: dict, orderBy: str = None,
                       orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                       ) -> list:
        """ 根据查询条件获取 """
        result = None
        if any([query_obj["origin_name"], query_obj["storage_mode"], query_obj["mime_type"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.origin_name.like('%' + query_obj["origin_name"] + '%'),
                                               self.model.storage_mode.like('%' + query_obj["storage_mode"] + '%'),
                                               self.model.mime_type.like('%' + query_obj["mime_type"] + '%'))\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.origin_name.like('%' + query_obj["origin_name"] + '%'),
                                               self.model.storage_mode.like('%' + query_obj["storage_mode"] + '%'),
                                               self.model.mime_type.like('%' + query_obj["mime_type"] + '%'))\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model).where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
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
        if any([query_obj["origin_name"], query_obj["storage_mode"], query_obj["mime_type"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.origin_name.like('%' + query_obj["origin_name"] + '%'),
                                               self.model.storage_mode.like('%' + query_obj["storage_mode"] + '%'),
                                               self.model.mime_type.like('%' + query_obj["mime_type"] + '%'))\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.origin_name.like('%' + query_obj["origin_name"] + '%'),
                                               self.model.storage_mode.like('%' + query_obj["storage_mode"] + '%'),
                                               self.model.mime_type.like('%' + query_obj["mime_type"] + '%'))\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"],
                                               self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model).where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}

    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        """ 修改列表排序 """
        sql = update(self.model).where(self.model.id == obj_in["id"]).values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount


getAnnex = CRUDAnnex(Attachment)