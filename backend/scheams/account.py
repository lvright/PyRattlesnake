# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import List, Optional, Set, TypeVar, Any
from enum import Enum


class Account(BaseModel):
    """ 用户模型 """
    userId: Optional[str] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    dashboard: Optional[str] = None
    dept_id: Optional[str] = None
    post_ids: Optional[Any] = None
    role_ids: Optional[Any] = None
    login_ip: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class AccountUpdate(BaseModel):
    """ 更新用户模型 """
    id: Optional[int] = None
    userId: Optional[str] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    dashboard: Optional[str] = None
    login_ip: Optional[str] = None
    signed: Optional[str] = None
    user_type: Optional[int] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class QueryUser(BaseModel):
    """ 用户查询模型 """
    page: int = None
    pageSize: int = None
    orderBy: Optional[str] = None
    orderType: Optional[str] = None
    dept_id: Optional[str] = None
    role_id: Optional[str] = None
    post_id: Optional[str] = None
    username: Optional[str] = None
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    maxDate: Optional[str] = None
    minDate: Optional[str] = None


class Login(BaseModel):
    """ 登录模型 """
    username: str = None
    password: str = None


class ModifyPassword(BaseModel):
    """ 更改密码模型 """
    oldPassword: str = None
    newPassword: str = None
    newPassword_confirmation: str = None


class UserId(BaseModel):
    """ 用户ID """
    id: int = None


class UserIDList(BaseModel):
    """ 用户ID批量操作 """
    ids: list = None

class UserHome(BaseModel):
    id: int = None
    dashboard: str = None


