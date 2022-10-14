# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders

from utils import resp_200, resp_400, resp_500, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user, check_jwt_token, page_total
from backend.crud import getMessage
from backend.scheams import Token, Result, MessageStructure, ChangeStatus, Ids, ChangeSort, SendMessage
from backend.db import MyRedis

router = APIRouter()

@router.get(path="/system/queueMessage/receiveList", response_model=Result, summary="消息分页列表")
async def get_message_page(
        page: Optional[int] = 1, pageSize: Optional[int] = 10, orderBy: Optional[str] = "", orderType: Optional[str] = "", read_status: Optional[str] = "",
        content_type: Optional[str] = "", db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    result = await getMessage.getQuery(db, query_obj={"read_status": read_status, "content_type": content_type})
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page, "totalPage": result["page_total"]}})

@router.post(path="/system/queueMessage/sendPrivateMessage", response_model=Result, summary="发送消息")
async def send_message(message: SendMessage, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for user_id in message.users: await getMessage.update(db, user_id, obj_in={"content": message.content, "title": message.title, "send_user": token["username"]})
    return resp_200(msg="已发送")