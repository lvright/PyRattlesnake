# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------部门管理模块----------

@router.get(path='/dept/deptIndex', summary='获取部门列表')
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

    """获取部门列表"""

    admin_dept_list = []

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([code, status, name]):

        # 按传参条件查询
        fuzzy_range_data = db.query(admin_dept).filter(
            and_(
                admin_dept.c.leader.like('%' + code + '%'),
                admin_dept.c.status.like('%' + status + '%'),
                admin_dept.c.name.like('%' + name + '%')
            ),
        ).limit(pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            data.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([minDate, maxDate]):
        time_range_data = db.query(admin_dept).filter(
            minDate <= admin_dept.c.created_at,
            maxDate >= admin_dept.c.created_at
        ).all()

        # 更新data列表数据
        for item in time_range_data:
            data.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        admin_dept_list = [dict(dept_item) for dept_item in db.query(admin_dept).order_by(desc(orderBy)).limit(pageSize) if dept_item]

    elif orderType == 'ascending':
        admin_dept_list = [dict(dept_item) for dept_item in db.query(admin_dept).order_by(orderBy).limit(pageSize) if dept_item]

    # 如果没有查询条件则按分页查询
    else:
        admin_dept_list = [dict(dept_item) for dept_item in db.query(admin_dept).all() if dept_item]

    # 建立部门树状结构数据
    dept_list = []
    if admin_dept_list:
        for items in admin_dept_list:
            items['children'] = [
                dept for dept in admin_dept_list
                if dept['parent_id'] == items['id']
            ]
            if items['parent_id'] == 0: dept_list.append(items)

    return http.respond(200, True, 'OK', dept_list)

@router.get(path='/dept/userDept/tree', summary='获取部门树')
async def get_dept_tree(token_info: str = Depends(http.token)):

    """获取树状部门数据"""

    admin_dept_list = db.query(admin_dept).all()

    # 建立部门树状数据
    dept_list = []
    if admin_dept_list:
        admin_dept_list = [dict(item) for item in admin_dept_list if item]
        admin_dept_list = [{
            'id': dept['id'],
            'label': dept['name'],
            'parent_id': dept['parent_id'],
            'value': dept['id']
        } for dept in admin_dept_list]
        for items in admin_dept_list:
            items['children'] = [
                dept for dept in admin_dept_list
                if dept['parent_id'] == items['id']
            ]
            if items['parent_id'] == 0: dept_list.append(items)

    return http.respond(200, True, 'OK', dept_list)

@router.put(path='/dept/updateDept', summary='更新部门')
async def update_dept(depts: admin.Dept, token_info: str = Depends(http.token)):

    """更新部门数据"""

    # 格式化传参
    dept = dict(depts)

    # 插入更新时间
    dept['updated_by'] = now_date_time
    dept['updated_at'] = now_timestamp

    # 更新部门数据
    db.execute(admin_dept.update().where(id=depts.id).values(dept))

    return http.respond(200, True, '更新成功')

@router.delete(path='/dept/deptDelete/{deptId:path}', summary='删除部门')
async def delete_dept(deptId: str, token_info: str = Depends(http.token)):

    """删除部门"""

    try:
        # 删除部门
        dept_id_list = deptId.split(',')
        for dept_id in dept_id_list:
            db.execute(admin_dept.delete().where(admin_dept.c.id == dept_id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.log_error(e)
        db.rollback()

    return http.respond(200, True, '已删除')

@router.post(path='/dept/deptSave', summary='添加角色')
async def dept_save(dept: admin.Dept, token_info: str = Depends(http.token)):

    """添加角色"""

    # 格式化传参
    dept = dict(dept)

    # 插入创建时间
    dept['created_at'] = now_date_time
    dept['created_by'] = now_timestamp

    # 格式化 parent_id
    if isinstance(dept['parent_id'], list):
        dept['parent_id'] = dept['parent_id'][-1]

    # 插入数据
    db.execute(admin_dept.insert().values(dept))
    db.commit()

    return http.respond(200, True, '添加成功')

@router.put(path='/dept/deptUpdate/{deptId:path}', summary='编辑角色')
async def dept_update(deptId: int, dept: admin.Dept, token_info: str = Depends(http.token)):

    """编辑角色"""

    # 格式化传参
    dept = dict(dept)

    # 处理部门 parent_id
    if isinstance(dept['parent_id'], list):
        dept['parent_id'] = dept['parent_id'][-1]

    # 更新编辑时间
    dept['updated_at'] = now_date_time
    dept['updated_by'] = now_timestamp

    # 更新数据
    db.execute(admin_dept.update().where(admin_dept.c.id == deptId).values(dept))
    db.commit()

    return http.respond(200, True, '编辑成功')

@router.put(path='/dept/changeStatus', summary='更改部门状态')
async def dept_change_status(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """更改部门状态"""

    # 变更 status 状态
    db.execute(admin_dept.update().where(admin_dept.c.id == id).values(status=status))
    db.commit()

    return http.respond(200, True, '已变更状态')