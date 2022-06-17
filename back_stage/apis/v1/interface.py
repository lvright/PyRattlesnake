# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------系统Api管理----------

@router.get(path='/apiGroup/index', summary='系统api分组列表')
def apis_group_index(
        page: Optional[int] = 0,
        pageSize: Optional[int] = 0,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        status: Optional[str] = '',
        name: Optional[str] = '',
        _: Optional[int] = 0,
        token_info: str = Depends(http.token)
):

    """系统api分组列表"""

    if any([status, name]):
        apis_list = [
            dict(item) for item in db.query(sys_apis_group).where(
                sys_apis_group.c.name.like('%' + name + '%'),
                sys_apis_group.c.status.like('%' + status + '%')
            ).limit(pageSize).offset((page - 1) * pageSize) if item
        ]
    else:
        apis_list = [
            dict(item) for item in db.query(sys_apis_group)
            .limit(pageSize).offset((page - 1) * pageSize) if item
        ]

    total = db.query(func.count(sys_oper_log.c.id)).scalar()

    return http.respond(200, True, '请求成功', {
        'items': apis_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': math.ceil(total / pageSize)
        }
    })

@router.post(path='/apis/apiGroup/save', summary='创建api分组')
async def api_group_save(api_group: admin.ApiGroup, token_info: str = Depends(http.token)):

    """创建api分组"""

    api_group = dict(api_group)

    api_group['created_at'] = now_date_time
    api_group['created_by'] = now_timestamp

    db.execute(sys_apis_group.insert().values(**api_group))
    db.commit()

    return http.respond(200, True, '创建成功')

@router.put(path='/apis/apiGroup/update/{id:path}', summary='更新api分组')
async def app_group_save(id: int, api_group: admin.AppGroup, token_info: str = Depends(http.token)):

    """更新api分组"""

    api_group = dict(api_group)

    api_group['updated_at'] = now_date_time
    api_group['updated_by'] = now_timestamp

    db.execute(sys_apis_group.update().where(sys_apis_group.c.id == id).values(**api_group))
    db.commit()

    return http.respond(200, True, '创建成功')

@router.delete(path='/apis/apiGroup/delete/{ids:path}', summary='删除api分组')
async def app_group_save(ids: str, token_info: str = Depends(http.token)):

    """删除api分组"""

    try:
        for id in ids.split(','):
            db.execute(sys_apis_group.delete().where(sys_apis_group.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollbackl()
        return http.respond(500, False, '删除失败')

    return http.respond(200, True, '创建成功')

@router.get(path='/api/index', summary='系统api列表')
def apis_column_index(
        page: Optional[int] = 0,
        pageSize: Optional[int] = 0,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        status: Optional[str] = '',
        name: Optional[str] = '',
        _: Optional[int] = 0,
        token_info: str = Depends(http.token)
):

    """系统api分组列表"""

    if any([status, name]):
        apis_list = [
            dict(item) for item in db.query(sys_apis).where(
                sys_apis.c.name.like('%' + name + '%'),
                sys_apis.c.status.like('%' + status + '%')
            ).limit(pageSize).offset((page - 1) * pageSize) if item
        ]
    else:
        apis_list = [
            dict(item) for item in db.query(sys_apis)
            .limit(pageSize).offset((page - 1) * pageSize) if item
        ]

    total = db.query(func.count(sys_oper_log.c.id)).scalar()

    return http.respond(200, True, '请求成功', {
        'items': apis_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': math.ceil(total / pageSize)
        }
    })
