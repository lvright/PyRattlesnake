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
from backend.scheams import Dept
from backend.models import UserDept, DeptRelation
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis

class SystemDept(CRUDBase[UserDept, Dept]):

    async def deptTree(self, db: AsyncSession) -> list:
        """ 获取树状部门结构数据 """
        fields = [self.model.id, self.model.name.label("label"), self.model.parent_id, self.model.id.label("value")]
        sql = select(*fields)
        dept_data = await db.execute(sql)
        dept_list = jsonable_encoder(dept_data.all())
        if dept_list:
            result = []
            for item in dept_list:
                item["children"] = [dept for dept in dept_list if dept["parent_id"] == item["id"]]
                if item["parent_id"] == 0: result.append(item)
            return result

    async def userDept(self, db: AsyncSession, user_id: int) -> list:
        """ 根据用户ID查询关联部门 """
        sql = select(DeptRelation).where(DeptRelation.user_id == user_id)
        relation_data = await db.scalars(sql)
        _relation = jsonable_encoder(relation_data.first())
        sql = select(self.model).where(self.model.id == _relation["dept_id"])
        ids_data = await db.scalars(sql)
        result = jsonable_encoder(ids_data.all())
        return result

    async def createRelation(self, db: AsyncSession, obj_in: dict) -> dict:
        """ 创建部门关联用户数据 """
        sql = insert(DeptRelation).values(obj_in)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def removeRelation(self, db: AsyncSession, user_id: int) -> int:
        """ 删除用户关联表 """
        sql = delete(DeptRelation).where(DeptRelation.user_id == user_id)
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
    ):
        """ 根据查询条件获取部门 """
        result = None
        if any([query_obj["name"], query_obj["leader"], query_obj["phone"]]):
            if orderType == "descending":
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.leader.like('%' + query_obj["leader"]),
                           self.model.phone.like('%' + query_obj["phone"] + '%')) \
                    .where(self.model.delete != "1") \
                    .offset((pageIndex - 1) * pageSize) \
                    .order_by(desc(orderBy)) \
                    .limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.leader.like('%' + query_obj["leader"]),
                           self.model.phone.like('%' + query_obj["phone"] + '%')) \
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
    ):
        """ 根据查询条件获取部门 """
        result = None
        if any([query_obj["name"], query_obj["leader"], query_obj["phone"]]):
            if orderType == "descending":
                sql = select(self.model).where(
                    self.model.name.like('%' + query_obj["name"] + '%'),
                    self.model.leader.like('%' + query_obj["leader"]),
                    self.model.phone.like('%' + query_obj["phone"] + '%')
                ).where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.name.like('%' + query_obj["name"] + '%'),
                           self.model.leader.like('%' + query_obj["leader"]),
                           self.model.phone.like('%' + query_obj["phone"] + '%')) \
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

getDept = SystemDept(UserDept)