# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import page_total
from backend.crud import CRUDBase
from backend.models import Dept, DeptRelation
from backend.scheams import DeptStructure


class CRUDDept(CRUDBase[Dept, DeptStructure]):

    async def deptTree(self, db: AsyncSession) -> list:
        """ 获取树状部门结构数据 """
        sql = select(*[self.model.id, self.model.name.label("label"),
                       self.model.parent_id, self.model.id.label("value")])
        _dept = await db.execute(sql)
        dept_list = jsonable_encoder(_dept.all())
        if dept_list:
            result = []
            for item in dept_list:
                item.setdefault("children", [dept for dept in dept_list if dept["parent_id"] == item["id"]])
                if item["parent_id"] == 0: result.append(item)
            return result

    async def userDept(self, db: AsyncSession, user_id: int) -> list:
        """ 根据用户ID查询关联部门 """
        sql = select(DeptRelation).where(DeptRelation.user_id == user_id)
        _relation = await db.scalars(sql)
        relation = jsonable_encoder(_relation.first())
        sql = select(self.model).where(self.model.id == relation["dept_id"])
        _ids = await db.scalars(sql)
        result = jsonable_encoder(_ids.all())
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
            queryObj: dict,
            orderBy: str = None,
            orderType: str = "ascending",
            pageIndex: int = 1,
            pageSize: int = 10,
            delete: str = "0"
    ) -> list:
        """ 根据查询条件获取部门 """

        result = None

        baseSQL = select(self.model).where(self.model.delete == delete)

        if any([queryObj["name"], queryObj["leader"], queryObj["phone"]]):
            sql = baseSQL.where(self.model.name.like('%' + queryObj["name"] + '%'),
                                self.model.leader.like('%' + queryObj["leader"] + '%'),
                                self.model.phone.like('%' + queryObj["phone"] + '%'))
        elif any([queryObj["minDate"], queryObj["maxDate"]]):
            sql = baseSQL.where(self.model.created_at >= queryObj["minDate"],
                                self.model.created_at <= queryObj["maxDate"])
        elif queryObj["status"]:
            sql = baseSQL.where(self.model.status == str(queryObj["status"]))
        else:
            sql = baseSQL.offset((pageIndex - 1) * pageSize)

        if orderType == "descending":
            sql = sql.order_by(desc(orderBy)).limit(pageSize)
        else:
            sql = sql.order_by(orderBy).limit(pageSize)

        _query = await db.scalars(sql)
        total = await self.get_number(db)
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": total, "page_total": page_total(total, pageSize)}

    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        """ 修改列表排序 """
        sql = update(self.model)\
            .where(self.model.id == obj_in["id"])\
            .values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount


getDept = CRUDDept(Dept)
