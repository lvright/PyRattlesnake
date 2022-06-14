# -*- coding: utf-8 -*-

from back_stage import *


@router.get(path='/menu/menuIndex', summary='获取菜单列表')
async def menu_index(_: int, token_info: str = Depends(http.token)):

    admin_menu_list = [dict(menu) for menu in db.query(admin_system_menu).all() if menu]

    # 处理返回的路由结构
    if admin_menu_list:

        menu_list = []

        # children 路由结构
        for item in admin_menu_list:

            item['children'] = [menu for menu in admin_menu_list if menu['parent_id'] == item['id']]

            if item['parent_id'] == 0: menu_list.append(item)

        return http.respond(200, True, '获取成功', menu_list)

@router.get(path='/menu/tree', summary='获取菜单权限')
def menu_tree(_: int, token_info: str = Depends(http.token)):

    """获取菜单权限"""

    admin_menu_list = db.query(admin_system_menu).where(
        admin_system_menu.c.status != '1'
    ).with_entities(
        admin_system_menu.c.id, admin_system_menu.c.title,
        admin_system_menu.c.id, admin_system_menu.c.parent_id
    ).all()

    admin_menu_list = [dict(menu) for menu in admin_menu_list if menu]

    # 处理返回的路由结构
    if admin_menu_list:

        menu_list = []

        # children 路由结构
        for items in admin_menu_list:

            items['label'] = items['title']
            items['value'] = items['id']

            del items['title']

            items['children'] = [menu for menu in admin_menu_list if menu['parent_id'] == items['id']]

            if items['parent_id'] == 0: menu_list.append(items)

        return http.respond(200, True, '获取成功', menu_list)

@router.get(path='/menu/getMenuByRole/{id:path}', summary='获取角色已拥有菜单权限')
def get_menu_by_role(id: int, token_info: str = Depends(http.token)):

    """获取角色已拥有菜单权限"""

    role_menu_list = db.query(
        admin_system_menu, admin_menu_account
    ).filter(
        admin_menu_account.c.role_id == id,
        admin_system_menu.c.id == admin_menu_account.c.menu_id
    ).with_entities(
        admin_system_menu.c.id,
        admin_system_menu.c.parent_id,
        admin_menu_account.c.menu_id,
        admin_menu_account.c.role_id
    ).all()

    role_menu_list = [dict(menu) for menu in role_menu_list if menu]

    print(role_menu_list)

    menu_list = [
        {
            'id': id,
            'menus': [
                {
                    'id': items['menu_id'],
                    'pivot': {
                        'role_id': items['role_id'],
                        'menu_id': items['menu_id']
                    }
                }
            ]
        }
        for items in role_menu_list if items
    ]

    return http.respond(200, True, '获取成功', menu_list)

@router.put(path='/menu/menuUpdate/{menuId:path}', summary='更新菜单')
async def menu_update(menuId: int, menu: admin.AdminMenuForm, token_info: str = Depends(http.token)):

    """更新菜单"""

    db.execute(admin_system_menu.update().where(admin_system_menu.c.id == menuId).values(**dict(menu)))
    db.commit()

    return http.respond(200, True, '保存成功')

@router.post(path='/menu/menuSave/{menuId:path}', summary='新建菜单')
async def menu_update(menu: admin.AdminMenuForm, token_info: str = Depends(http.token)):

    """新建菜单"""

    db.execute(admin_system_menu.insert().values(**dict(menu)))
    db.commit()

    return http.respond(200, True, '保存成功')

@router.delete(path='/menu/menuDelete/{ids:path}', summary='删除菜单')
def menu_delete(ids: Any, token_info: str = Depends(http.token)):

    """删除菜单"""

    try:
        # split ids
        for id in ids.split(','):
            # 循环删除
            db.execute(admin_system_menu.delete().where(admin_system_menu.c.id == int(id)))
            db.commit()
    except Exception as e:
        # 错误回滚 打印日志
        log.log_error(e)
        db.rollback()

    return http.respond(200, True, '删除成功')
