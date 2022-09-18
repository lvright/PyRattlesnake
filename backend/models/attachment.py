# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, text

from backend.models import Base


class Attachment(Base):
    """ 附件管理 """

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    object_name = Column(String(20), comment="现文件名称")

    origin_name = Column(String(20), comment="原文件名称")

    size_byte = Column(String(20), comment="文件类型")

    size_info = Column(String(20), comment="文件大小")

    storage_mode = Column(String(20), comment="文件模式")

    storage_path = Column(String(100), comment="文件地址")

    suffix = Column(String(20), comment="文件后缀")

    url = Column(String(100), comment="附件地址")

    remark = Column(String(300), comment="备注")