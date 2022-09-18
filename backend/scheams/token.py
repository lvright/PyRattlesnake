# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    """ token """
    access_token: str


class TokenData(BaseModel):
    sub: Optional[str] = None
    scopes: List[str] = []
