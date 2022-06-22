# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  应用管理
#  ---

@router.get(path='/app/appGroup/index', summary='应用分类列表', tags=['应用模块'])
async def app_group(
        page: Optional[int] = 0,
        pageSize: Optional[int] = 0,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        status: Optional[str] = '',
        name: Optional[str] = '',
        _: Optional[int] = 0,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序类型
        status: 应用状态
        name: 应用名
        _:
        token_info: token 认证

    Returns: app_group_list 应用分组列表 -> list

    """

    offset_page = (page - 1) * pageSize

    if any([status, name]):
        app_group_list = [item for item in par_type.to_json(db.execute(select(sys_app_group).where(
            sys_app_group.c.name.like('%' + name + '%'),
            sys_app_group.c.status.like('%' + status + '%')).limit(pageSize).offset(offset_page)))]
    else:
        app_group_list = [item for item in par_type.to_json(db.execute(select(
            sys_app_group).limit(pageSize).offset(offset_page)))]

    total = db.query(func.count(sys_app_group.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': app_group_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.get(path='/app/appGroup/list', summary='获取应用分类列表', tags=['应用模块'])
async def app_list(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: app_group_list -> list

    """

    app_group_list = [{'name': item['name'], 'id': item['id']}
                      for item in db.execute(select(sys_app_group).all()) if item]

    return http.respond(status=200, data=app_group_list)

@router.post(path='/app/appGroup/save', summary='创建应用分组', tags=['应用模块'])
async def app_group_save(app_group: admin.AppGroup, token_info: str = Depends(http.token)):

    """

    Args:
        app_group: 应用分组信息
        token_info: token 认证

    Returns: respond

    """

    app_group = dict(app_group)
    app_group['created_at'] = now_date_time
    app_group['created_by'] = now_timestamp

    db.execute(insert(sys_app_group).values(**app_group))
    db.commit()

    return http.respond(status=200)

@router.put(path='/app/appGroup/update/{id:path}', summary='更新应用分组', tags=['应用模块'])
async def app_group_save(id: int, app_group: admin.AppGroup, token_info: str = Depends(http.token)):

    """

    Args:
        id: 应用分组ID
        app_group: 应用分组信息
        token_info: token 认证

    Returns: respond

    """

    app_group = dict(app_group)
    app_group['updated_at'] = now_date_time
    app_group['updated_by'] = now_timestamp

    db.execute(update(sys_app_group).where(sys_app_group.c.id == id).values(**app_group))
    db.commit()

    return http.respond(status=200)

@router.delete(path='/app/appGroup/delete/{ids:path}', summary='删除应用分组')
async def app_group_save(ids: str, token_info: str = Depends(http.token)):

    """删除应用分组"""

    try:
        for id in ids.split(','):
            db.execute(sys_app_group.delete().where(sys_app_group.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollbackl()
        return http.respond(500, False, '删除失败')

    return http.respond(200, True, '创建成功')

@router.get(path='/app/index', summary='获取应用列表', tags=['应用模块'])
def app_index(
        page: Optional[int] = 0,
        pageSize: Optional[int] = 0,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        status: Optional[str] = '',
        app_name: Optional[str] = '',
        app_id: Optional[str] = '',
        _: Optional[int] = 0,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序类型
        status: 应用状态
        app_name: 应用名称
        app_id: 应用ID
        _: 时间戳
        token_info: token 认证

    Returns: app_list 应用列表 -> list

    """

    offset_page = (page - 1) * pageSize

    if any([status, app_name, app_id]):
        app_list = par_type.to_json(db.execute(select(sys_app).where(and_(
            sys_app.c.name.like('%' + name + '%'),
            sys_app.c.status.like('%' + status + '%'),
            sys_app.c.app_id.like('%' + app_id + '%'))).limit(pageSize).offset(offset_page)))
    else:
        app_list = par_type.to_json(db.execute(select(sys_app).limit(pageSize).offset(offset_page)))

    total = db.query(func.count(sys_app.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': app_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)

@router.post(path='/app/save', summary='创建应用', tags=['应用模块'])
async def app_group_save(app: admin.App, token_info: str = Depends(http.token)):

    """创建应用"""

    app = dict(app)
    app['created_at'] = now_date_time
    app['created_by'] = now_timestamp

    db.execute(insert(sys_app).values(**app))
    db.commit()

    return http.respond(status=200)

@router.get(path='/app/getAppId', summary='获取应用AppID', tags=['应用模块'])
async def get_app_id(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: app_id 应用AppID -> str

    """

    results = {'app_id': base_code.app_id}

    return http.respond(status=200, data=results)


@router.get(path='/app/getAppSecret', summary='获取应用AppSecret', tags=['应用模块'])
async def get_app_id(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns:  app_secret 获取应用AppSecret -> str

    """

    results = {'app_secret': base_code.app_secret}

    return http.respond(status=200, data=results)

@router.delete(path='/app/delete/{ids:path}', summary='删除应用', tags=['应用模块'])
async def app_delete(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 应用ID
        token_info: token 认证

    Returns: respond

    """

    try:
        for id in ids.split(','):
            db.execute(delete(sys_app).where(sys_app.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)

@router.put(path='/app/update/{id:path}', summary='更新应用', tags=['应用模块'])
def app_update(id: int, app: admin.App, token_info: str = Depends(http.token)):

    """

    Args:
        id: 应用ID
        app: 应用信息
        token_info: token 认证

    Returns: respond

    """

    app = dict(app)
    app['updated_at'] = now_date_time
    app['updated_by'] = now_timestamp

    db.execute(update(sys_app).where(sys_app.c.id == id).values(**app))
    db.commit()

    return http.respond(status=200)
