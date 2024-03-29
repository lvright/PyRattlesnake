# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders

from utils import resp_200, resp_400, resp_500, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user, check_jwt_token, page_total
from backend.crud import getNotification
from backend.scheams import Token, Result, SystemNotification, ChangeStatus, Ids, ChangeSort
from backend.db import MyRedis

router = APIRouter()


@router.post(
    path="/system/notice/save",
    response_model=Result,
    summary="添加公告"
)
async def save_notice(
        notice: SystemNotification,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for user_id in notice.users:
        data = notice.dict()
        data["users"] = str(user_id)
        await getNotification.create(db, obj_in=data)
    return resp_200(msg="添加成功")


@router.get(
    path="/system/common/getNoticeList",
    response_model=Result,
    summary="系统公告列表"
)
async def recycle_notice(
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        pageSize: Optional[int] = 10,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getNotification.get_multi(db, pageSize=pageSize, orderBy=orderBy, orderType=orderType)
    return resp_200(data=result)


@router.get(
    path="/system/notice/index",
    response_model=Result,
    summary="系统通知分页列表"
)
async def get_notice_page(
        page: Optional[int] = 1, pageSize: Optional[int] = 10,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        title: Optional[str] = "", type: Optional[str] = "",
        maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getNotification.getQuery(
        db, queryObj={"title": title, "type": type, "maxDate": maxDate, "minDate": minDate}, delete="0",
    ))


@router.get(
    path="/system/notice/recycle",
    response_model=Result,
    summary="系统通知分页列表"
)
async def recycle_notice(
        page: Optional[int] = 1, pageSize: Optional[int] = 10,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        title: Optional[str] = "", type: Optional[str] = "",
        maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getNotification.getQuery(
        db, queryObj={"title": title, "type": type, "maxDate": maxDate, "minDate": minDate}, delete="1",
    ))
