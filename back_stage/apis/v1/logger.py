# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------系统日志模块----------

@router.get(path='/logs/getLoginLogPageList', summary='获取登录日志')
def login_log(
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

    """获取登录日志"""

    login_logs = []

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([username, ip]):

        # 按传参条件查询
        fuzzy_range_data = db.query(sys_login_log).filter(
            sys_login_log.c.username.like('%' + username + '%'),
            sys_login_log.c.ip.like('%' + ip + '%')
        ).limit(pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            login_logs.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = db.query(sys_login_log).filter(
            minDate <= sys_login_log.c.created_at,
            maxDate >= sys_login_log.c.created_at
        ).limit(pageSize)

        # 更新data列表数据
        for item in time_range_data:
            login_logs.append(dict(item))

    elif status:
        status_range_data = db.query(sys_login_log).filter(
            sys_login_log.c.status == status,
        ).limit(pageSize)

        # 更新data列表数据
        for item in status_range_data:
            login_logs.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        login_logs = [dict(logs) for logs in db.query(sys_login_log).order_by(desc(orderBy)).limit(pageSize) if logs]

    elif orderType == 'ascending':
        login_logs = [dict(logs) for logs in db.query(sys_login_log).order_by(orderBy).limit(pageSize) if logs]

    # 如果没有查询条件则按分页查询
    else:
        login_logs = [dict(logs) for logs in db.query(sys_login_log).limit(pageSize) if logs]

    return http.respond(200, True, 'OK', {
        'items': login_logs,
        'pageInfo': {
            'total': len(login_logs),
            'currentPage': page,
            'totalPage': math.ceil(len(login_logs) / pageSize)
        }
    })

@router.delete(path='/logs/loginLog/delete/{ids:path}', summary='删除登录日志')
def login_logs_delete(ids: str, token_info: str = Depends(http.token)):

    """删除登录日志"""

    try:
        for id in ids.split(','):
            db.execute(sys_login_log.delete().where(sys_login_log.c.id == id))
            db.commit()
    except Exception as e:
        log.log_error(e)
        db.rollback()

        return http.respond(500, False, '删除失败')

    return http.respond(200, True, '删除成功')

@router.get(path='/logs/getOperLogPageList', summary='获取操作日志')
def oper_logs(
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

    """获取操作日志"""

    pass
