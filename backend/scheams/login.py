# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import List, Optional, Set, TypeVar, Any


class Login(BaseModel):
    """ 登录模型 """
    username: str
    password: str