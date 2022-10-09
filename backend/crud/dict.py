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
from backend.scheams import DictDate, DictClassify
from backend.models import Dict, DictType
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis


class CRUDDictData(CRUDBase[Dict, DictDate]):

    async def getByCode(self, db: AsyncSession, code: str) -> list:
        sql = select(self.model).where(self.model.code == code)
        _dict = await db.scalars(sql)
        result = [{"id": res["id"], "key": res["value"], "title": res["label"]} for res in jsonable_encoder(_dict.all())]
        return result


class CRUDDictType(CRUDBase[DictType, DictClassify]):

    pass


getDictType = CRUDDictType(DictType)

getDictData = CRUDDictData(Dict)