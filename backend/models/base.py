# -*- coding: utf-8 -*-
import datetime
import time

from sqlalchemy import Column, DateTime, func, Integer, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# id 也能写在这里, 不过为了方便看字段, 就在每个表内创建了
# https://www.osgeo.cn/sqlalchemy/orm/mapping_api.html#sqlalchemy.orm.as_declarative
# noinspection PyMethodParameters

@as_declarative()
class Base:
    """ 基本表 """

    __name__: str  # 表名
    __table_args__ = {"mysql_charset": "UTF8MB4", "extend_existing": True}  # 设置表的字符集
    # __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新

    # 将类名小写并转化为表名 __tablename__
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @declared_attr
    def created_at(cls):  # 创建时间
        return Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')

    @declared_attr
    def updated_at(cls):  # 更新时间
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')

    @declared_attr
    def delete(cls):  # 逻辑删除
        return Column(String(5), server_default="0", comment="是否逻辑删除")