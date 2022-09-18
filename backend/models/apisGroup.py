# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text

from backend.models import Base


class ApiGroup(Base):
    """ Api分组 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    name = Column(String(20), comment="分组名称")

    status = Column(Integer, comment="分组状态")

    remark = Column(String(300), comment="备注")