# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base


class RoleRelation(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    user_id = Column(Integer, comment="关联用户ID")

    role_id = Column(Integer, comment="关联角色ID")