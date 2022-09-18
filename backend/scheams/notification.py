# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class SystemMessage(BaseModel):
    """ 系统消息模型 """
    title: Optional[str] = None
    remark: Optional[str] = None
    users: Any = None
    content: Optional[str] = None
    content_type: Optional[str] = None


class SystemNotification(BaseModel):
    """ 系统通知模型 """
    title: Optional[str] = None
    type: Optional[str] = None
    remark: Optional[str] = None
    users: Optional[Any] = None
    content: Optional[str] = None