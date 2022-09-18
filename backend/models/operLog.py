# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from backend.models import Base


class OperLog(Base):
    """ 接口日志 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    username = Column(String(20), comment='操作用户')

    router = Column(String(50), comment="接口名称")

    ip = Column(String(25), comment="登录IP地址")

    ip_location = Column(String(50), comment="IP所在地")

    response_code = Column(String(5), comment="请求状态码")

    method = Column(String(10), comment="请求方式")

    request_data = Column(String(300), comment="请求参数")

    response_data = Column(String(300), comment="响应参数")

    remark = Column(String(300), comment='备注')
