# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import page_total
from backend.crud import CRUDBase
from backend.models import Message
from backend.scheams import MessageStructure


class CRUDMessage(CRUDBase[Message, MessageStructure]):

    async def getQuery(
            self, db: AsyncSession,
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

        if any([queryObj["read_status"], queryObj["content_type"]]) \
                and queryObj["read_status"] and queryObj["content_type"] != "all":
            sql = baseSQL.where(self.model.read_status.like('%' + queryObj["read_status"] + '%'),
                                self.model.content.like('%' + queryObj["content_type"] + '%'))
        elif any([queryObj["minDate"], queryObj["maxDate"]]):
            sql = baseSQL.where(self.model.created_at >= queryObj["minDate"],
                                self.model.created_at <= queryObj["maxDate"])
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


getMessage = CRUDMessage(Message)
