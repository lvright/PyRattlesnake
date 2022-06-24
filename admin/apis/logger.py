# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ----------
#  系统日志
#  ----------

@router.get(path='/logs/getLoginLogPageList', summary='获取登录日志', tags=['系统日志'])
async def login_log(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        username: Optional[str] = '',
        ip: Optional[str] = '',
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
        orderType: 培训规则
        username: 用户名称
        ip: 登录IP
        status: 登录状态
        maxDate: 最大时间
        minDate: 最小时间
        _: 时间戳
        token_info: token 认证

    Returns: login_logs 登录日志列表 -> list

    """

    login_logs = []

    offset_page = (page - 1) * pageSize

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([username, ip]):
        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(sys_login_log).where(
            sys_login_log.c.username.like('%' + username + '%'),
            sys_login_log.c.ip.like('%' + ip + '%')).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in fuzzy_range_data: login_logs.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(sys_login_log).where(
            minDate <= sys_login_log.c.created_at,
            maxDate >= sys_login_log.c.created_at).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in time_range_data: login_logs.append(item)

    elif status:
        status_range_data = par_type.to_json(db.execute(select(sys_login_log).where(
            sys_login_log.c.status == status).limit(pageSize)).all())
        # 更新data列表数据
        for item in status_range_data: login_logs.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        login_logs = par_type.to_json(db.execute(select(
            sys_login_log).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all())
    elif orderType == 'ascending':
        login_logs = par_type.to_json(db.execute(select(
            sys_login_log).order_by(orderBy).limit(pageSize).offset(offset_page)).all())

    # 如果没有查询条件则按分页查询
    else:
        login_logs = par_type.to_json(db.execute(select(
            sys_login_log).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(sys_login_log.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': login_logs,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.delete(path='/logs/loginLog/delete/{ids:path}', summary='删除登录日志', tags=['系统日志'])
async def login_logs_delete(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 日志ID
        token_info: token 认证

    Returns: respond

    """

    try:
        for id in ids.split(','):
            db.execute(delete(sys_login_log).where(sys_login_log.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)


@router.get(path='/logs/getOperLogPageList', summary='获取操作日志', tags=['系统日志'])
async def oper_logs(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        username: Optional[str] = '',
        ip: Optional[str] = '',
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
        orderType: 排序桂香斋
        username: 用户名
        ip: 访问IP
        maxDate: 最大时间
        minDate: 最小时间
        _: 时间戳
        token_info: token 认证

    Returns: oper_logs 操作日志列表 -> list

    """

    oper_logs = []

    offset_page = (page - 1) * pageSize

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([username, ip]):
        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(sys_oper_log).where(
            sys_oper_log.c.username.like('%' + username + '%'),
            sys_oper_log.c.ip.like('%' + ip + '%')).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in fuzzy_range_data: oper_logs.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(sys_oper_log).where(
            minDate <= sys_oper_log.c.created_at,
            maxDate >= sys_oper_log.c.created_at).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in time_range_data: oper_logs.append(item)

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        oper_logs = par_type.to_json(db.execute(select(
            sys_oper_log).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all())
    elif orderType == 'ascending':
        oper_logs = par_type.to_json(db.execute(select(
            sys_oper_log).order_by(orderBy).limit(pageSize).offset(offset_page)).all())

    # 如果没有查询条件则按分页查询
    else:
        oper_logs = par_type.to_json(db.execute(select(
            sys_oper_log).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(sys_oper_log.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': oper_logs,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)