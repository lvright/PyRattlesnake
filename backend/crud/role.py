# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Role
from backend.models import Role, RoleRelation
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis

class SystemRole(CRUDBase[Role, Role]):

    async def userRole(self, db: AsyncSession, user_id: int) -> list:
        """ 根据用户ID获取关联角色 """
        sql = select(RoleRelation).where(RoleRelation.user_id == user_id)
        relation_data = await db.scalars(sql)
        _relation = jsonable_encoder(relation_data.all())
        result = []
        if _relation:
            for dept_id in [item['role_id'] for item in _relation]:
                sql = select(self.model).where(self.model.id == dept_id)
                ids_data = await db.scalars(sql)
                for id in jsonable_encoder(ids_data.all()): result.append(id)
        return result

    async def createRelation(self, db: AsyncSession, obj_in: dict) -> dict:
        """ 创建岗位关联用户数据 """
        sql = insert(RoleRelation).values(obj_in)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def removeRelation(self, db: AsyncSession, user_id: int) -> int:
        """ 删除用户关联表 """
        sql = delete(RoleRelation).where(RoleRelation.user_id == user_id)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def getQuery(
        self, db: AsyncSession,
        query_obj: dict,
        orderBy: str = None,
        orderType: str = "ascending",
        pageIndex: int = 1,
        pageSize: int = 10
    ) -> list:
        """ 按条件查询 """
        if any([query_obj["name"], query_obj["code"]]):
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.code.like('%' + query_obj["code"])) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)) \
                    .limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.code.like('%' + query_obj["code"])) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(orderBy) \
                    .limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.created_at >= query_obj["minDate"],
                           self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.created_at >= query_obj["minDate"],
                           self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(orderBy).limit(pageSize)
        elif query_obj["status"]:
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.status == str(query_obj["status"])) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.status == str(query_obj["status"])) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model) \
                .where(self.model.delete != "1") \
                .offset((pageIndex - 1) * pageSize) \
                .order_by(orderBy).limit(pageSize)

        data = await db.scalars(sql)
        result = jsonable_encoder(data.all())
        await db.close()  # 释放会话
        return result

    async def getQueryReclcle(
        self, db: AsyncSession,
        query_obj: dict,
        orderBy: str = None,
        orderType: str = "ascending",
        pageIndex: int = 1,
        pageSize: int = 10
    ) -> list:
        """ 按条件查询逻辑删除数据 """
        if any([query_obj["name"], query_obj["code"]]):
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.code.like('%' + query_obj["code"])) \
                    .where(self.model.delete == "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)) \
                    .limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.code.like('%' + query_obj["code"])) \
                    .where(self.model.delete == "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(orderBy) \
                    .limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.created_at >= query_obj["minDate"],
                           self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete == "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.created_at >= query_obj["minDate"],
                           self.model.created_at <= query_obj["maxDate"]) \
                    .where(self.model.delete == "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(orderBy).limit(pageSize)
        elif query_obj["status"]:
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.status == str(query_obj["status"])) \
                    .where(self.model.delete == "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.status == str(query_obj["status"])) \
                    .where(self.model.delete == "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model) \
                .where(self.model.delete == "1") \
                .offset((pageIndex - 1) * pageSize) \
                .order_by(orderBy).limit(pageSize)

        data = await db.scalars(sql)
        result = jsonable_encoder(data.all())
        await db.close()  # 释放会话
        return result

    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        sql = update(self.model).where(self.model.id == obj_in["id"]).values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

getRole = SystemRole(Role)