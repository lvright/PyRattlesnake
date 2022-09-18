# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, func

from backend.models import Base
from utils import check_or_enum


class UserMenu(Base):
    """ 系统路由 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    name = Column(String(50), comment="菜单名称")

    path = Column(String(30), comment="菜单路径")

    parent_id = Column(Integer, comment="上级ID")

    icon = Column(String(50), comment="菜单图标")

    redirect = Column(String(25), comment="重定向")

    title = Column(String(15), comment="菜单标题")

    hidden = check_or_enum(name="hidden", enumList=["0", "1"], comment="是否隐藏: 0->是 1->否")

    type = Column(String(5), comment="菜单类型")

    component = Column(String(200), comment="菜单组件")

    sort = Column(Integer, comment="序号")

    level = Column(Integer, comment="菜单等级")

    status = check_or_enum(name="status", enumList=["0", "1"], comment="状态: 0->正常 1->禁用")