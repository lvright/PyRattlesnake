# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base


class MenuRelation(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    menu_id = Column(Integer, comment="关联菜单ID")

    role_id = Column(Integer, comment="关联角色ID")