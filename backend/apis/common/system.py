# -*- coding: utf-8 -*-
import celery
from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders

from utils import resp_200, resp_400, resp_500, resp_404, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user, page_total
from backend.crud import getLoginLog, getOperLog, getBackendSetting
from backend.core import check_jwt_token
from backend.scheams import Token, Result, BackendSetting
from backend.db import MyRedis

router = APIRouter()

@router.get(path="/system/common/getLoginLogList", summary="系统登录日志")
async def get_login_log(username: str, orderBy: str, orderType: str, pageSize: int, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    total = await getLoginLog.get_number(db)
    result = await getLoginLog.get_multi(db, orderBy="login_time", orderType="desc", pageIndex=1, pageSize=pageSize)
    result = [res for res in result if res["username"] == username and res]
    return resp_200(data={"items": result, "pageInfo": {"total": total, "currentPage": 1, "totalPage": page_total(total, pageSize)}})

@router.get(path="/system/common/getOperationLogList", summary="系统登录日志")
async def get_oper_log(username: str, orderBy: str, orderType: str, pageSize: int, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    total = await getOperLog.get_number(db)
    result = await getOperLog.get_multi(db, orderBy="login_time", orderType="desc", pageIndex=1, pageSize=pageSize)
    result = [res for res in result if res["username"] == username and result]
    return resp_200(data={"items": result, "pageInfo": {"total": total, "currentPage": 1, "totalPage": page_total(total, pageSize)}})

@router.put(path="/system/setting/backendSetting", summary="更新系统配置")
async def update_backend_setting(backend_setting: BackendSetting, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getBackendSetting.updateBackendSetting(db, user_id=token["id"], obj_in=backend_setting.dict())
    return resp_200(msg="更新成功")