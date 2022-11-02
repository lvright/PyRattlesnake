# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import page_total
from backend.crud import CRUDBase
from backend.models import Dict, DictType
from backend.scheams import DictDate, DictClassify


class CRUDDictData(CRUDBase[Dict, DictDate]):

    async def getByCode(self, db: AsyncSession, code: str) -> list:
        """ 根据字典类型code获取数据字典 """
        sql = select(self.model).where(self.model.code == code)
        _dict = await db.scalars(sql)
        result = jsonable_encoder(_dict.all())
        result = [{"id": res["id"], "key": res["value"], "title": res["label"]} for res in result]
        return result

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

        result = None

        baseSQL = select(self.model).where(self.model.delete == delete)

        if any([queryObj["name"], queryObj["code"]]):
            sql = baseSQL.where(self.model.name.like('%' + queryObj["name"] + '%'),
                                self.model.code.like('%' + queryObj["code"]))
        elif queryObj["type_id"]:
            sql = baseSQL.where(self.model.type_id == queryObj["type_id"])
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
        result = jsonable_encoder(_query.all())
        await db.close()  # 释放会话
        return {"data": result, "total": len(result), "page_total": page_total(len(result), pageSize)}

    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        """ 修改列表排序 """
        sql = update(self.model).where(self.model.id == obj_in["id"]).values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount


class CRUDDictType(CRUDBase[DictType, DictClassify]):

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

        if any([queryObj["name"], queryObj["code"]]):
            sql = baseSQL.where(self.model.name.like('%' + queryObj["name"] + '%'),
                                self.model.code.like('%' + queryObj["code"]))
        elif any([queryObj["minDate"], queryObj["maxDate"]]):
            sql = baseSQL.where(self.model.created_at >= queryObj["minDate"],
                                self.model.created_at <= queryObj["maxDate"])
        elif queryObj["status"]: sql = baseSQL.where(self.model.status == str(queryObj["status"]))
        else: sql = baseSQL.offset((pageIndex - 1) * pageSize)

        if orderType == "descending": sql = sql.order_by(desc(orderBy)).limit(pageSize)
        else: sql = sql.order_by(orderBy).limit(pageSize)

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


getDictType = CRUDDictType(DictType)

getDictData = CRUDDictData(Dict)
