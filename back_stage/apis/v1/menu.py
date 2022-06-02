# -*- coding: utf-8 -*-

from back_stage import *


@router.get(path='/menu/menuIndex', summary='获取菜单列表')
async def menu_index(
        _: int,
        token_info: str = Depends(http.token)
):

    admin_menu_list = [dict(menu) for menu in db.query(admin_system_menu).all() if menu]

    # 处理返回的路由结构
    if admin_menu_list:

        menu_list = []

        # children 路由结构
        for item in admin_menu_list:

            item['children'] = [menu for menu in admin_menu_list if menu['parent_id'] == item['id']]

            if item['parent_id'] == 0: menu_list.append(item)

        return http.respond(200, True, '加载完成', menu_list)

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
