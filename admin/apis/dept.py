# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  部门管理模块
#  ---

@router.get(path='/dept/deptIndex', summary='获取部门列表', tags=['部门管理'])
async def dept_list(
        # 查询筛选条件
        page: int,
        pageSize: int,
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
        code: Optional[str] = '',
        name: Optional[str] = '',
        status: Optional[str] = '',
        maxDate: Optional[str] = '',
        minDate: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序规则
        code: 部门标识
        name: 部门名称
        status: 部门状态
        maxDate: 最大时间
        minDate: 最小时间
        _: 时间戳
        token_info: token 认证

    Returns: user_dept_list 部门分页列表 -> list

    """

    admin_dept_list = []

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([code, status, name]):
        # 按传参条件查询
        fuzzy_range_data = db.execute(select(admin_dept).where(and_(
            admin_dept.c.leader.like('%' + code + '%'), admin_dept.c.status.like('%' + status + '%'),
            admin_dept.c.name.like('%' + name + '%'))).limit(pageSize)).all()
        # 更新data列表数据
        for item in fuzzy_range_data: data.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([minDate, maxDate]):
        time_range_data = db.execute(select(admin_dept).where(
            minDate <= admin_dept.c.created_at, maxDate >= admin_dept.c.created_at)).all()
        # 更新data列表数据
        for item in time_range_data: data.append(item)

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        admin_dept_list = par_type.to_json(db.execute(select(
            admin_dept).order_by(desc(orderBy)).limit(pageSize)).all())
    elif orderType == 'ascending':
        admin_dept_list = par_type.to_json(db.execute(select(
            admin_dept).order_by(orderBy).limit(pageSize)).all())

    # 如果没有查询条件则按分页查询
    else:
        admin_dept_list = par_type.to_json(db.execute(select(admin_dept)).all())

    # 建立部门树状结构数据
    dept_list = []
    if admin_dept_list:
        for items in admin_dept_list:
            items['children'] = [dept for dept in admin_dept_list if dept['parent_id'] == items['id']]
            if items['parent_id'] == 0: dept_list.append(items)

    return http.respond(200, True, 'OK', dept_list)

@router.get(path='/dept/userDept/tree', summary='获取部门树', tags=['部门管理'])
async def get_dept_tree(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: dept_list 树状部门列表 -> list

    """

    user_dept_list = par_type.to_json(db.execute(select(admin_dept)).all())

    # 建立部门树状数据
    dept_list = []

    if user_dept_list:
        user_dept_list = [{'id': dept['id'], 'label': dept['name'], 'parent_id': dept['parent_id'],
                           'value': dept['id']} for dept in user_dept_list]

        for items in user_dept_list:
            items['children'] = [dept for dept in user_dept_list if dept['parent_id'] == items['id']]
            if items['parent_id'] == 0: dept_list.append(items)

    return http.respond(status=200, data=dept_list)


@router.put(path='/dept/updateDept', summary='更新部门', tags=['部门管理'])
async def update_dept(depts: admin.Dept, token_info: str = Depends(http.token)):

    """

    Args:
        depts: 部门信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化传参
    dept = dict(depts)
    # 插入更新时间
    dept['updated_by'] = now_date_time
    dept['updated_at'] = now_timestamp

    # 更新部门数据
    db.execute(update(admin_dept).where(admin_dept.c.id == depts.id).values(**dept))

    return http.respond(status=200)

@router.delete(path='/dept/deptDelete/{deptId:path}', summary='删除部门', tags=['部门管理'])
async def delete_dept(deptId: str, token_info: str = Depends(http.token)):

    """

    Args:
        deptId: 部门ID
        token_info: token 认证

    Returns: respond

    """

    try:
        # 删除部门
        dept_id_list = deptId.split(',')
        for id in dept_id_list:
            db.execute(admin_dept.delete().where(admin_dept.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.error(e)
        db.rollback()
        return http.respond(status=200)

    return http.respond(status=200)


@router.post(path='/dept/deptSave', summary='添加角色', tags=['部门管理'])
async def dept_save(dept: admin.Dept, token_info: str = Depends(http.token)):

    """

    Args:
        dept: 部门信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化传参
    dept = dict(dept)
    # 插入创建时间
    dept['created_at'] = now_date_time
    dept['created_by'] = now_timestamp

    # 格式化 parent_id
    if isinstance(dept['parent_id'], list):
        dept['parent_id'] = dept['parent_id'][-1]

    # 插入数据
    db.execute(insert(admin_dept).values(**dept))
    db.commit()

    return http.respond(status=200)


@router.put(path='/dept/deptUpdate/{deptId:path}', summary='编辑角色', tags=['部门管理'])
async def dept_update(deptId: int, dept: admin.Dept, token_info: str = Depends(http.token)):

    """

    Args:
        deptId: 部门ID
        dept: 部门信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化传参
    dept = dict(dept)
    # 更新编辑时间
    dept['updated_at'] = now_date_time
    dept['updated_by'] = now_timestamp

    # 处理部门 parent_id
    if isinstance(dept['parent_id'], list):
        dept['parent_id'] = dept['parent_id'][-1]

    # 更新数据
    db.execute(update(admin_dept).where(admin_dept.c.id == deptId).values(**dept))
    db.commit()

    return http.respond(status=200)


@router.put(path='/dept/changeStatus', summary='更改部门状态', tags=['部门管理'])
async def dept_change_status(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """

    Args:
        id: 部门ID
        status: 部门状态
        token_info: token 认证

    Returns: respond

    """

    # 变更 status 状态
    db.execute(update(admin_dept).where(admin_dept.c.id == id).values(status=status))
    db.commit()

    return http.respond(status=200)