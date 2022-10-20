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
from backend.scheams import BackendSetting
from backend.models import Setting
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis


class CRUDBackendSetting(CRUDBase[Setting, BackendSetting]):

    async def updateBackendSetting(self, db: AsyncSession, obj_in: dict, user_id: int) -> bool:
        sql = update(self.model).where(self.model.user_id == user_id).values(obj_in)
        await db.execute(sql)
        await db.commit()
        return True


getBackendSetting = CRUDBackendSetting(Setting)
