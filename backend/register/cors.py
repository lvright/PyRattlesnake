# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.conf import setting


def register_cors(app: FastAPI):
    """ 跨域请求 """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in setting.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=("GET", "POST", "PUT", "DELETE"),
        allow_headers=("*", "authentication"),
    )