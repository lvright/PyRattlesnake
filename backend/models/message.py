# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, func

from backend.models import Base
from utils import check_or_enum


class Message(Base):
    """ 系统消息 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    content = Column(String(500), comment="消息内容")

    read_status = check_or_enum(name="read)_status", enumList=["0", "1"], comment="阅读状态: 0->未被阅读 1->已被阅读")

    send_by = Column(Integer, comment="发送用户ID")

    send_user = Column(String(20), comment="发送用户昵称")

    receive_by = Column(Integer, comment="接收方式")