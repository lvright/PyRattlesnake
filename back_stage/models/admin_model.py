# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field
from typing import List, Optional, Set, TypeVar, Any
from fastapi import Path, Query, Body, Header

# 登录账户信息
class AdminUpdateInfo(BaseModel):
    status: Optional[int] = Query(None)
    phone: Optional[str] = Query(None)
    nickname: Optional[str] = Query(None)
    email: Optional[str] = Query(None)
    dashboard: Optional[str] = Query(None)
    dept_id: Optional[int] = Query(None)
    id: Optional[int] = Query(None)
    login_ip: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    signed: Optional[str] = Query(None)
    updated_at: Optional[str] = Query(None)
    updated_by: Optional[str] = Query(None)
    userId: Optional[str] = Query(None)
    user_type: Optional[int] = Query(None)
    username: Optional[str] = Query(None)

# 账户密码
class ModifyPassword(BaseModel):
    oldPassword: str = Query(None)
    newPassword: str = Query(None)
    newPassword_confirmation: str = Query(None)

# 系统外观配置
class BackendSetting(BaseModel):
    colorPrimary: Optional[str] = Query(None)
    lang: Optional[str] = Query(None)
    layout: Optional[str] = Query(None)
    layoutTags: Optional[bool] = Query(None)
    theme: Optional[str] = Query(None)

# 系统扩展配置
class ExtendConfig(BaseModel):
    group_name: Optional[str] = Query(None)
    isSet: Optional[bool] = Query(None)
    isVirtual: Optional[bool] = Query(None)
    key: Optional[str] = Query(None)
    name: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    value: Optional[str] = Query(None)

# 系统配置信息
class SystemConfig(BaseModel):
    site_copyright: Optional[str] = Query(None)
    site_desc: Optional[str] = Query(None)
    site_keywords: Optional[str] = Query(None)
    site_name: Optional[str] = Query(None)
    site_record_number: Optional[str] = Query(None)
    site_storage_mode: Optional[str] = Query(None)

# 账户登录
class AdminLogin(BaseModel):
    username: str = Query(None)
    password: str = Query(None)

# 菜单
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

# 角色
class RolesForm(BaseModel):
    code: Optional[str] = Query(None)
    id: Optional[int] = Query(None)
    name: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    sort: Optional[int] = Query(None)
    status: Optional[str] = Query(None)
    data_scope: Optional[str] = Query(None)
    dept_ids: Optional[Any] = Query(None)
    menu_ids: Optional[Any] = Query(None)

# 岗位
class Post(BaseModel):
    code: Optional[str] = Query(None)
    name: Optional[str] = Query(None)
    status: Optional[str] = Query(None)
    sort: Optional[int] = Query(None)
    remark: Optional[str] = Query(None)

# 用户
class User(BaseModel):
    status: Optional[str] = Query(None)
    phone: Optional[str] = Query(None)
    nickname: Optional[str] = Query(None)
    email: Optional[str] = Query(None)
    password: Optional[str] = Query(None)
    dashboard: Optional[str] = Query(None)
    dept_id: Optional[Any] = Query(None)
    post_ids: Optional[Any] = Query(None)
    role_ids: Optional[Any] = Query(None)
    id: Optional[int] = Query(None)
    userId: Optional[str] = Query(None)
    login_ip: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    username: Optional[str] = Query(None)

# 部门
class Dept(BaseModel):
    id: Optional[int] = Query(None)
    leader: Optional[str] = Query(None)
    name: Optional[str] = Query(None)
    parent_id: Optional[Any] = Query(None)
    phone: Optional[str] = Query(None)
    remark: Optional[str] = Query(None)
    sort: Optional[int] = Query(None)
    status: Optional[str] = Query(None)

# 数据字典
class DictDate(BaseModel):
    label: Optional[str] = Query(None)
    value: Optional[str] = Query(None)
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
    users: Optional[Any] = Query(None)
    content: Optional[str] = Query(None)

# 系统登录配置
class ConfigByKey(BaseModel):
    key: str = Query(None)

# 在线用户
class OnlineUser(BaseModel):
    id: int = Query(None)

# redis信息
class RedisInfo(BaseModel):
    key: str = Query(None)