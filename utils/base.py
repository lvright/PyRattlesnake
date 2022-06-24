# -*- coding: utf-8 -*-

import datetime
import time
import string
import random
import math
import yagmail
import markdown
import jwt
import json
import pymysql
import sqlalchemy
import logging
import redis
import argparse
import io
import torch
import paginator
import base64
import os
import sys
import pickle
import dload
import psutil
import cpuinfo
import platform
import uvicorn
import numpy as np
import pandas as pd
import fastapi
import requests
from binascii import hexlify
from fuzzywuzzy import fuzz
from sqlmodel import create_engine, SQLModel, Session, select, insert, update, join, union, and_, or_, func, Table, MetaData
from PIL import Image, ImageDraw, ImageFont
from fastapi import HTTPException, Header, UploadFile, File, WebSocket, WebSocketDisconnect, Request, FastAPI, Response, APIRouter, Depends, Body, Header, Cookie
from fastapi.responses import JSONResponse, StreamingResponse, UJSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Set, TypeVar, Any
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime, timedelta
from typing import List, Optional, Set, TypeVar
from logging.handlers import RotatingFileHandler
from config import *

"""
参数类型设置
"""
class ParType:

    def __init__(self):
        return

    # 将JSON转成字符串的路径拼接
    def parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'
        return url[0:-1]

    # AbstractKeyedTuple 对象转字典
    def to_json(self, res):
        if isinstance(res, list):
            res = [dict(items) for items in res if res]
            return res
        else:
            res = dict(res)
        return res

"""
时间设置
"""
class WideTime:

    def __init__(self):
        return

    # ISO时间戳获取
    def get_iso_timestamp(self):
        timestamp = datetime.datetime.utcnow()
        t = timestamp.isoformat("T", "milliseconds")
        return t + "Z"

"""
JWT加解密
"""
class JsonWebToken:

    def __init__(self):
        return

    # JWT加密
    def encode(self, msg):
        data_dict = {'exp': datetime.now() + timedelta(minutes=300000), 'massage': msg}
        headers = {'alg': 'HS256', 'typ': 'JWT'}
        auth = jwt.encode(data_dict, Config.secret_key, algorithm='HS256', headers=headers)
        return auth

    # JWT解密
    def decode(self, token):
        try:
            data = jwt.decode(token, Config.secret_key, algorithms='HS256')
        except Exception as e:
            return Log().log_error(e)
        return data['massage']

"""
验证码工具
"""
class Captcha:

    def __init__(self):
        return

    # 随机码生成 6位数字加大小写英文
    def random_code(self):
        """
        可用于邀请码、随机命名等
        :return: str
        """
        str_list = [random.choice(string.digits + string.ascii_letters) for _ in range(6)]
        code = ''.join(str_list)
        return code

    # 图形验证码
    def code_img(self):
        """
        图像验证码
        :return: file
        """
        # 定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片
        img = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))

        # 实例化一支画笔
        draw = ImageDraw.Draw(img, mode="RGB")

        # 定义要使用的字体和字体大小
        font = ImageFont.truetype(font='./static/font/Century751 No2 BT Bold Italic.ttf', size=28)

        # 将每次循环的char存code_text到数组里
        code_text = []

        for i in range(5):
            # 每循环一次,从a到z中随机生成一个字母或数字
            # 65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符
            # str把生成的数字转换成字符串
            char = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9))])
            code_text.append(char)
            # 每循环一次重新生成随机颜色
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # 把生成的字母或数字添加到图片上
            # 图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
            draw.text([i * 24, 0], char, color, font=font)

        # 将code_text数组转字符串
        code = ''.join(code_text)

        file = './static/captcha/' + str(Captcha().random_code()) + '.png'
        filename = file[1:]

        # 保存到本地，推荐保存到云存储
        img.save(file)

        return {'img_code': code, 'img_url': 'http://' + Config.url + ':' + str(Config.port) + filename}

"""
Response 工具类
"""
class ResponseMethod:
    """
    200 - 服务器成功返回网页，客户端请求已成功。
    302 - 对象临时移动。服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求。
    304 - 属于重定向。自上次请求后，请求的网页未修改过。服务器返回此响应时，不会返回网页内容。
    401 - 未授权。请求要求身份验证。 对于需要登录的网页，服务器可能返回此响应。
    404 - 未找到。服务器找不到请求的网页。
    2xx - 成功。表示服务器成功地接受了客户端请求。
    3xx - 重定向。表示要完成请求，需要进一步操作。客户端浏览器必须采取更多操作来实现请求。
          例如，浏览器可能不得不请求服务器上的不同的页面，或通过代理服务器重复该请求。
    4xx - 请求错误。这些状态代码表示请求可能出错，妨碍了服务器的处理。
    5xx - 服务器错误。表示服务器在尝试处理请求时发生内部错误。 这些错误可能是服务器本身的错误，而不是请求出错。

    :param code: 状态码
    :param success: 是否成功 Ture and False
    :param message: 状态消息
    :param data: 返回数据体
    """
    def __init__(self):
        return

    # 请求响应状态
    def respond(self, status, success=True, message='OK', data=None):
        if status != 200:
            success = False
            message = 'ERROR'
        results = {
            'status': status,
            'success': success,
            'message': message,
            'timestamp': str(int(time.time())),
            'data': data
        }
        return JSONResponse(status_code=status, content=results)

    # token 失效响应状态
    def token(self, token: str = Header(None)):
        info = JsonWebToken().decode(token)
        token_redis = DataBase().redis.get('user_token:' + info['username'])
        if isinstance(info, dict) and token_redis:
            return info
        raise HTTPException(status_code=401, detail={
            'status': 401,
            'success': False,
            'message': '登录验证失效',
            'timestamp': str(int(time.time()))
        })

"""
websocket 连接管理
"""
class ConnectionManager:

    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove(ws)

    @staticmethod
    async def send_personal_message(message, ws: WebSocket):
        # 发送个人消息
        if isinstance(message, str):
            await ws.send_text(message)
        if isinstance(message, dict):
            await ws.send_json(message)
        if isinstance(message, bytes):
            await ws.send_bytes(message)

    async def broadcast(self, message):
        # 广播消息
        for connection in self.active_connections:
            if isinstance(message, str):
                await connection.send_text(message)
            if isinstance(message, dict):
                await connection.send_json(message)
            if isinstance(message, bytes):
                await connection.send_bytes(message)

"""
第三方模块
"""
class Tackle:

    def __init__(self):
        return

    # 邮箱验证码
    def smtp_email(self, user_name, user_email):
        """
        :param user_name: 邮件内容称呼
        :param user_email: 发送的邮箱
        :return: email_code
        """
        smtp = yagmail.SMTP(user=Config.email, password=Config.email_pawssword, host=Config.email_host)
        subject = ["G-Markdown 您的邮箱验证码"]
        code = Captcha().random_code()
        contents = ['''[HTML]'''.format(user_name, code)]
        try:
            smtp.send(user_email, subject, contents)
        except EOFError as e:
            Log().log_error('邮箱发送失败：' + str(e))
        return code

    # markdown 模块
    def mkd(self, content):
        mkd_text = """[TOC]{}""".format(str(content))
        markdown.markdown(mkd_text, extensions=[
            # markdown支持的格式
            'markdown.extensions.toc',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables'
        ])
        return mkd_text

    # 拦截请求用户 ip 并查询地区
    def get_request_ip_info(self, host):

        info = {}

        try:
            get_ip_info = requests.get(Config.get_ip_url, {'ip': host, 'token': Config.get_ip_token})
            if get_ip_info.status_code == 200:
                location = get_ip_info.json()['data']
                if host in ['0.0.0.0', '127.0.0.1']:
                    info['ip_location'] = '本地测试'
                else:
                    info['ip_location'] = f'{location[0]}-{location[1]}-{location[2]}-{location[3]}'
        except Exception as e:
            Log().log_error(e)

        return info

"""
数据库类 SQLAlchemy
"""
class DataBase:

    def __init__(self):
        return

    # 数据库链接
    engine = create_engine(
        Config.databases,
        echo=True,
        pool_pre_ping=True,
        pool_use_lifo=True,
        future=True,
        pool_recycle=1000,
        execution_options={
            'isolation_level': 'REPEATABLE READ'
        }
    )

    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    metadata = MetaData()

    # redis 链接
    redis = redis.StrictRedis(
        host=Config.redis_host,
        port=Config.redis_port,
        decode_responses=Config.decode,
        db=Config.redis_db,
        password=Config.redis_paw
    )

    # 数据库表链接
    def table(self, table_name):
        table = Table(
            table_name,
            DataBase.metadata,
            autoload=True,
            autoload_with=DataBase.engine
        )
        return table

"""
日志模块
"""
class Log:

    def __init__(self):
        return

    # INFO：处理请求或者状态变化等日常事务
    def log_info(self, text):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.info(text)
        return

    # DEBUG：调试过程中使用DEBUG等级，如算法中每个循环的中间状态
    def log_debug(self, text):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.debug(text)
        return

    # WARNING：发生很重要的事件，但是并不是错误时，如用户登录密码错误
    def log_warning(self, text):
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.warning(text)
        return

    # ERROR：数据库连接、IO等操作失败或者连接问题
    def log_error(self, text):
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.error(text)
        return

    # FATAL：对业务造成致命错误
    def log_fatal(self):
        logging.basicConfig(level=logging.FATAL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.fatal(self.text)
        return

    # CRITICAL：特别糟糕的事情，如内存耗尽、磁盘空间为空，较少使用
    def log_critical(self):
        logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        logger.critical(self.text)
        return

"""
baseCodeKey 64位加密工具
"""
class BaseCode:

    def __init__(self):
        return

    app_id = str(hexlify(os.urandom(12)), 'utf-8')
    app_secret = base64.b64encode(app_id.encode(encoding='utf-8')).decode('utf-8')
    app_key_decode = base64.b64decode(app_secret.encode(encoding='utf-8'))