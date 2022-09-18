# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base


class Config(Base):
    """ 系统配置 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    group_name = Column(String(255), comment="配置组名称")

    key = Column(String(255), comment="系统配置Key")

    name = Column(String(255), comment="配置名称")

    sort = Column(Integer, comment="序号")

    value = Column(String(255), comment="系统配置值")

    remark = Column(String(255), comment="备注")