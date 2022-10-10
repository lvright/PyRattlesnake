# -*- coding: utf-8 -*-

from fastapi import FastAPI, Security
from backend.core.conf import setting
from backend.apis import app_router
from backend.apis.deps import get_current_user
from backend.apis.common import login, admin, system, dept, post, role, dict, menu, annex

def register_router(app: FastAPI):
    """ 注册路由 """
    app.include_router(login.router, prefix=setting.API_PREFIX, tags=["Login"])  # Login(权限在每个接口上)
    app.include_router(admin.router, prefix=setting.API_PREFIX, tags=["Admin"])
    app.include_router(system.router, prefix=setting.API_PREFIX, tags=["System"])
    app.include_router(dept.router, prefix=setting.API_PREFIX, tags=["Dept"])
    app.include_router(post.router, prefix=setting.API_PREFIX, tags=["Post"])
    app.include_router(role.router, prefix=setting.API_PREFIX, tags=["Role"])
    app.include_router(dict.router, prefix=setting.API_PREFIX, tags=["Dictionary"])
    app.include_router(menu.router, prefix=setting.API_PREFIX, tags=["Menu"])
    app.include_router(annex.router, prefix=setting.API_PREFIX, tags=["Annex"])

    # 权限(权限在每个接口上)
    app.include_router(app_router, prefix=setting.API_PREFIX)
