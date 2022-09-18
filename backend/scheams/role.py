# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class Role(BaseModel):
    """ 系统角色模型 """
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    remark: Optional[str] = None
    sort: Optional[int] = None
    status: Optional[str] = None
    data_scope: Optional[str] = None
    dept_ids: Optional[str] = None
    menu_ids: Optional[str] = None


class BaseRole(BaseModel):
    """ 增 改角色模型 """
    id: Optional[int] = None
    name: Optional[str] = None
    code: Optional[str] = None
    remark: Optional[str] = None
    sort: Optional[int] = None
    status: Optional[str] = None


class RoleDataScope(BaseModel):
    """ 保存部门角色数据模型 """
    data_scope: Optional[int] = None
    dept_ids: Optional[list] = None


