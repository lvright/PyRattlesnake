# -*- coding: utf-8 -*-

import secrets
from typing import Union, List
from pydantic import BaseSettings, AnyHttpUrl

project_desc = """
        🎉 管理员账户 🎉
        ✨ 账号: superAdmin ✨
        ✨ 密码: 888888 ✨
        ✨ 权限(scopes): superAdmin ✨
        """

class CeleryConf:

    broker_url: str = 'amqp://guest@localhost:5672'
    result_backend: str = 'redis://localhost:6379/1'

    imports: tuple = (
        'backend.crud.login.Login',
        'backend.crud.login.User',
    )

    enable_utc: bool = True
    task_serializer: str = 'json'
    result_serializer: str = 'json'

    IGNORE_RESULT: bool = True

    WORKER_DISABLE_RATE_LIMITS: bool = True
    RESULT_EXPIRES: int = 3600

    TASK_TIME_LIMIT: str = 600
    TASK_DEFAULT_ROUTING_KEY: str = "default"
    TASK_DEFAULT_EXCHANGE: str = "default"
    TASK_DEFAULT_EXCHANGE_TYPE: str = "direct"
    TASK_ANNOTATIONS: dict = {'*': {'rate_limit': '10/s'}}
    TASK_COMPRESSION: str = 'zlib'

    DEFAULT_QUEUE: str = 'default'

    TIMEZONE: str = 'Asia/Shanghai'

    WORKER_CONCURRENCY: str = 20
    WORKER_PREFETCH_MULTIPLIER: str = 4
    WORKER_MAX_TASKS_PER_CHILD: str = 200


class Settings(BaseSettings):

    PROJECT_NAME: str = "PyRattlesnake"
    PROJECT_DESC: str = project_desc  # 描述
    PROJECT_VERSION: Union[int, str] = 1.5  # 版本
    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8082"  # 开发环境
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:2888"]  # 跨域请求

    API_PREFIX: str = '/api'  # 接口前缀
    STATIC_DIR: str = 'static'  # 本地静态文件目录
    GLOBAL_ENCODING: str = 'utf-8'  # 全局编码
    API_DOCS = API_PREFIX + '/docs'  # 接口文档

    REDIS_URI: str = "redis://localhost:6379/0"  # redis
    DATABASE_URI: str = "mysql+asyncmy://root:123456@localhost:3306/snake?charset=UTF8MB4"  # MySQL(异步)
    DATABASE_ECHO: bool = True

    SECRET_KEY: str = 'lvright'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # token过期时间: 60 minutes * 24 hours * 1 days = 1 days

    LOGGER_DIR: str = "logs"  # 日志文件夹名
    LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log'  # 日志文件名 (时间格式)
    LOGGER_LEVEL: str = 'DEBUG'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "12:00"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "7 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    PERMISSION_DATA: List[dict] = [{}]

    class Config:
        case_sensitive = True  # 区分大小写


setting = Settings()

celconf = CeleryConf()