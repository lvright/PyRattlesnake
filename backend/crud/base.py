# -*- coding: utf-8 -*-

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import func, distinct, select, insert, update, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

from backend.core import verify_password
from backend.models import Base
from utils import obj_as_dict, list_obj_as_dict

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

# db.scalar(sql) 返回的是标量(原始数据) <models.department.Department object at 0x000002F2C2D22110>
# db.execute(sql) 返回的是元组 (<models.department.Department object at 0x000002F2C2D22110>)
# db.scalars(sql).all()  [<models...>, <models...>, <models...>]
# db.execute(sql).fetchall()  [(<models...>,), (<models...>,), (<models...>,)]

class CRUDBase(Generic[ModelType, SchemaType]):
    """ CRUD 增 查 改 删 """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """ 通过 id 获取对象 """
        sql = select(self.model).where(self.model.id == id)
        result = await db.execute(sql)
        await db.close()  # 释放会话
        data = jsonable_encoder(result.first())[str(self.model.__name__)]
        return data

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        """ 获取表里的所有数据 """
        sql = select(self.model)
        result = await db.execute(sql)
        await db.close()
        data = [res[str(self.model.__name__)] for res in jsonable_encoder(result.all())]
        return data

    async def get_first(self, db: AsyncSession) -> dict:
        """ 获取最新一条数据 """
        sql = select(self.model)
        result = await db.execute(sql)
        await db.close()
        data =  jsonable_encoder(result.first())[str(self.model.__name__)]
        return data

    async def get_multi(
            self, db: AsyncSession,
            orderBy: str = None,
            orderType: str = "ascending",
            pageIndex: int = 1,
            pageSize: int = 10
    ) -> List[ModelType]:
        """ 获取第 pageIndex 页的 pageSize 数据 """
        if orderType == "descending":
            if pageIndex and pageSize <= 1: sql = select(self.model).order_by(desc(orderBy))
            else: sql = select(self.model).offset((pageIndex - 1) * pageSize).limit(pageSize).order_by(desc(orderBy))
        else:
            if pageIndex and pageSize <= 1: sql = select(self.model)
            else: sql = select(self.model).offset((pageIndex - 1) * pageSize).limit(pageSize)
        result = await db.scalars(sql)
        data = jsonable_encoder(result.all())
        await db.close()  # 释放会话
        return data

    async def get_number(self, db: AsyncSession) -> int:
        """ 获取表的总条数 """
        sql = select(func.count(distinct(self.model.id)))
        result = await db.scalar(sql)
        await db.close()  # 释放会话
        return result

    async def create(self, db: AsyncSession, obj_in: SchemaType) -> int:
        """ 添加对象 """
        if isinstance(obj_in, dict):  # 判断对象是否为字典类型(更新部分字段)
            obj_data = obj_in
        else:
            obj_data = obj_in.dict()
        for k in obj_data.keys():
            if isinstance(obj_data[k], bool):
                obj_data[k] = str(int(obj_data[k]))
        sql = insert(self.model).values(obj_data)
        result = await db.execute(sql)
        await db.commit()
        return result.lastrowid

    async def update(self, db: AsyncSession, id: int, obj_in: Union[SchemaType, Dict[str, Any]]) -> int:
        """ 通过 id 更新对象 """
        if isinstance(obj_in, dict):  # 判断对象是否为字典类型(更新部分字段)
            obj_data = obj_in
        else:
            obj_data = obj_in.dict()
        for k in obj_data.keys():
            if isinstance(obj_data[k], bool):
                obj_data[k] = str(int(obj_data[k]))
        sql = update(self.model).where(self.model.id == id).values(obj_data)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def remove(self, db: AsyncSession, id: int) -> int:
        """ 通过 id 删除对象 """
        sql = delete(self.model).where(self.model.id == id)
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def tombstone(self, db: AsyncSession, id: int) -> int:
        """ 通过 id 逻辑删除 """
        sql = update(self.model).where(self.model.id == id).values({"delete": "1"})
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def remove_multi(self, db: AsyncSession, id_list: list):
        """ 同时删除多个对象 """
        id_list = [int(i) for i in id_list]  # postgresql 字段类型限制
        sql = delete(self.model).where(self.model.id.in_(id_list))
        result = await db.execute(sql)
        await db.commit()
        return result.rowcount

    async def get_multi_relation(self, db: AsyncSession):
        """ 获取关系字段 """
        sql = select(self.model.id, self.model.name).order_by(desc(self.model.id)).distinct()
        result = await db.execute(sql)
        await db.close()
        return result.fetchall()

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[ModelType]:
        """ 通过名字得到用户 """
        sql = select(self.model).where(self.model.name == name)
        result = await db.scalar(sql)
        await db.close()  # 释放会话
        return result

    async def authenticate(self, db: AsyncSession, username: str, password: str) -> Optional[ModelType]:
        """ 验证用户 """
        user = await self.get_by_name(db, name=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def sort(self, db: AsyncSession, name: str, pageIndex: int = 1, pageSize: int = 10) -> List[ModelType]:
        """ 验证用户 """
        filed_name = self.model.__table__.c[name]
        if pageIndex == -1 and pageSize == -1:
            sql = select(self.model).order_by(desc(filed_name))
        else:
            sql = select(self.model).offset((pageIndex - 1) * pageSize).limit(pageSize).order_by(desc(filed_name))
        result = await db.scalars(sql)
        await db.close()  # 释放会话
        return result.all()