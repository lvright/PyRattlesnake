# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from backend.models import Base
from utils import check_or_enum


class Role(Base):
    """ 角色 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    name = Column(String(20), comment='部门名称')

    code = Column(String(20), comment='部门标识')

    data_scope = Column(Integer, comment="ID")

    sort = Column(Integer, comment="ID")

    dept_ids = Column(String(50), comment='关联部门')

    menu_ids = Column(String(50), comment='关联菜单')

    status = check_or_enum(name="status", enumList=["0", "1"], comment="状态: 0->正常 1->禁用")

    remark = Column(String(300), comment='备注')