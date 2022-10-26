# -*- coding: utf-8 -*-

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud import CRUDBase
from backend.models import Setting
from backend.scheams import BackendSetting


class CRUDBackendSetting(CRUDBase[Setting, BackendSetting]):

    async def updateBackendSetting(self, db: AsyncSession, obj_in: dict, user_id: int) -> bool:
        sql = update(self.model).where(self.model.user_id == user_id).values(obj_in)
        await db.execute(sql)
        await db.commit()
        return True


getBackendSetting = CRUDBackendSetting(Setting)
