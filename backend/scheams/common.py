# -*- coding: utf-8 -*-

from datetime import datetime
from pydantic import BaseModel, validator


class GMT(BaseModel):
    """ 时间字段处理 """
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at")
    def format_time(cls, value: datetime) -> str:
        return value.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间
