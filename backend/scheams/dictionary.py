# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class DictDate(BaseModel):
    """ 数据字典模型 """
    label: Optional[str] = None
    value: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None
    sort: Optional[int] = None
    type_id: Optional[int] = None


class DictClassify(BaseModel):
    """ 数据字典分类模型 """
    code: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None