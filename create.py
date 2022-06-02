# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from back_stage import router as admin

# 创建app
app = FastAPI(
    title="APIS-LINE",
    description="""PYRIGHT 是基于FASTAPI模块，配备了Web开发过程所需的工具和代码块。""",
    version='1.0',
    docs_url="/api/v1/docs",  # 自定义文档地址
    redoc_url=None,  # 禁用redoc文档
    openapi_url="/api/v1/openapi.json",
    openapi_tags=[
        {
            "name": "back_stage",
            "description": "后台模块API",
        },
        {
            "name": "application_tools",
            "description": "应用工具模块API",
        },
    ]
)

# fastapi蓝图
app.include_router(admin)

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins='http://localhost:2800/',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 静态文件设置
# Jinja2Templates(directory="./templates")
# app.mount("/static", StaticFiles(directory="./static"), name="static")