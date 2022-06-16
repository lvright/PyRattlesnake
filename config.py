# -*- coding: utf-8 -*-

class Config:

    # 项目配置
    url = '127.0.0.1'
    port = 8082
    workers = 1

    # 数据库配置
    host = 'localhost'
    mysql_port = 3306
    db = 'pysql'
    root = 'root'
    password = 'root123456'
    databases = 'mysql+pymysql://root:root123456@localhost:3306/pysql'

    # redis
    redis_host = '127.0.0.1'
    redis_port = 6379
    redis_paw = ''
    decode = True
    redis_db = 0

    # SMTP邮箱配置
    email = '2978413623@qq.com'
    email_password = 'jabcbnmcmlkcdfdi'
    email_host = 'smtp.qq.com'

    # JWT 密钥
    secret_key = 'pyright'

    # 云存储
    security_token = ''
    secretID = ''
    secretKey = ''

class DevConfig(Config):
    pass
