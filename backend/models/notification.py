# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from backend.models import Base


class Notification(Base):
    """ 系统通知 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    title = Column(String(100), comment="通知标题")

    users = Column(String(25), comment="发送用户")

    content = Column(String(500), comment="通知内容")

    remark = Column(String(300), comment='备注')