# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import page_total
from backend.crud import CRUDBase
from backend.models import SystemMenu, MenuRelation
from backend.scheams import MenuStructure


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
                item = {
                    "id": item["id"],
                    "parent_id": item["parent_id"],
                    "label": item["title"],
                    "value": item["id"]
                }
                item.setdefault("children", [
                    {
                        "id": menu["id"],
                        "parent_id": menu["parent_id"],
                        "label": menu["title"],
                        "value": menu["id"]
                    }
                    for menu in routers
                    if menu["parent_id"] == item["id"]
                ])
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

    async def getQuery(
            self,
            db: AsyncSession,
            queryObj: dict,
            orderBy: str = None,
            orderType: str = "ascending",
            pageIndex: int = 1,
            pageSize: int = 10,
            delete: str = "0"
    ) -> list:
        """ 根据查询条件获取 """

        baseSQL = select(self.model).where(self.model.delete == delete)

        if any([queryObj["name"], queryObj["title"], queryObj["hidden"]]):
            sql = baseSQL.where(self.model.name.like('%' + queryObj["name"] + '%'),
                                self.model.title.like('%' + queryObj["title"] + '%'))
        elif any([queryObj["minDate"], queryObj["maxDate"]]):
            sql = baseSQL.where(self.model.created_at >= queryObj["minDate"],
                                self.model.created_at <= queryObj["maxDate"])
        elif queryObj["hidden"]: sql = baseSQL.where(self.model.hidden == queryObj["hidden"])
        elif queryObj["status"]: sql = baseSQL.where(self.model.status == str(queryObj["status"]))
        else: sql = baseSQL.offset((pageIndex - 1) * pageSize)

        if orderType == "descending": sql = sql.order_by(desc(orderBy))
        else: sql = sql.order_by(orderBy)

        _query = await db.scalars(sql)
        total = await self.get_number(db)
        routers = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        result = []
        if routers:
            for item in routers:
                item.setdefault("children", [menu for menu in routers if menu["parent_id"] == item["id"]])
                if item["parent_id"] == 0: result.append(item)
            return {
                "items": result, "pageInfo": {
                    "total": total, "currentPage": pageIndex, "totalPage": page_total(total, pageSize)
                }
            }
        return result


    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        """ 修改列表排序 """
        sql = update(self.model).where(self.model.id == obj_in["id"]).values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount


getMenu = CRUDMenu(SystemMenu)
