# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class Dept(BaseModel):
    """ 部门模型 """
    id: Optional[int] = None
    leader: Optional[str] = None
    name: Optional[str] = None
    parent_id: Optional[str] = None
    phone: Optional[str] = None
    remark: Optional[str] = None
    sort: Optional[int] = None
    status: Optional[str] = None