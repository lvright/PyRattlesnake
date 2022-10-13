# -*- coding: utf-8 -*-

import psutil
import sys
import fastapi

base_number = 1000000

def get_cpu():
    """ 获取系统cpu信息 """
    cpu_cores = psutil.cpu_count() # 逻辑CPU个数
    cpu_physical_cores = psutil.cpu_count(logical=False) # 物理CPU个数
    cpu_percent = psutil.cpu_percent() # cpu平均使用率
    cpu_freq = psutil.cpu_freq() # CPU频率

    return {"cores": f"物理核心数：{cpu_cores}个，逻辑核心数：{cpu_physical_cores}个", "usage": cpu_percent, "free": cpu_freq}

def get_memory():
    """ 获取主机内存信息 """
    memory = psutil.virtual_memory()

    memory_total = memory.total / base_number  # 总物理内存
    memory_used = memory.used / base_number  # 已使用的物理内存
    memory_free = memory.free / base_number  # 没使用的物理内存
    memory_available = memory.available / base_number  # 可用内存

    return {"total": memory_total, "usage": memory_used, "free": memory_free, "rate": memory_available}

def get_disk():
    """ 获取主机存储信息 """
    disk = psutil.disk_usage("/")

    disk_total = disk.total / base_number # 总空间
    disk_used = disk.used / base_number # 已使用空间
    disk_free = disk.free / base_number # 可用空间
    disk_percent = disk.percent # 使用率

    return {"total": disk_total, "usage": disk_used, "free": disk_free, "rate": disk_percent}

def get_system():
    """ 获取python系统信息 """
    sys_python_v = sys.version # python系统版本信息
    sys_path = sys.path[1] # 项目路径
    sys_fastapi_v = fastapi.__version__ # fastapi版本

    return {"python_version": sys_python_v, "project_path": sys_path, "fastapi_version": sys_fastapi_v}