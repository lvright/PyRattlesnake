# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text, ForeignKey

from backend.models import Base
from utils import check_or_enum


class Api(Base):
    """Api管理"""

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    api_id = Column(Integer, comment="ApiID")

    name = Column(String(20), comment="API名称")

    group_id = Column(Integer, ForeignKey("apigroup.id", ondelete="CASCADE"), comment="分组ID")

    data_type = Column(String(10), comment="API数据类型")

    is_required = check_or_enum(name="is_required", enumList=['0', '1'], comment="是否必须: 0->是 1->否")

    default_value = Column(String(10), comment="API值")

    description = Column(String(10), comment="描述")

    type = Column(String(10), comment="API类型")

    remark = Column(String(300), comment="备注")