# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, and_, desc
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Result, Token, Account, Login, AccountUpdate, ModifyPassword
from backend.models import Admin, MenuRelation, SystemMenu, Role, Dept, RoleRelation, DeptRelation, Setting, PostRelation
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis


class CRUBAdmin(CRUDBase[Admin, Account]):

    async def getUserInfo(self, db: AsyncSession, user: dict) -> dict:
        """ 获取用户详情 """
        sql = select(self.model).where(self.model.id == user["id"]).where(self.model.status == "1")
        _user = await db.scalars(sql)
        result = jsonable_encoder(_user.first())
        await db.close()  # 释放会话
        return result

    async def getUserRouters(self, db: AsyncSession, user: dict) -> list:
        """ 获取用户权限理由 """
        fields = [SystemMenu.id, SystemMenu.title, SystemMenu.type, SystemMenu.hidden, SystemMenu.parent_id,
                  SystemMenu.redirect, SystemMenu.path, SystemMenu.icon, SystemMenu.component, SystemMenu.status, SystemMenu.name]
        sql = select(*fields).where(SystemMenu.status == "1", SystemMenu.hidden == "0")\
            .where(SystemMenu.id == MenuRelation.menu_id, MenuRelation.role_id == RoleRelation.role_id).where(user['id'] == RoleRelation.user_id)
        _menus = await db.execute(sql)
        routers = jsonable_encoder(_menus.all())

        # 路由结构处理
        if routers:
            menus = []
            codes = []
            for item in routers:
                if user["username"] == "superAdmin": codes = ["*"] or codes.append(item["title"])
                item["meta"] = {"icon": item["icon"], "title": item["title"], "type": item["type"], "hidden": bool(int(item["hidden"]))}
                del item["hidden"], item["icon"], item["title"], item["type"]
                item["children"] = [menu for menu in routers if menu["parent_id"] == item["id"]]
                if item["parent_id"] == 0: menus.append(item)
            result = {"codes": codes, "menus": menus}
            await db.close()  # 释放会话
            return result

    async def getUserSetting(self, db: AsyncSession, user: dict) -> dict:
        """ 根据用户ID获取用户系统设置 """
        sql = select(Setting).where(user["id"] == Setting.user_id)
        _setting = await db.scalars(sql)
        result = jsonable_encoder(_setting.first())
        await db.close()  # 释放会话
        return result

    async def updatePassword(self, db: AsyncSession, paw: dict, user_id: int) -> int:
        """ 更改用户密码 """
        if paw["newPassword"] == paw["newPassword_confirmation"]:
            sql = update(self.model).where(self.model.id == user_id).where(self.model.password == paw["oldPassword"]).values(password=paw['newPassword'])
            result = await db.execute(sql)
            await db.commit()
            await db.close()  # 释放会话
            return result.rowcount

    async def updateSetting(self, db: AsyncSession, obj_in: dict, user_id: int) -> int:
        """ 更新用户系统设置 """
        obj_in['layoutTags'] = str(int(obj_in['layoutTags']))
        sql = update(Setting).where(Setting.user_id == user_id).values(**obj_in)
        result = await db.execute(sql)
        await db.commit()
        await db.close()  # 释放会话
        return result.rowcount

    async def getQuery(self, db: AsyncSession, query_obj: dict, dept_id: int, orderBy: str = None,
                       orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                       ) -> list:
        """ 根据查询条件获取用户 """
        result = None
        if any([query_obj["username"], query_obj["nickname"], query_obj["phone"], query_obj["email"]]):
            if orderType == "descending":
                sql = select(self.model)\
                    .where(self.model.username.like('%' + query_obj["username"] + '%'), self.model.nickname.like('%' + query_obj["nickname"] + '%'),
                           self.model.phone.like('%' + query_obj["phone"] + '%'), self.model.email.like('%' + query_obj["email"] + '%'))\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model)\
                    .where(self.model.username.like('%' + query_obj["username"] + '%'), self.model.nickname.like('%' + query_obj["nickname"] + '%'),
                           self.model.phone.like('%' + query_obj["phone"] + '%'), self.model.email.like('%' + query_obj["email"] + '%'))\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif dept_id:
            if orderType == "descending":
                sql = select(self.model).where(DeptRelation.dept_id == dept_id, self.model.id == DeptRelation.user_id)\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(DeptRelation.dept_id == dept_id, self.model.id == DeptRelation.user_id)\
                    .where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif query_obj["status"]:
            if orderType == "descending":
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete != "1")\
                    .offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete != "1")\
                    .offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model).where(self.model.delete != "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}

    async def getQueryReclcle(self, db: AsyncSession, query_obj: dict, dept_id: int, orderBy: str = None,
                              orderType: str = "ascending", pageIndex: int = 1, pageSize: int = 10
                              ) -> list:
        """ 根据查询条件获取用户 """
        result = None
        if any([query_obj["username"], query_obj["nickname"], query_obj["phone"], query_obj["email"]]):
            if orderType == "descending":
                sql = select(self.model)\
                    .where(self.model.username.like('%' + query_obj["username"] + '%'), self.model.nickname.like('%' + query_obj["nickname"] + '%'),
                           self.model.phone.like('%' + query_obj["phone"] + '%'), self.model.email.like('%' + query_obj["email"] + '%'))\
                    .where(self.model.delete == "1") .offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model)\
                    .where(self.model.username.like('%' + query_obj["username"] + '%'), self.model.nickname.like('%' + query_obj["nickname"] + '%'),
                           self.model.phone.like('%' + query_obj["phone"] + '%'), self.model.email.like('%' + query_obj["email"] + '%'))\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif any([query_obj["minDate"], query_obj["maxDate"]]):
            if orderType == "descending":
                sql = select(self.model)\
                    .where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model) \
                    .where(self.model.created_at >= query_obj["minDate"], self.model.created_at <= query_obj["maxDate"])\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif dept_id:
            if orderType == "descending":
                sql = select(self.model).where(DeptRelation.dept_id == dept_id, self.model.id == DeptRelation.user_id)\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(DeptRelation.dept_id == dept_id, self.model.id == DeptRelation.user_id)\
                    .where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        elif query_obj["status"]:
            if orderType == "descending":
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete == "1")\
                    .offset((pageIndex - 1) * pageSize).order_by(desc(orderBy)).limit(pageSize)
            else:
                sql = select(self.model).where(self.model.status == str(query_obj["status"])).where(self.model.delete == "1")\
                    .offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        else:
            sql = select(self.model).where(self.model.delete == "1").offset((pageIndex - 1) * pageSize).order_by(orderBy).limit(pageSize)
        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}


getUser = CRUBAdmin(Admin)