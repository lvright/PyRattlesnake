# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from backend.models import Base
from utils import check_or_enum


class Setting(Base):
    """ 系统配置 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    color = Column(String(20), comment='系统主色')

    language = Column(String(20), comment='系统语言')

    layout = Column(String(20), comment='系统布局')

    menuCollapse = Column(Integer, comment="是否展开菜单: 0->否 1->是")

    menuWidth = Column(Integer, comment='菜单宽度')

    mode = Column(String(20), comment='菜单模式')

    skin = Column(String(20), comment='系统皮肤')

    tag = Column(Integer, comment="是否显示标签: 0->否 1->是")

    user_id = Column(String(5), comment='绑定用户ID')