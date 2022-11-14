# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db, check_jwt_token
from backend.crud import getMessage, getUser
from backend.scheams import Result, SendMessage
from utils import resp_200

router = APIRouter()


@router.post(
    path="/system/queueMessage/sendPrivateMessage",
    response_model=Result,
    summary="发送消息"
)
async def send_message(
        message: SendMessage,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for user_id in message.users:
        send_user = await getUser.get(db, user_id)
        await getMessage.create(db, obj_in={
            "content": message.content,
            "title": message.title,
            "send_user": send_user["username"],
            "send_by": token["id"]
        })
    return resp_200(msg="已发送")


@router.get(
    path="/system/queueMessage/receiveList",
    response_model=Result,
    summary="消息分页列表"
)
async def get_message_page(
        page: Optional[int] = 1,
        pageSize: Optional[int] = 10,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        read_status: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        content_type: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getMessage.getQuery(
        db,
        queryObj={
            "read_status": read_status,
            "content_type": content_type,
            "maxDate": maxDate,
            "minDate": minDate
        },
        delete = "0",
    )
    return resp_200(data={
        "items": result["data"],
        "pageInfo": {
            "total": result["total"],
            "currentPage": page,
            "totalPage": result["page_total"]
        }
    })


@router.get(
    path="/system/queueMessage/sendList",
    response_model=Result,
    summary="已发送消息"
)
async def get_send_message_page(
        page: Optional[int] = 1,
        pageSize: Optional[int] = 10,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        read_status: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        content_type: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getMessage.getQuery(
        db,
        queryObj={
            "read_status": read_status,
            "content_type": content_type,
            "maxDate": maxDate,
            "minDate": minDate
        },
        delete="0",
    )
    return resp_200(data={
        "items": result["data"],
        "pageInfo": {
            "total": result["total"],
            "currentPage": page,
            "totalPage": result["page_total"]
        }
    })
