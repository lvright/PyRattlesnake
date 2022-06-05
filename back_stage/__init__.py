# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Body, Header, Cookie
from back_stage.models import admin_model as admin
from utils import *

# APIRouter admin模块
router = APIRouter(prefix='/admin', tags=['back_stage'])


# TODO ------------数据库表连接池------------

# 账户和菜单管理
admin_account = data_base.table('admin_account')
admin_system_menu = data_base.table('admin_system_menu')

# 系统设置相关
backend_setting = data_base.table('backend_setting')
admin_config = data_base.table('admin_config')
admin_extend = data_base.table('admin_extend')

# 角色、部门、岗位表
admin_dept = data_base.table('admin_dept')
admin_roles = data_base.table('admin_roles')
admin_post = data_base.table('admin_post')

# 部门、角色、岗位、菜单权限与账户之间关联表
admin_role_relation = data_base.table('admin_role_relation')
admin_roles_account = data_base.table('admin_roles_account')
admin_dept_account = data_base.table('admin_dept_account')
admin_post_account = data_base.table('admin_post_account')

# 数据字典
data_dictionary = data_base.table('data_dictionary')
dictionary = data_base.table('dictionary')

# 附件管理
attachment = data_base.table('attachment')

# 应用管理
sys_app_group = data_base.table('sys_app_group')
sys_app = data_base.table('sys_app')

# api管理
sys_apis_group = data_base.table('sys_apis_group')
sys_apis = data_base.table('sys_apis')

# 系统通知
sys_message = data_base.table('sys_message')

# 导出接口模块
from back_stage.apis.v1 \
    import account, menu, roles, login, config, message, \
    dept, post, auth, attachment, interface, app