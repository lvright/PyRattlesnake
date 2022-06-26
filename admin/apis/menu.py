# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  菜单管理
#  ---

@router.get(path='/menu/menuIndex', summary='获取菜单列表', tags=['菜单管理'])
async def menu_index(_: int, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: menu_list 菜单路由列表 -> list

    """

    admin_menu_list = par_type.to_json(db.execute(select(admin_system_menu)).all())

    # 处理返回的路由结构
    if admin_menu_list:
        menu_list = []
        # children 路由结构
        for item in admin_menu_list:
            item['children'] = [menu for menu in admin_menu_list
                                if menu['parent_id'] == item['id']]
            if item['parent_id'] == 0: menu_list.append(item)

        return http.respond(status=200, data=menu_list)


@router.get(path='/menu/tree', summary='获取菜单权限', tags=['菜单管理'])
def menu_tree(_: int, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: menu_list 菜单路由列表 -> list

    """

    admin_menu_list = par_type.to_json(db.execute(select(
        admin_system_menu).select_from(admin_system_menu.c.id, admin_system_menu.c.title, admin_system_menu.c.id,
                                       admin_system_menu.c.parent_id).where(admin_system_menu.c.status != '1')).all())
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

        return http.respond(status=200, data=menu_list)


@router.get(path='/menu/getMenuByRole/{id:path}', summary='获取角色已拥有菜单权限', tags=['菜单管理'])
def get_menu_by_role(id: int, token_info: str = Depends(http.token)):

    """

    Args:
        id: 角色ID
        token_info: token 认证

    Returns: menu_list 菜单路由列表 -> list

    """

    role_menu_list = par_type.to_json(db.execute(select(admin_system_menu, admin_menu_account)).select_from(
        admin_system_menu.c.id, admin_system_menu.c.parent_id, admin_menu_account.c.menu_id,
        admin_menu_account.c.role_id).where(admin_menu_account.c.role_id == id,
                                            admin_system_menu.c.id == admin_menu_account.c.menu_id).all())

    menu_list = [{'id': id, 'menus': [
        {'id': items['menu_id'], 'pivot': {'role_id': items['role_id'], 'menu_id': items['menu_id']}}
    ]} for items in role_menu_list if items]

    return http.respond(status=200, data=menu_list)


@router.put(path='/menu/menuUpdate/{menuId:path}', summary='更新菜单', tags=['菜单管理'])
async def menu_update(menuId: int, menu: admin.AdminMenuForm, token_info: str = Depends(http.token)):

    """

    Args:
        menuId: 菜单ID
        menu: 菜单信息
        token_info: token 认证

    Returns: respond

    """

    db.execute(update(admin_system_menu).where(
        admin_system_menu.c.id == menuId).values(**dict(menu)))
    db.commit()

    return http.respond(status=200)


@router.post(path='/menu/menuSave/{menuId:path}', summary='新建菜单', tags=['菜单管理'])
async def menu_update(menu: admin.AdminMenuForm, token_info: str = Depends(http.token)):

    """

    Args:
        menu: 菜单信息
        token_info: token 认证

    Returns: respond

    """

    db.execute(insert(admin_system_menu).values(**dict(menu)))
    db.commit()

    return http.respond(status=200)


@router.delete(path='/menu/menuDelete/{ids:path}', summary='删除菜单', tags=['菜单管理'])
def menu_delete(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 菜单ID
        token_info: token 认证

    Returns: respond

    """

    try:
        # split ids
        for id in ids.split(','):
            # 循环删除
            db.execute(delete(admin_system_menu).where(admin_system_menu.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 打印日志
        log.error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)
