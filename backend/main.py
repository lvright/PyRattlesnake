# -*- coding: utf-8 -*-

import uvicorn
import os
from fastapi import FastAPI
from core import setting
from utils.logger import logger
from db import init_db, init_data, init_redis_pool
from register import register_mount, register_exception, register_cors, register_middleware, register_router


app = FastAPI(description=setting.PROJECT_DESC, version=setting.PROJECT_VERSION, docs_url=setting.API_DOCS)

def create_app():
    """ 注册中心 """
    register_mount(app)  # 挂载静态文件

    register_exception(app)  # 注册捕获全局异常

    register_router(app)  # 注册路由

    register_middleware(app)  # 注册请求响应拦截

    register_cors(app)  # 注册跨域请求

    logger.info("日志初始化成功！")  # 初始化日志

@app.on_event("startup")
async def startup():
    create_app()  # 加载注册中心
    await init_db()  # 初始化表
    await init_data()
    app.state.redis = await init_redis_pool()  # redis

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()  # 关闭 redis


if __name__ == '__main__':
    os.system(f"figlet -f slant {setting.PROJECT_NAME}")
    uvicorn.run(app='main:app', host="127.0.0.1", debug=True, reload=True, port=8082)