# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base


class App(Base):
    """ App管理 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    app_name = Column(String(20), comment="app名称")

    app_id = Column(String(100), comment="AppID")

    app_secret = Column(String(100), comment="AppSecret")

    group_id = Column(Integer, ForeignKey("appgroup.id", ondelete="CASCADE"), comment="分组ID")

    remark = Column(String(300), comment="备注")

