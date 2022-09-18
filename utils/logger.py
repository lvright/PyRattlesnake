# -*- coding: utf-8 -*-

import os
from loguru import logger
from backend.core.conf import setting

# 请不要随意移动该文件,创建文件夹是根据当前文件位置来创建
def create_dir(file_name: str) -> str:
    """ 创建文件夹 """
    current_path = os.path.dirname(__file__)  # 获取当前文件夹
    base_path = os.path.abspath(os.path.join(current_path, ".."))  # 获取当前文件夹的上一层文件
    path = base_path + os.sep + file_name + os.sep  # 拼接日志文件夹的路径
    os.makedirs(path, exist_ok=True)  # 如果文件夹不存在就创建
    return path

# 创建日志文件名
def logger_file() -> str:
    """ 创建日志文件名 """
    log_path = create_dir(setting.LOGGER_DIR)

    """ 保留日志文件夹下最大个数(本地调试用) 
    本地调式需要多次重启, 日志轮转片不会生效 """
    file_list = os.listdir(log_path)
    if len(file_list) > 3:
        os.remove(os.path.join(log_path, file_list[0]))
    # 日志输出路径
    return os.path.join(log_path, setting.LOGGER_NAME)


logger.add(
    logger_file(),
    encoding=setting.GLOBAL_ENCODING,
    level=setting.LOGGER_LEVEL,
    rotation=setting.LOGGER_ROTATION,
    retention=setting.LOGGER_RETENTION,
    enqueue=True
)