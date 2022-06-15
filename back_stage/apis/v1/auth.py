# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------角色管理模块----------

@router.get(path='/role/roleList', summary='获取角色列表')
async def get_role_list(token_info: str = Depends(http.token)):

    """获取角色列表"""

    roles = [dict(role) for role in db.query(admin_roles).all() if role]

    return http.respond(200, True, 'OK', roles)

@router.get(path='/role/rolesIndex', summary='获取角色分页列表')
async def get_post_list(
        page: int,
        pageSize: int,
        code: Optional[str] = '',
        status: Optional[str] = '',
        name: Optional[str] = '',
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        maxDate: Optional[str] = '',
        minDate: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token),
):

    """获取角色分页列表"""

    roles_list = []

    # 筛选式查询 any判断传参有值时 介入查询条件 [code, name, status]
    if any([code, name, status]):

        # 按传参条件查询
        fuzzy_range_data = db.query(admin_roles).filter(
            and_(
                admin_roles.c.code.like('%' + code + '%'),
                admin_roles.c.name.like('%' + name + '%'),
                admin_roles.c.status.like('%' + status + '%'),
            ),
        ).limit(pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            roles_list.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = db.query(admin_roles).filter(
            minDate <= admin_roles.c.created_at,
            maxDate >= admin_roles.c.created_at
        ).all()

        # 更新data列表数据
        for item in time_range_data:
            roles_list.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        roles_list = [dict(role) for role in db.query(admin_roles).order_by(desc(orderBy)).limit(pageSize) if role]

    elif orderType == 'ascending':
        roles_list = [dict(role) for role in db.query(admin_roles).order_by(orderBy).limit(pageSize) if role]

    # 如果没有查询条件则按分页查询
    else:
        roles_list = [dict(role) for role in db.query(admin_roles).limit(pageSize) if role]

    return http.respond(200, True, 'OK', {
        'items': roles_list,
        'pageInfo': {
            'total': len(roles_list),
            'currentPage': page,
            'totalPage': math.ceil(len(roles_list) / pageSize)
        }
    })

@router.post(path='/role/roleSave', summary='创建角色')
async def create_role(role_data: admin.RolesForm, token_info: str = Depends(http.token)):

    """创建角色"""

    # 传参数据格式化
    role = dict(role_data)

    del role['dept_ids'], role['menu_ids']

    # 插入创建时间
    role['created_at'] = now_date_time
    role['created_by'] = now_timestamp

    # 插入角色数据
    db.execute(admin_roles.insert().values(role))
    db.commit()

    return http.respond(200, True, '创建成功')

@router.put(path='/role/roleUpdate/{roleId:path}', summary='编辑角色')
async def create_role(
        roleId: int,
        role_data: admin.RolesForm,
        token_info: str = Depends(http.token)
):

    """编辑角色"""

    # 传参数据格式化
    role = dict(role_data)

    del role['dept_ids']

    if role['menu_ids']:

        db.execute(admin_menu_account.delete().where(admin_menu_account.c.role_id == role_data.id))

        for menu_id in role['menu_ids']:
            db.execute(admin_menu_account.insert().values({'role_id': role_data.id, 'menu_id': menu_id}))
            db.commit()

    else:

        del role['menu_ids']

        # 插入创建时间
        role['updated_at'] = now_date_time
        role['updated_by'] = now_timestamp

        # 更新角色数据
        db.execute(admin_roles.update().where(admin_roles.c.id == roleId).values(role))
        db.commit()

    return http.respond(200, True, '更新成功')

@router.delete(path='/role/roleDelete/{roleId:path}', summary='删除角色')
async def delete_role(roleId: str, token_info: str = Depends(http.token)):

    """删除角色"""

    try:
        role_id_list = roleId.split(',')
        # 提交删除
        for role_id in role_id_list:
            db.execute(admin_roles.delete().where(admin_roles.c.id == int(role_id)))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.log_error(e)
        db.rollback()
        return http.respond(500, False, str(e))

    return http.respond(200, True, '已删除')

@router.put(path='/auth/changeStatus', summary='修改角色状态')
def auth_change_status(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """修改角色状态"""

    db.execute(admin_roles.update().where(admin_roles.c.id == id).values(status=status))
    db.commit()

    return http.respond(200, True, '已变更状态')