# -*- coding: utf-8 -*-

from sqlalchemy import Enum, CheckConstraint, String, Column

from backend.core import setting


# sex = Column(String(1), CheckConstraint("sex in ('1', '2', '3')")) # sqlite
# sex = Column(Enum('0', '1')) # mysql
# sex = Column(Enum('0', '1', name='sex_enum')) # postgresql

def check_or_enum(name: str, enumList: [], comment: str = ''):
    """
        - sqlite不支持枚举, 用check约束
        - mysql和postgresql用check没效果, 用枚举限制
    """
    if setting.DATABASE_URI.startswith('sqlite'):
        return Column(String(1), CheckConstraint(f"{name} in {tuple(enumList)}"), nullable=False, comment=comment)
    else:
        return Column(Enum(*enumList, name=name), nullable=False, comment=comment)
