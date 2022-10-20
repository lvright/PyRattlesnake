# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, func

from backend.models import Base
from utils import check_or_enum


class LoginLog(Base):
    """ 登录日志 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    username = Column(String(20), comment="用户昵称")

    ip = Column(String(25), comment="登录IP地址")

    ip_location = Column(String(50), comment="IP所在地")

    login_time = Column(DateTime, server_default=func.now(), comment='登录时间')