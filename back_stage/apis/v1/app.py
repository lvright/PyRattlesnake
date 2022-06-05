# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------应用管理----------

@router.get(path='/app/appGroup/index', summary='应用分组')
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

    """应用分组"""

    if any([status, name]):
        app_group_list = [
            dict(item) for item in db.query(sys_app_group).where(
                sys_app_group.c.name.like('%' + name + '%'),
                sys_app_group.c.status.like('%' + status + '%')
            ).limit(pageSize).all() if item
        ]
    else:
        app_group_list = [
            dict(item) for item in db.query(sys_app_group).limit(pageSize).all() if item
        ]

    return http.respond(200, True, '请求成功', {
        'items': app_group_list,
        'pageInfo': {
            'total': len(app_group_list),
            'currentPage': pageSize,
            'totalPage': pageSize
        }
    })


@router.get(path='/app/appGroup/list', summary='获取应用分组列表')
async def app_list(token_info: str = Depends(http.token)):

    """获取应用分组列表"""

    app_group_list = [
        {
            'name': dict(item)['name'],
            'id': dict(item)['id']
        } for item in db.query(sys_app_group).all() if item
    ]

    return http.respond(200, True, '获取成功', app_group_list)

@router.post(path='/app/appGroup/save', summary='创建应用分组')
async def app_group_save(app_group: admin.AppGroup, token_info: str = Depends(http.token)):

    """创建应用分组"""

    app_group = dict(app_group)

    app_group['created_at'] = now_date_time
    app_group['created_by'] = now_timestamp

    db.execute(sys_app_group.insert().values(**app_group))
    db.commit()

    return http.respond(200, True, '创建成功')

@router.put(path='/app/appGroup/update/{id:path}', summary='更新应用分组')
async def app_group_save(id: int, app_group: admin.AppGroup, token_info: str = Depends(http.token)):

    """更新应用分组"""

    app_group = dict(app_group)

    app_group['updated_at'] = now_date_time
    app_group['updated_by'] = now_timestamp

    db.execute(sys_app_group.update().where(sys_app_group.c.id == id).values(**app_group))
    db.commit()

    return http.respond(200, True, '创建成功')


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

@router.get(path='/app/index', summary='获取应用列表')
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

    """获取应用列表"""

    if any([status, app_name, app_id]):
        app_list = [
            dict(item) for item in db.query(sys_app).where(
                sys_app.c.name.like('%' + name + '%'),
                sys_app.c.status.like('%' + status + '%'),
                sys_app.c.app_id.like('%' + app_id + '%')
            ).limit(pageSize).all() if item
        ]
    else:
        app_list = [
            dict(item) for item in db.query(sys_app).limit(pageSize).all() if item
        ]

    return http.respond(200, True, '获取成功', {
        'items': app_list,
        'pageInfo': {
            'total': len(app_list),
            'currentPage': pageSize,
            'totalPage': pageSize
        }
    })

@router.post(path='/app/save', summary='创建应用')
async def app_group_save(app: admin.App, token_info: str = Depends(http.token)):

    """创建应用"""

    app = dict(app)

    app['created_at'] = now_date_time
    app['created_by'] = now_timestamp

    db.execute(sys_app.insert().values(**app))
    db.commit()

    return http.respond(200, True, '创建成功')

@router.get(path='/app/getAppId', summary='获取应用AppID')
async def get_app_id(token_info: str = Depends(http.token)):

    """获取应用AppID"""

    return http.respond(200, True, '获取成功', {'app_id': base_code.app_id})


@router.get(path='/app/getAppSecret', summary='获取应用AppSecret')
async def get_app_id(token_info: str = Depends(http.token)):

    """获取应用AppSecret"""

    return http.respond(200, True, '获取成功', {'app_secret': base_code.app_secret})

@router.delete(path='/app/delete/{ids:path}', summary='删除应用')
async def app_delete(ids: str, token_info: str = Depends(http.token)):

    """删除应用"""

    try:
        for id in ids:
            db.execute(sys_app.delete().where(sys_app.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollback()
        return http.respond(500, False, '删除失败')

    return http.respond(200, True, '删除成功')

@router.put(path='/app/update/{id:path}', summary='更新应用')
def app_update(id: int, app: admin.App, token_info: str = Depends(http.token)):

    """更新应用"""

    app = dict(app)

    app['updated_at'] = now_date_time
    app['updated_by'] = now_timestamp

    db.execute(sys_app.update().where(sys_app.c.id == id).values(**app))
    db.commit()

    return http.respond(200, True, '更新成功')
