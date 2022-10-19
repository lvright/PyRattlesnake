# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional, Any


class SystemNotification(BaseModel):
    """ 系统通知模型 """
    title: Optional[str] = None
    type: Optional[str] = None
    remark: Optional[str] = None
    content: Optional[str] = None
    users: Optional[Any] = None