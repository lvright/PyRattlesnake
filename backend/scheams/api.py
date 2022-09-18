# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class ApiGroup(BaseModel):
    """ api分组模型 """
    name: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class Api(BaseModel):
    """ api管理模型 """
    api_id: Optional[str] = None
    app_secret: Optional[str] = None
    app_name: Optional[str] = None
    status: Optional[str] = None
    group_id: Optional[str] = None
    description: Optional[str] = None
    remark: Optional[str] = None