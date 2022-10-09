# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class MenuStructure(BaseModel):
    """ 系统路由模型 """
    name: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    redirect: Optional[str] = None
    title: Optional[str] = None
    hidden: Optional[str] = None
    type: Optional[str] = None
    component: Optional[str] = None
    sort: Optional[int] = None
    level: Optional[str] = None
    status: Optional[str] = None