# -*- coding: utf-8 -*-

from typing import List, Union
from backend.core.conf import setting
from utils import PermissionNotEnough


def handle_oauth2_scopes():
    """ 配置 OAuth2PasswordBearer 的 scopes """
    join_dict = {}
    for item in setting.PERMISSION_DATA:
        join_dict.update(item)
    return join_dict


def generate_permission_data():
    """ 生成 permission 表数据 """
    data = []
    for item in setting.PERMISSION_DATA:
        (key, value), = item.items()  # , 一定要存在
        data.append({'name': key, 'desc': value})
    return data