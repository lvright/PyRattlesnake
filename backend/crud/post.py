# -*- coding: utf-8 -*-

from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import page_total
from backend.crud import CRUDBase
from backend.models import Post, PostRelation
from backend.scheams import PostStructure


class CRUDPost(CRUDBase[Post, PostStructure]):

    async def userPost(self, db: AsyncSession, user_id: int) -> list:
        """ 根据用户ID获取关联岗位 """
        sql = select(PostRelation).where(PostRelation.user_id == user_id)
        _relation = await db.scalars(sql)
        relation = jsonable_encoder(_relation.all())
        result = []
        if relation:
            for dept_id in [item['post_id'] for item in relation]:
                sql = select(self.model).where(self.model.id == dept_id)
                _ids = await db.scalars(sql)
                post = jsonable_encoder(_ids.all())
                for post_id in post: result.append(post_id)
        return result

    async def createRelation(self, db: AsyncSession, obj_in: dict) -> int:
        """ 创建岗位关联用户数据 """
        sql = insert(PostRelation).values(obj_in)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def removeRelation(self, db: AsyncSession, user_id: int) -> int:
        """ 删除用户关联表 """
        sql = delete(PostRelation).where(PostRelation.user_id == user_id)
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
        """ 按条件查询 """

        baseSQL = select(self.model).where(self.model.delete == delete)

        if any([queryObj["name"], queryObj["code"]]):
            sql = baseSQL.where(self.model.name.like('%' + queryObj["name"] + '%'),
                                self.model.code.like('%' + queryObj["code"] + '%'))
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
        return {
            "items": result, "pageInfo": {
                "total": total, "currentPage": pageIndex, "totalPage": page_total(total, pageSize)
            }
        }

    async def getChangeSort(self, db: AsyncSession, obj_in: dict) -> int:
        """ 修改列表排序 """
        sql = update(self.model).where(self.model.id == obj_in["id"]).values({"sort": obj_in["numberValue"]})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount


getPost = CRUDPost(Post)
