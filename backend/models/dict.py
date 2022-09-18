# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base
from utils import check_or_enum


class Dict(Base):
    """ 数据字典 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    label = Column(String(20), comment='字典名称')

    value = Column(String(20), comment='字典值')

    code = Column(String(20), comment='字典标识')

    type_id = Column(Integer, ForeignKey("dicttype.id", ondelete="CASCADE"), comment="字典类型ID")

    sort = Column(Integer, comment="序号")

    status = check_or_enum(name="status", enumList=['0', '1'], comment="状态: 0->正常 1->禁用")

    remark = Column(String(300), comment='备注')













