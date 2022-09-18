# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class ChangeSort(BaseModel):
    """ 修改列表排序模型 """
    id: Optional[int] = None
    numberName: Optional[str] = None
    numberValue: Optional[int] = None


class ChangeStatus(BaseModel):
    """ 修改状态模型 """
    id: Optional[int] = None
    status: Optional[str] = None


class DeleteIds(BaseModel):
    """ 删除模型 """
    ids: Optional[list] = None