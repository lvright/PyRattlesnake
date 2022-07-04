# -*- coding: utf-8 -*-

import celery
from admin.models import model as admin
from admin.core.celery import celery
from utils import *


# TODO
#  ---
#  APIRouter admin模块
#  ---

router = APIRouter(prefix='/admin')


# TODO
#  ---
#  接口文档分类
#  ---

tags = [
    {
        'name': '登录',
        'description': '登录模块',
    }, {
        'name': '用户',
        'description': '用户模块',
    }, {
        'name': '应用模块',
        'description': '系统第三方应用模块',
    }, {
        'name': '系统附件',
        'description': '系统附件管理',
    }, {
        'name': '角色管理',
        'description': '系统角色管理',
    }, {
        'name': '系统服务',
        'description': '系统服务配置和服务信息',
    }, {
        'name': '系统配置',
        'description': '系统配置管理',
    }, {
        'name': '数据字典',
        'description': '系统数据字典',
    }, {
        'name': '部门管理',
        'description': '组织部门管理',
    }, {
        'name': 'Api应用管理',
        'description': '应用的api管理',
    }, {
        'name': '系统日志',
        'description': '系统日志管理',
    }, {
        'name': '菜单管理',
        'description': '系统功能菜单管理',
    }, {
        'name': '岗位管理',
        'description': '组织岗位管理',
    }, {
        'name': '角色管理',
        'description': '组织角色管理',
    }, {
        'name': '系统消息',
        'description': '系统消息管理',
    },

]


# TODO
#  ---
#  数据库表连接池
#  ---

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
admin_menu_account = data_base.table('admin_menu_account')
admin_roles_account = data_base.table('admin_roles_account')
admin_dept_account = data_base.table('admin_dept_account')
admin_post_account = data_base.table('admin_post_account')

# 数据字典
sys_dictionary_data = data_base.table('sys_dictionary_data')
sys_dictionary = data_base.table('sys_dictionary')

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
sys_notification = data_base.table('sys_notification')

# 系统日志
sys_login_log = data_base.table('sys_login_log')
sys_oper_log = data_base.table('sys_oper_log')


# TODO
#  ---
#  导出接口模块
#  ---

from admin.apis import \
    account, app, attachment, config, dept, \
    interface, logger, login, menu, message, \
    post, roles