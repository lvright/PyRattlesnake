# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class AppGroup(BaseModel):
    """ 应用分组模型 """
    name: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class App(BaseModel):
    """ 系统应用模型 """
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    app_name: Optional[str] = None
    status: Optional[str] = None
    group_id: Optional[str] = None
    description: Optional[str] = None
    remark: Optional[str] = None