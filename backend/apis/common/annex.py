# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Result, Token, DeptStructure, ChangeStatus, DeleteIds, ChangeSort
from backend.models import Attachment
from backend.crud import CRUDBase, getAnnex
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis
from utils import resp_200

router = APIRouter()

@router.get(path="/system/attachment/index", response_model=Result, summary="获取附件分页列表")
async def get_page_dept(
        page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "", mime_type: Optional[str] = "",
        origin_name: Optional[str] = "", storage_mode: Optional[str] = "", maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    query_obj = {"origin_name": origin_name, "storage_mode": storage_mode, "mime_type": mime_type, "maxDate": maxDate, "minDate": minDate}
    result = await getAnnex.getQuery(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page, "totalPage": result["page_total"]}})

@router.get(path="/system/attachment/recycle", response_model=Result, summary="获取被删除附件分页列表")
async def get_page_dept(
        page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "", mime_type: Optional[str] = "",
        origin_name: Optional[str] = "", storage_mode: Optional[str] = "", maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    query_obj = {"origin_name": origin_name, "storage_mode": storage_mode, "mime_type": mime_type, "maxDate": maxDate, "minDate": minDate}
    result = await getAnnex.getQueryReclcle(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page, "totalPage": result["page_total"]}})

@router.delete(path="/system/attachment/delete", response_model=Result, summary="删除附件[逻辑删除]")
async def delete_dept(annex: DeleteIds, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for id in annex.ids: await getAnnex.tombstone(db, id)
    return resp_200(msg="删除成功")

