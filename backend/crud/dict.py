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


class SystemDictData(CRUDBase[Dict, DictDate]):

    async def getByCode(self, db: AsyncSession, code: str) -> list:
        sql = select(self.model).where(self.model.code == code)
        dict_data = await db.scalars(sql)
        result = jsonable_encoder(dict_data.all())
        result = [{"id": res["id"], "key": res["value"], "title": res["label"]} for res in result]
        return result


class SystemDeptType(CRUDBase[DictType, DictType]):

    pass


getDictType = SystemDeptType(DictType)

getDict = SystemDictData(Dict)