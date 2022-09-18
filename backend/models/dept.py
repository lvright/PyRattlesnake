# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base
from utils import check_or_enum


class UserDept(Base):
    """ 岗位 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    name = Column(String(20), comment="岗位名称")

    phone = Column(String(15), comment='联系号码')

    level = Column(String(20), comment="岗位等级")

    leader = Column(String(20), comment="负责人")

    parent_id = Column(Integer, comment="上级ID")

    sort = Column(Integer, comment="序号")

    status = check_or_enum(name="status", enumList=['0', '1'], comment="状态: 0->正常 1->禁用")

    remark = Column(String(300), comment="备注")
