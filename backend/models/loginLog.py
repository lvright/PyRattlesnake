# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, func

from backend.models import Base
from utils import check_or_enum


class LoginLog(Base):
    """ 登录日志 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    username = Column(String(20), comment="用户昵称")

    ip = Column(String(25), comment="登录IP地址")

    os = Column(String(20), comment="登录系统")

    ip_location = Column(String(50), comment="IP所在地")

    message = Column(String(150), comment="日志消息")

    login_time = Column(DateTime, server_default=func.now(), comment='登录时间')

    status = check_or_enum(name="status", enumList=["0", "1"], comment="状态: 0->正常 1->禁用")

