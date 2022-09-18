# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base
from utils import check_or_enum


class Extend(Base):
    """ 系统设置 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    name = Column(String(20), comment='系统设置名称')

    key = Column(String(30), comment='系统设置KEY')

    value = Column(String(50), comment='系统设置值')

    group_name = Column(String(30), comment='设置分组名称')

    isSet = check_or_enum(name="isSet", enumList=['0', '1'], comment='是否插入: 0->是, 1->否')

    isVirtual = check_or_enum(name="isVirtual", enumList=['0', '1'], comment='是否模拟: 0->是, 1->否')

    sort = Column(Integer, comment="序号")

    remark = Column(String(300), comment='备注')


