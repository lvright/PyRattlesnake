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
from backend.scheams import MenuStructure
from backend.models import SystemMenu, MenuRelation, RoleRelation
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis

class CRUDMenu(CRUDBase[SystemMenu, MenuStructure]):

    async def menuTree(self, db: AsyncSession) -> list:
        """ 获取树状部门结构数据 """
        sql = select(self.model)
        _menu = await db.scalars(sql)
        routers = jsonable_encoder(_menu.all())
        await db.close()
        if routers:
            result = []
            for item in routers:
                item = {"id": item["id"], "parent_id": item["parent_id"], "label": item["title"], "value":  item["id"]}
                item["children"] = [{
                    "id": menu["id"],
                    "parent_id": menu["parent_id"],
                    "label": menu["title"],
                    "value": menu["id"]}
                    for menu in routers if menu["parent_id"] == item["id"]]
                if item["parent_id"] == 0: result.append(item)
            return result

    async def getMenuByRole(self, db: AsyncSession, user_id: int) -> list:
        """ 获取用户权限理由 """
        sql = select(MenuRelation).where(user_id == MenuRelation.role_id)
        _menus = await db.scalars(sql)
        result = jsonable_encoder(_menus.all())
        await db.close()  # 释放会话
        return result

    async def userMenu(self, db: AsyncSession, user_id: int) -> list:
        """ 根据用户ID查询关联部门 """
        sql = select(MenuRelation).where(MenuRelation.user_id == user_id)
        relation_data = await db.scalars(sql)
        _relation = jsonable_encoder(relation_data.first())
        sql = select(self.model).where(self.model.id == _relation["menu_id"])
        _ids = await db.scalars(sql)
        result = jsonable_encoder(_ids.all())
        return result

    async def createRelation(self, db: AsyncSession, obj_in: dict) -> dict:
        """ 创建部门关联用户数据 """
        sql = insert(MenuRelation).values(obj_in)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def removeRelation(self, db: AsyncSession, user_id: int) -> int:
        """ 删除用户关联表 """
        sql = delete(MenuRelation).where(DeptRelation.user_id == user_id)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def getQuery(self, db: AsyncSession, query_obj: dict, orderBy: str = None,
                       orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                       ) -> list:
        """ 根据查询条件获取 """
        result = None
        if any([query_obj["name"], query_obj["code"], query_obj["hidden"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.name.like('%' + query_obj["name"] + '%'), self.model.leader.like('%' + query_obj["code"] + '%'),
                                               self.model.phone.like('%' + query_obj["hidden"] + '%'))\
                    .where(self.model.delete != "1").order_by(desc(orderBy))
            else:
                sql = select(self.model).where(self.model.name.like('%' + query_obj["name"] + '%'), self.model.leader.like('%' + query_obj["code"] + '%'),
                                               self.model.phone.like('%' + query_obj["hidden"] + '%'))\
                    .where(self.model.delete != "1").order_by(orderBy)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"] + '%')\
                    .where(self.model.delete != "1").order_by(desc(orderBy))
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"] + '%')\
                    .where(self.model.delete != "1").order_by(orderBy)
        elif query_obj["status"]:
            if orderType == "descending":
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete != "1").order_by(desc(orderBy))
            else:
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete != "1").order_by(orderBy)
        else:
            sql = select(self.model).where(self.model.delete != "1").order_by(orderBy)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        routers = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        if routers:
            result = []
            for item in routers:
                item["children"] = [menu for menu in routers if menu["parent_id"] == item["id"]]
                if item["parent_id"] == 0: result.append(item)
        return {"data": result or [], "total": total, "page_total": page_total(total, pageSize)}

    async def getQueryReclcle(self, db: AsyncSession, query_obj: dict, orderBy: str = None,
                              orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                              ) -> list:
        """ 根据查询条件获取 """
        result = None
        if any([query_obj["name"], query_obj["code"], query_obj["hidden"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.name.like('%' + query_obj["name"] + '%'), self.model.code.like('%' + query_obj["code"] + '%'),
                                               self.model.hidden.like('%' + query_obj["hidden"] + '%'))\
                    .where(self.model.delete == "1").order_by(desc(orderBy))
            else:
                sql = select(self.model).where(self.model.name.like('%' + query_obj["name"] + '%'), self.model.code.like('%' + query_obj["code"] + '%'),
                                               self.model.hidden.like('%' + query_obj["hidden"] + '%'))\
                    .where(self.model.delete == "1").order_by(orderBy)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete == "1").order_by(desc(orderBy))
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete == "1").order_by(orderBy)
        elif query_obj["status"]:
            if orderType == "descending":
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete == "1").order_by(desc(orderBy))
            else:
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete == "1").order_by(orderBy)
        else:
            sql = select(self.model).where(self.model.delete == "1").order_by(orderBy)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        routers = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        if routers:
            result = []
            for item in routers:
                item["children"] = [menu for menu in routers if menu["parent_id"] == item["id"]]
                if item["parent_id"] == 0: result.append(item)
        return {"data": result or [], "total": total, "page_total": page_total(total, pageSize)}

    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        """ 修改列表排序 """
        sql = update(self.model).where(self.model.id == obj_in["id"]).values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

getMenu = CRUDMenu(SystemMenu)