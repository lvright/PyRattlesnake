# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Optional

class Annex(BaseModel):
    """ 附件管理模型 """
    object_name: Optional[str] = None
    origin_name: Optional[str] = None
    size_byte: Optional[str] = None
    size_info: Optional[str] = None
    storage_mode: Optional[str] = None
    storage_path: Optional[str] = None
    suffix: Optional[str] = None
    url: Optional[str] = None
    remark: Optional[str] = None