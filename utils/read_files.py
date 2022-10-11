# -*- coding: utf-8 -*-

import pandas as pd
import os
import datetime, time

def read_local_files(relative_path):
    """ 读取本地文件 """
    result = []
    path = os.path.abspath("..") + relative_path
    for r, d, f in os.walk(path):
        for i in f:
            fileValue = os.stat(path + i)
            time_local = time.localtime(fileValue.st_atime / 1000)
            dt = time.strftime("%Y-%m-%d", time_local)
            fileData = {
                "mime_type": str(i).split(".")[1],
                "object_name": str(fileValue.st_ino) + "." + str(i).split(".")[1],
                "origin_name": i,
                "size_byte": fileValue.st_size,
                "size_info": str(fileValue.st_size / 1000) + "KB",
                "storage_mode": fileValue.st_mode,
                "storage_path": dt,
                "suffix": str(i).split(".")[1],
                "url": relative_path + i
            }
            result.append(fileData)
    return result