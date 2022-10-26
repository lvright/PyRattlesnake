# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional
from fastapi import File, UploadFile, Form


class BackendSetting(BaseModel):
    """系统配置模型"""
    color: Optional[str] = None
    language: Optional[str] = None
    layout: Optional[str] = None
    menuCollapse: Optional[str] = None
    menuWidth: Optional[int] = None
    mode: Optional[str] = None
    skin: Optional[str] = None
    tag: Optional[str] = None
    user_id: Optional[int] = None

class ExtendConfig(BaseModel):
    """ 系统扩展配置模型 """
    id: Optional[int] = None
    group_name: Optional[str] = None
    isSet: Optional[bool] = None
    isVirtual: Optional[bool] = None
    key: Optional[str] = None
    name: Optional[str] = None
    remark: Optional[str] = None
    value: Optional[str] = None


class SystemConfig(BaseModel):
    """ 系统配置信息模型 """
    site_copyright: Optional[str] = None
    site_desc: Optional[str] = None
    site_keywords: Optional[str] = None
    site_name: Optional[str] = None
    site_record_number: Optional[str] = None
    site_storage_mode: Optional[str] = None


class MenuForm(BaseModel):
    """ 系统菜单模型 """
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


class ConfigByKey(BaseModel):
    """ 系统登录配置模型 """
    key: str = None


class RedisInfo(BaseModel):
    """ redis key模型 """
    key: str = None