# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    """ 岗位模型 """
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None
    sort: Optional[int] = None
    remark: Optional[str] = None