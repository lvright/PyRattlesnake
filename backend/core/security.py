# -*- coding: utf-8 -*-

# @desc : 安全配置 https://fastapi.tiangolo.com/zh/advanced/security/oauth2-scopes/#global-view

from typing import Any, Union, Optional
from datetime import datetime, timedelta
from fastapi import Header
from jose import jwt
from passlib.context import CryptContext

from backend.core import setting
from utils import AccessTokenFail

ALGORITHM = "HS256"  # 加密算法

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # 加密密码

def get_password_hash(password: str) -> str:
    """ 加密明文密码 """
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """ 验证明文密码 与 加密后的密码 是否一致 """
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    生成token

    :param data: 存储数据
    :param expires_delta: 有效时间
    :return: 加密后的token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # eg: {'sub': '1', scopes: ['items'] 'exp': '123'}
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# https://www.cnblogs.com/CharmCode/p/14191112.html?ivk_sa=1024320u

async def check_jwt_token(token: Optional[str] = Header(...)) -> Union[str, Any]:
    """ 解密token """
    try:
        payload = jwt.decode(token=token, key=setting.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:  # jwt.JWTError, jwt.ExpiredSignatureError, AttributeError
        raise AccessTokenFail(f'token已过期! -- {e}')