# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import page_total
from backend.core import get_password_hash, verify_password
from backend.crud import CRUDBase
from backend.models import Admin, MenuRelation, SystemMenu, RoleRelation, DeptRelation, Setting
from backend.scheams import Account


class CRUBAdmin(CRUDBase[Admin, Account]):

    async def info(self, db: AsyncSession, user: dict) -> dict:
        """ 获取用户详情 """
        sql = select(self.model).where(self.model.id == user["id"]).where(self.model.status == "1")
        _user = await db.scalars(sql)
        result = jsonable_encoder(_user.first())
        await db.close()  # 释放会话
        return result

    async def routers(self, db: AsyncSession, user: dict) -> list:
        """ 获取用户权限理由 """
        fields = [
            SystemMenu.id,
            SystemMenu.title,
            SystemMenu.type,
            SystemMenu.hidden,
            SystemMenu.parent_id,
            SystemMenu.redirect,
            SystemMenu.path,
            SystemMenu.icon,
            SystemMenu.component,
            SystemMenu.status,
            SystemMenu.name
        ]
        sql = select(*fields).where(SystemMenu.status == "1", SystemMenu.hidden == "0")\
            .where(SystemMenu.id == MenuRelation.menu_id, MenuRelation.role_id == RoleRelation.role_id)\
            .where(user['id'] == RoleRelation.user_id)
        _menus = await db.execute(sql)
        routers = jsonable_encoder(_menus.all())

        # 路由结构处理
        if routers:
            menus = []
            codes = []
            for item in routers:
                if user["username"] == "superAdmin": codes = ["*"] or codes.append(item["title"])
                item.setdefault("meta", {
                    "icon": item["icon"],
                    "title": item["title"],
                    "type": item["type"],
                    "hidden": bool(int(item["hidden"]))
                })
                for key in ["hidden", "icon", "title", "type"]: item.pop(key)
                item.setdefault("children", [menu for menu in routers if menu["parent_id"] == item["id"]])
                if item["parent_id"] == 0: menus.append(item)
            result = {"codes": codes, "menus": menus}
            await db.close()  # 释放会话
            return result

    async def setting(self, db: AsyncSession, user: dict) -> dict:
        """ 根据用户ID获取用户系统设置 """
        sql = select(Setting).where(user["id"] == Setting.user_id)
        _setting = await db.scalars(sql)
        result = jsonable_encoder(_setting.first())
        await db.close()  # 释放会话
        return result

    async def updatePassword(self, db: AsyncSession, password: dict, user: dict) -> int:
        """ 更改用户密码 """
        password_match = verify_password(password["oldPassword"], user["password"])
        if password_match:
            if password["newPassword"] == password["newPassword_confirmation"]:
                sql = update(self.model).where(self.model.id == user["id"]).values(
                    password=get_password_hash(password['newPassword']))
                result = await db.execute(sql)
                await db.commit()
                await db.close()  # 释放会话
                return result.rowcount
        return password_match

    async def updateSetting(self, db: AsyncSession, obj_in: dict, user_id: int) -> int:
        """ 更新用户系统设置 """
        obj_in['layoutTags'] = str(int(obj_in['layoutTags']))
        sql = update(Setting).where(Setting.user_id == user_id).values(**obj_in)
        result = await db.execute(sql)
        await db.commit()
        await db.close()  # 释放会话
        return result.rowcount

    async def getQuery(
            self, db: AsyncSession,
            queryObj: dict,
            deptId: int,
            orderBy: str = None,
            orderType: str = "ascending",
            pageIndex: int = 1,
            pageSize: int = 10,
            delete: str = "1"
    ) -> list:
        """ 根据查询条件获取用户 """

        baseSQL = select(self.model).where(self.model.delete == delete)

        if any([queryObj["username"], queryObj["nickname"], queryObj["phone"], queryObj["email"]]):
            sql = baseSQL.where(self.model.username.like('%' + queryObj["username"] + '%'),
                                self.model.nickname.like('%' + queryObj["nickname"] + '%'),
                                self.model.phone.like('%' + queryObj["phone"] + '%'),
                                self.model.email.like('%' + queryObj["email"] + '%'))
        elif any([queryObj["minDate"], queryObj["maxDate"]]):
            sql = baseSQL.where(self.model.created_at >= queryObj["minDate"],
                                self.model.created_at <= queryObj["maxDate"])
        elif deptId: sql = baseSQL.where(DeptRelation.dept_id == deptId, self.model.id == DeptRelation.user_id)
        elif queryObj["status"]: sql = baseSQL.where(self.model.status == str(queryObj["status"]))
        else: sql = baseSQL.offset((pageIndex - 1) * pageSize)

        if orderType == "descending": sql = sql.order_by(desc(orderBy)).limit(pageSize)
        else: sql = sql.order_by(orderBy).limit(pageSize)

        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {
            "items": result, "pageInfo": {
                "total": total, "currentPage": pageIndex, "totalPage": page_total(total, pageSize)
            }
        }


getUser = CRUBAdmin(Admin)
