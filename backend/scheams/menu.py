# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class Menu(BaseModel):
    """ 系统路由模型 """
    code: Optional[str] = None
    path: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    redirect: Optional[str] = None
    name: Optional[str] = None
    hidden: Optional[bool] = None
    hiddenBreadcrumb: Optional[bool] = None
    type: Optional[str] = None
    component: Optional[str] = None
    sort: Optional[int] = None
    level: Optional[str] = None
    status: Optional[str] = None