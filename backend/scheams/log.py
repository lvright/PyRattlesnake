# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional


class Loginlogger(BaseModel):
    """ 登录日志 """
    username: Optional[str] = None
    ip: Optional[str] = None
    os: Optional[str] = None
    ip_location: Optional[str] = None
    message: Optional[str] = None
    login_time: Optional[str] = None
    status: Optional[str] = None


class Operlogger(BaseModel):
    """ 操作日志 """
    username: Optional[str] = None
    router: Optional[str] = None
    ip: Optional[str] = None
    ip_location: Optional[str] = None
    response_code: Optional[str] = None
    metho: Optional[str] = None
    request_data: Optional[str] = None
    response_data: Optional[str] = None
    remark: Optional[str] = None