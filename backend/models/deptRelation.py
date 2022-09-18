# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base


class DeptRelation(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    user_id = Column(Integer, comment="关联用户ID")

    dept_id = Column(Integer, comment="关联岗位ID")
