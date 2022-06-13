# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from typing import List, Optional, Set, TypeVar, Any
from fastapi import Path, Query, Body, Header

# 修改登录账户信息
class AdminUpdateInfo(BaseModel):
    status: int = Query(None)
    phone: str = Query(None)
    nickname: str = Query(None)
    email: str = Query(None)
    dashboard: str = Query(None)
    dept_id: int = Query(None)
    id: int = Query(None)
    login_ip: str = Query(None)
    remark: str = Query(None)
    signed: str = Query(None)
    updated_at: str = Query(None)
    updated_by: str = Query(None)
    userId: str = Query(None)
    user_type: int = Query(None)
    username: str = Query(None)

# 修改账户密码
class ModifyPassword(BaseModel):
    oldPassword: str = Query(None)
    newPassword: str = Query(None)
    newPassword_confirmation: str = Query(None)

# 系统外观配置
class BackendSetting(BaseModel):
    colorPrimary: str = Query(None)
    lang: str = Query(None)
    layout: str = Query(None)
    layoutTags: bool = Query(None)
    theme: str = Query(None)

# 系统扩展配置
class ExtendConfig(BaseModel):
    group_name: str = Query(None)
    isSet: bool = Query(None)
    isVirtual: bool = Query(None)
    key: str = Query(None)
    name: str = Query(None)
    remark: str = Query(None)
    value: str = Query(None)

# 系统配置信息
class SystemConfig(BaseModel):
    site_copyright: str = Query(None)
    site_desc: str = Query(None)
    site_keywords: str = Query(None)
    site_name: str = Query(None)
    site_record_number: str = Query(None)
    site_storage_mode: str = Query(None)

# 管理员登录
class AdminLogin(BaseModel):
    username: str = Query(None)
    password: str = Query(None)

# 添加/编辑菜单
class AdminMenuForm(BaseModel):
    component: Optional[str] = None,
    hidden: Optional[str] = None,
    hiddenBreadcrumb: Optional[int] = None,
    icon: Optional[str] = None,
    name: Optional[str] = None,
    parent_id: Optional[int] = None,
    path: Optional[str] = None,
    redirect:  Optional[str] = None,
    sort: Optional[int] = None,
    status: Optional[str] = None,
    title: Optional[str] = None,
    type: Optional[str] = None,

# 添加角色
class RolesForm(BaseModel):
    code: str = Query(None)
    id: int = Query(None)
    name: str = Query(None)
    remark: str = Query(None)
    sort: int = Query(None)
    status: str = Query(None)
    data_scope: Optional[str] = ''
    dept_ids: Optional[Any] = ''

# 添加岗位
class Post(BaseModel):
    code: Optional[str] = Query(None)
    name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    sort: Optional[int] = Query(None)
    remark: Optional[str] = Query(None)

# 添加/编辑用户
class User(BaseModel):
    status: int = Query(None)
    phone: str = Query(None)
    nickname: str = Query(None)
    email: str = Query(None)
    password: str = Query(None)
    dashboard: str = Query(None)
    dept_id: list = Query(None)
    post_ids: list = Query(None)
    role_ids: list = Query(None)
    id: int = Query(None)
    userId: str = Query(None)
    login_ip: str = Query(None)
    remark: str = Query(None)
    username: str = Query(None)

# 部门
class Dept(BaseModel):
    id: int = Query(None)
    leader: str = Query(None)
    name: str = Query(None)
    parent_id: Any = Query(None)
    phone: str = Query(None)
    remark: str = Query(None)
    sort: int = Query(None)
    status: str = Query(None)

# 数据字典
class DictDate(BaseModel):
    label: str = Query(None)
    value: str = Query(None)
    code: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    sort: Optional[int] = Query(None)
    type_id: Optional[int] = Query(None)

# 数据字典类型
class DictType(BaseModel):
    code: Optional[str] = Query(None)
    name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)

# 应用分组
class AppGroup(BaseModel):
    name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)

# 应用
class App(BaseModel):
    app_id: Optional[str] = Query(None)
    app_secret: Optional[str] = Query(None)
    app_name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    group_id: Optional[str] = Query(None)
    description: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)

# api分组
class ApiGroup(BaseModel):
    name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)

# Apis
class Api(BaseModel):
    api_id: Optional[str] = Query(None)
    app_secret: Optional[str] = Query(None)
    app_name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    group_id: Optional[str] = Query(None)
    description: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)

# 系统消息
class SystemMessage(BaseModel):
    title: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    users: Any = Query(None)
    content: Optional[str] = Query(None)
    content_type: Optional[str] = Query(None)

# 系统通知
class SystemNotification(BaseModel):
    title: Optional[str] = Query(None)
    type: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    users: Any = Query(None)
    content: Optional[str] = Query(None)