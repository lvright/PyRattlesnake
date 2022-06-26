# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  角色管理模块
#  ---

@router.get(path='/role/roleList', summary='获取角色列表', tags=['角色管理'])
async def get_role_list(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: role_list 角色列表 -> list

    """

    roles = par_type.to_json(db.execute(select(admin_roles)).all())

    return http.respond(status=200, data=roles)


@router.get(path='/role/rolesIndex', summary='获取角色分页列表', tags=['角色管理'])
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

    """

    Args:
        page: 当前页
        pageSize: 分页数
        code: 角色标识
        status: 角色状态
        name: 角色名称
        orderBy: 排序
        orderType: 排序规则
        maxDate: 最大时间
        minDate: 最小时间
        _: 时间戳
        token_info: token 认证

    Returns: roles_list 角色列表 -> list

    """

    roles_list = []

    offset_page = (page - 1) * pageSize

    # 筛选式查询 any判断传参有值时 介入查询条件 [code, name, status]
    if any([code, name, status]):

        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(admin_roles).where(and_(
            admin_roles.c.code.like('%' + code + '%'),
            admin_roles.c.name.like('%' + name + '%'),
            admin_roles.c.status.like('%' + status + '%'))).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in fuzzy_range_data: roles_list.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(admin_roles).where(
            minDate <= admin_roles.c.created_at,
            maxDate >= admin_roles.c.created_at).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in time_range_data: roles_list.append(item)

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        roles_list = par_type.to_json(db.execute(select(
            admin_roles).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all())
    elif orderType == 'ascending':
        roles_list = par_type.to_json(db.execute(select(
            admin_roles).order_by(orderBy).limit(pageSize).offset(offset_page)).all())
    # 如果没有查询条件则按分页查询
    else:
        roles_list = par_type.to_json(db.execute(select(
            admin_roles).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(admin_roles.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': roles_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.post(path='/role/roleSave', summary='创建角色', tags=['角色管理'])
async def create_role(role: admin.RolesForm, token_info: str = Depends(http.token)):

    """

    Args:
        role: 角色信息
        token_info: token 认证

    Returns: respond

    """

    # 传参数据格式化
    role = dict(role)
    del role['dept_ids'], role['menu_ids']
    # 插入创建时间
    role['created_at'] = now_date_time
    role['created_by'] = now_timestamp

    # 插入角色数据
    db.execute(insert(admin_roles).values(**role))
    db.commit()

    return http.respond(200, True, '创建成功')

@router.put(path='/role/roleUpdate/{roleId:path}', summary='编辑角色', tags=['角色管理'])
async def create_role(
        roleId: int,
        role: admin.RolesForm,
        token_info: str = Depends(http.token)
):

    """

    Args:
        roleId: 角色ID
        role: 角色信息
        token_info: token 认证

    Returns:

    """

    # 传参数据格式化
    role = dict(role)
    del role['dept_ids']

    if role['menu_ids']:
        db.execute(delete(admin_menu_account).where(admin_menu_account.c.role_id == role_data.id))
        for menu_id in role['menu_ids']:
            db.execute(admin_menu_account.insert().values(**{'role_id': role_data.id, 'menu_id': menu_id}))
            db.commit()
    else:
        del role['menu_ids']
        # 插入创建时间
        role['updated_at'] = now_date_time
        role['updated_by'] = now_timestamp
        # 更新角色数据
        db.execute(update(admin_roles).where(admin_roles.c.id == roleId).values(**role))
        db.commit()

    return http.respond(status=200)


@router.delete(path='/role/roleDelete/{roleId:path}', summary='删除角色', tags=['角色管理'])
async def delete_role(roleId: str, token_info: str = Depends(http.token)):

    """

    Args:
        roleId: 角色ID
        token_info: token 认证

    Returns: respond

    """

    try:
        # 提交删除
        for id in roleId.split(','):
            db.execute(delete(admin_roles).where(admin_roles.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)


@router.put(path='/auth/changeStatus', summary='修改角色状态', tags=['角色管理'])
def auth_change_status(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """

    Args:
        id: 角色ID
        status: 角色状态
        token_info: token 认证

    Returns: respond

    """

    db.execute(update(admin_roles).where(admin_roles.c.id == id).values(status=status))
    db.commit()

    return http.respond(status=200)