# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Post
from backend.models import Post, PostRelation
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis

class SystemPost(CRUDBase[Post, Post]):

    async def userPost(self, db: AsyncSession, user_id: int):
        """ 根据用户ID获取关联岗位 """
        sql = select(PostRelation).where(PostRelation.user_id == user_id)
        relation_data = await db.scalars(sql)
        _relation = jsonable_encoder(relation_data.all())
        result = []
        if _relation:
            for dept_id in [item['post_id'] for item in _relation]:
                sql = select(self.model).where(self.model.id == dept_id)
                ids_data = await db.scalars(sql)
                ids_post = jsonable_encoder(ids_data.all())
                print(ids_post)
                for post in ids_post: result.append(post)
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

getPost = SystemPost(Post)