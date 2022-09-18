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
from backend.scheams import DictDate, DictType
from backend.models import Dict, DictType
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis


class SystmDictData(CRUDBase[Dict, DictDate]):

    async def getByCode(self, db: AsyncSession, code: str) -> list:
        sql = select(self.model).where(self.model.code == code)
        dict_data = await db.scalars(sql)
        reslut = jsonable_encoder(dict_data.all())
        reslut = [{"id": res["id"], "key": res["value"], "title": res["label"]} for res in reslut]
        return reslut


class SystemDeptType(CRUDBase[DictType, DictType]):

    pass


getDictType = SystemDeptType(DictType)

getDict = SystmDictData(Dict)