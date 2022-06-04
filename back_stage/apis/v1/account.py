# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------用户账户模块----------

@router.post(path='/info', summary='获取账号信息')
async def admin_info(token_info: str = Depends(http.token)):

    """获取账号信息"""

    # 根据返回的 token 解密后获得当前账户 userid 查询 userid 账户信息
    admin_info = db.query(admin_account).filter_by(userId=token_info['userId']).first()

    if admin_info:
        admin_info = dict(admin_info)

        # 根据 admin_role_relation 关联表查询菜单
        admin_menu_list = [
            dict(menu) for menu in db.query(admin_system_menu, admin_role_relation).filter(
                admin_role_relation.c.role_id == admin_info['id'],
                admin_system_menu.c.id == admin_role_relation.c.menu_id
            ).all()
        ]

        # 处理返回的路由结构
        if admin_menu_list:
            menu_list = []
            for items in admin_menu_list:
                items['meta'] = {
                    'hidden': bool(int(items['hidden'])),
                    'hiddenBreadcrumb': bool(items['hiddenBreadcrumb']),
                    'icon': items['icon'],
                    'title': items['title'],
                    'type': items['type']
                }
                del items['hidden'], items['hiddenBreadcrumb'], items['icon'], items['title'], items['type']
                if items['status'] == '0':
                    items['children'] = [
                        menu for menu in admin_menu_list
                        if menu['parent_id'] == items['menu_id']
                        if menu['status'] == '0'
                    ]
                    if items['parent_id'] == 0: menu_list.append(items)

            # 获取系统配置
            back_setting = db.query(backend_setting).filter_by(user_id=token_info['id']).first()

            # 插入 backend_setting 系统设置
            admin_info['backend_setting'] = dict(back_setting)

            return http.respond(200, True, '加载完成', {
                'codes': ['*'],
                'roles': [token_info['userId']],
                'routers': menu_list,
                'user': admin_info
            })

    return http.respond(500, False, '获取失败')

@router.post(path='/user/updateInfo', summary='修改账号信息')
async def admin_edit_info(edit_info: admin.AdminUpdateInfo, token_info: str = Depends(http.token)):

    """修改账号信息"""

    # 格式化
    edit_data = dict(edit_info)

    # 在修改账户接口中删除 AdminUpdateInfo model 的 dept_id
    del edit_data['dept_id']

    db.execute(admin_account.update().where(admin_account.c.userId == token_info['userId']).values(**edit_data))
    db.commit()

    return http.respond(200, True, '修改成功')

@router.post(path='/user/modifyPassword', summary='修改账户密码')
async def modify_password(password: admin.ModifyPassword, token_info: str = Depends(http.token)):

    """修改账户密码"""

    db.execute(admin_account.update().where(admin_account.c.userId == token_info['userId']).values(password=password.newPassword))
    db.commit()

    return http.respond(200, True, '密码修改成功')

@router.put(path='/user/initUserPassword/{userId:path}', summary='初始化账户密码')
async def init_password(userId: int, token_info: str = Depends(http.token)):

    """初始化账户密码"""

    db.execute(admin_account.update().where(admin_account.c.id == userId).values(password='123456'))
    db.commit()

    return http.respond(200, True, '已初始化密码')