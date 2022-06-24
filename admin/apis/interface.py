# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  API管理
#  ----

@router.get(path='/apiGroup/index', summary='系统api分组列表', tags=['Api应用管理'])
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

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序规则
        status: 分组状态
        name: 分组名称
        _: 时间戳
        token_info: token 认证

    Returns: apis_group_list api分组列表 -> list

    """

    offset_page = (page - 1) * pageSize

    if any([status, name]):
        apis_group_list = par_type.to_json(db.execute(select(sys_apis_group).where(
            sys_apis_group.c.name.like('%' + name + '%'),
            sys_apis_group.c.status.like('%' + status + '%')).limit(pageSize).offset(offset_page)).all())
    else:
        apis_group_list = par_type.to_json(db.execute(select(
            sys_apis_group).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(sys_apis_group.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': apis_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.post(path='/apis/apiGroup/save', summary='创建api分组', tags=['Api应用管理'])
async def api_group_save(api_group: admin.ApiGroup, token_info: str = Depends(http.token)):

    """

    Args:
        api_group: api 分组信息
        token_info: token 认证

    Returns: respond

    """

    api_group = dict(api_group)
    api_group['created_at'] = now_date_time
    api_group['created_by'] = now_timestamp

    db.execute(insert(sys_apis_group).values(**api_group))
    db.commit()

    return http.respond(status=200)


@router.put(path='/apis/apiGroup/update/{id:path}', summary='更新api分组', tags=['Api应用管理'])
async def app_group_save(id: int, api_group: admin.AppGroup, token_info: str = Depends(http.token)):

    """

    Args:
        id: api id
        api_group: api分组信息
        token_info: token 认证

    Returns: respond

    """

    api_group = dict(api_group)
    api_group['updated_at'] = now_date_time
    api_group['updated_by'] = now_timestamp

    db.execute(update(sys_apis_group).where(sys_apis_group.c.id == id).values(**api_group))
    db.commit()

    return http.respond(status=200)


@router.delete(path='/apis/apiGroup/delete/{ids:path}', summary='删除api分组', tags=['Api应用管理'])
async def app_group_save(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 分组ID
        token_info: token 认证

    Returns: respond

    """

    try:
        for id in ids.split(','):
            db.execute(delete(sys_apis_group).where(sys_apis_group.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollbackl()
        return http.respond(status=500)

    return http.respond(status=200)


@router.get(path='/api/index', summary='系统api列表', tags=['Api应用管理'])
def apis_column_index(
        page: Optional[int] = 0,
        pageSize: Optional[int] = 0,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        status: Optional[str] = '',
        name: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序规则
        status: 应用状态
        name: 应用名称
        _: 时间戳
        token_info: token 认证

    Returns: apis_list api 列表 -> list

    """

    offset_page = (page - 1) * pageSize

    if any([status, name]):
        apis_list = par_type.to_json(db.execute(select(sys_apis).where(
            sys_apis.c.name.like('%' + name + '%'),
            sys_apis.c.status.like('%' + status + '%')).limit(pageSize).offset(offset_page)).all())
    else:
        apis_list = par_type.to_json(db.execute(select(
            sys_apis).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(sys_apis.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': apis_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)
