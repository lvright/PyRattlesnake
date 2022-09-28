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
from backend.scheams import Result, Token, ChangeSort, ChangeStatus, DeleteIds, menu
from backend.models import UserMenu
from backend.crud import CRUDBase, getMenu
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis
from utils import resp_200

router = APIRouter()

@router.get(path="/system/menu/tree", response_model=Result, summary="获取树状菜单")
async def get_tree_menu(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getMenu.menuTree(db))

@router.get(path="/system/menu/index", response_model=Result, summary="获取菜单分页列表")
async def get_page_menu(
    page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "",
    name: Optional[str] = "", code: Optional[str] = "", hidden: Optional[str] = "",
    maxDate: Optional[str] = "", minDate: Optional[str] = "", status: Optional[str] = "",
    db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    total = await getMenu.get_number(db)
    query_obj = {"name": name, "code": code, "hidden": hidden, "status": status, "maxDate": maxDate, "minDate": minDate}
    return resp_200(data=await getMenu.getQuery(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj))

@router.get(path="/system/menu/recycle", response_model=Result, summary="获取被删除菜单分页列表")
async def get_page_dept(
    page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "",
    name: Optional[str] = "", code: Optional[str] = "", hidden: Optional[str] = "",
    maxDate: Optional[str] = "", minDate: Optional[str] = "", status: Optional[str] = "",
    db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    total = await getMenu.get_number(db)
    query_obj = {"name": name, "code": code, "hidden": hidden, "status": status, "maxDate": maxDate, "minDate": minDate}
    return resp_200(data=await getMenu.getQueryReclcle(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj))