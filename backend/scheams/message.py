# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class MessageStructure(BaseModel):
    """ 系统消息模型 """
    content: Optional[str] = None
    read_status: Optional[str] = None
    send_by: Optional[str] = None
    send_user: Optional[str] = None
    receive_by: Optional[str] = None


class SendMessage(BaseModel):
    """ 发送消息 """
    content: Optional[str] = None
    title: Optional[str] = None
    users: Optional[list] = None