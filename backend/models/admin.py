# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, func, DateTime

from backend.core import setting, get_password_hash
from backend.models import Base
from utils import check_or_enum


class Admin(Base):
    """管理员"""

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    username = Column(String(20), comment='昵称')

    userId = Column(String(20), comment="用户唯一ID")

    nickname = Column(String(20), comment="用户唯一标识")

    avatar = Column(String(300), comment='头像')

    phone = Column(String(15), comment='手机号')

    email = Column(String(50), comment='邮箱')

    user_type = Column(String(10), comment='用户类型')

    password = Column(String(12), server_default="123456", comment='密码')

    signed = Column(String(100), server_default="人生苦短，我写Python", comment='简介')

    dashboard = Column(String(15), server_default="statistics", comment='控制台模式')

    login_ip = Column(String(25), comment='登录IP')

    login_time = Column(DateTime(timezone=True), server_default=func.now(), comment='登录时间')

    status = check_or_enum(name="status", enumList=['0', '1'], comment="是否必须: 0->正常 1->禁用")

    remark = Column(String(300), comment='备注')