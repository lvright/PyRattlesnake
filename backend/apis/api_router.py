# -*- coding: utf-8 -*-

from fastapi import APIRouter
from backend.apis.common import (
    login, admin, post, dept, role, system, dict, menu, message, annex
)

app_router = APIRouter()

# include_in_schema=False 隐藏属性

# common
# app_router.include_router(login.router, prefix="/admin", tags=["Login"])
