# -*- coding: utf-8 -*-

from admin import *
from admin.tasks.message.sysmsg import *


# TODO
#  ---
#  系统消息
#  ---

@router.websocket(path='/message.io')
async def message_io(token: str, websocket: WebSocket):

    """
    WebSocket
    """

    token_info = jwt_token.decode(token)
    mess = par_type.to_json(db.execute(select(
        sys_message).where(sys_message.c.click_num == 0,
                           sys_message.c.users.like('%' + str(token_info['id']) + '%'))).all())
    db.flush()
    data = {'event': 'ev_new_message', 'message': '你有一条新的消息', 'data': mess or []}
    data = json.dumps(data, indent=2)
    log.info(f'callback service data：{data}')
    await manager.connect(websocket)
    await manager.broadcast(data)
    try:
        while True:
            get_mess = await websocket.receive_text()
            await manager.send_personal_message(data, websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect as e:
        log.error(e)
        manager.disconnect(websocket)
        await manager.broadcast('账户登出')


@router.get(path='/notice/index', summary='获取系统通知', tags=['系统消息'])
async def get_notice(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        type: Optional[str] = '',
        title: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序规则
        type: 消息类型
        title: 消息标题
        _: 时间戳
        token_info: token 认证

    Returns: notice_list 消息列表 -> list

    """

    notice_list = []
    offset_page = (page - 1) * pageSize

    if any([type, title]):
        notice = par_type.to_json(
            db.execute(select(sys_notification).where(
                and_(
                    sys_notification.c.title.like('%' + title + '%'),
                    sys_notification.c.type.like('%' + type + '%')
                )
            ).limit(pageSize).offset(offset_page)).all()
        )

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        notice_list = par_type.to_json(
            db.execute(select(sys_notification).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all()
        )
    elif orderType == 'ascending':
        notice_list = par_type.to_json(
            db.execute(select(sys_notification).order_by(orderBy).limit(pageSize).offset(offset_page)).all()
        )
    else:
        notice_list = par_type.to_json(
            db.execute(select(sys_notification).limit(pageSize).offset(offset_page)).all()
        )

    total = db.query(func.count(sys_notification.c.id)).scalar()
    total_page = math.ceil(total / pageSize)
    results = {
        'items': notice_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.post(path='/notice/save', summary='发送通知', tags=['系统消息'])
async def notice_save(notice: admin.SystemNotification, token_info: str = Depends(http.token)):

    """

    Args:
        notice: 消息信息
        token_info: token 认证

    Returns: respond

    """

    notice = dict(notice)
    notice['created_at'] = now_date_time
    notice['created_by'] = now_timestamp

    if notice.users is not None:
        for user_id in notice['users']:
            notice['users'] = str(user_id)
            db.execute(insert(sys_message).values(**notice))
            db.commit()
    else:
        users = par_type.to_json(db.execute(select(admin_account)).all())
        for user_id in users:
            db.execute(insert(sys_message).values(**notice))
            db.commit()

    return http.respond(status=200)


@router.put(path='/notice/update/{id:path}', summary='编辑通知', tags=['系统消息'])
async def notice_save(id: int, notice: admin.SystemNotification, token_info: str = Depends(http.token)):

    """

    Args:
        id: 通知ID
        notice: 通知信息
        token_info: token 认证

    Returns: respond

    """

    notice = dict(notice)
    del notice['users']
    notice['updated_at'] = now_date_time
    notice['updated_by'] = now_timestamp

    db.execute(update(sys_notification).where(sys_notification.c.id == id).values(**notice))
    db.commit()

    return http.respond(status=200)


@router.delete(path='/notice/delete/{ids:path}', summary='删除消息', tags=['系统消息'])
async def delete_dept(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 消息ID
        token_info: token 认证

    Returns: respond

    """

    try:
        for id in ids.split(','):
            db.execute(delete(sys_message).where(sys_message.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)


@router.get(path='/queueMessage/sendList', summary='获取已发送信息', tags=['系统消息'])
async def send_message_list(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序规则
        _: 时间戳
        token_info: token 认证

    Returns: send_message 已发送信息列表 -> list

    """

    if orderType == 'descending':
        send_message = par_type.to_json(db.execute(select(sys_message).where(
            sys_message.c.send_by == token_info['id']).order_by(desc(orderBy)).limit(pageSize)).all())
    elif orderType == 'ascending':
        send_message = par_type.to_json(db.execute(select(sys_message).where(
            sys_message.c.send_by == token_info['id']).order_by(orderBy).limit(pageSize)).all())
    else:
        send_message = par_type.to_json(db.execute(select(sys_message).where(
            sys_message.c.send_by == token_info['id']).limit(pageSize)).all())

    return http.respond(status=200, data=send_message)


@router.get(path='/queueMessage/readMessage/{id:path}', summary='获取消息详情', tags=['系统消息'])
async def read_status_update(id: int, token_info: str = Depends(http.token)):

    """

    Args:
        id: 消息ID
        token_info: token 认证

    Returns: read_message 已读消息 -> dict

    """

    read_message = par_type.to_json(db.execute(select(
        sys_message).where(sys_message.c.id == id)).first())

    if read_message:
        db.execute(update(sys_message).where(sys_message.c.id == id).values(
            **{'click_num': read_message['click_num'] + 1, 'read_status': 1}))
        db.commit()

    return http.respond(status=200, data=read_message)


@router.delete(path='/queueMessage/delete/{ids:path}', summary='删除消息', tags=['系统消息'])
async def message_delete(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 消息ID
        token_info: token 认证

    Returns: respond

    """

    try:
        for id in ids.split(','):
            db.execute(delete(sys_message).where(sys_message.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.error(e)
        db.rollback()
        http.respond(status=500)

    return http.respond(status=200)


@router.get(path='/queueMessage/getReceiveUser', summary='获取消息接收人', tags=['系统消息'])
async def read_status_update(
        page: int,
        pageSize: int,
        id: Optional[int] = 0,
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        id: 消息ID
        _: 时间戳
        token_info: token 认证

    Returns: user_message 用户消息列表 -> list

    """

    user_message = par_type.to_json(db.execute(select(sys_message).where(sys_message.c.id == id)).all())

    user_message_list = []
    for item in user_message:
        for user_id in item['users'].split(','):
            user_message_list = par_type.to_json(db.execute(select(admin_account).where(
                admin_account.c.id == user_id).limit(pageSize)).all())

    return http.respond(status=200, data=user_message_list)


@router.get(path='/queueMessage/receiveList', summary='获取接收信息', tags=['系统消息'])
async def send_message_list(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
        content_type: Optional[str] = '',
        read_status: Optional[str] = '',
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序规则
        content_type: 消息类型
        read_status: 阅读状态
        _: 时间戳
        token_info: token 认证

    Returns: receive_message 接收消息列表 -> list

    """

    receive_message = []

    # 定义 orderBy 参数
    orderBy = orderBy.split('.')[0] or 'created_at'
    offset_page = (page - 1) * pageSize

    # orderBy 方法
    def message_order_by(where_sql):
        if orderType == 'descending':
            message_data = par_type.to_json(db.execute(select(sys_message).where(
                where_sql).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all())
        elif orderType == 'ascending':
            message_data = par_type.to_json(db.execute(select(sys_message).where(
                where_sql).order_by(orderBy).limit(pageSize).offset(offset_page)).all())
        else:
            message_data = par_type.to_json(db.execute(select(sys_message).where(
                where_sql).limit(pageSize).offset(offset_page)).all())
        return message_data

    if any([content_type, read_status]):
        if read_status == 'all':
            receive_message = message_order_by(and_(
                sys_message.c.content_type.like('%' + content_type + '%'),
                sys_message.c.send_by == token_info['id']))
        else:
            receive_message = message_order_by(and_(
                sys_message.c.content_type.like('%' + content_type + '%'),
                sys_message.c.read_status == read_status,
                sys_message.c.send_by == token_info['id']))
    else:
        receive_message = par_type.to_json(db.execute(select(sys_message).where(
            sys_message.c.send_by == token_info['id']).limit(pageSize).offset(offset_page)).all())

    if receive_message:
        for item in receive_message:
            item['send_user'] = {'nickname': item['send_user']}

    return http.respond(status=200, data=receive_message)


@router.post(path='/queueMessage/sendPrivateMessage', summary='发送通知', tags=['系统消息'])
async def notice_save(message: admin.SystemMessage, token_info: str = Depends(http.token)):

    """

    Args:
        message: 消息信息
        token_info: token 认证

    Returns: respond

    """

    message = par_type.to_json(message)
    # 插入消息内容
    message['created_at'] = now_date_time
    message['created_by'] = now_timestamp
    message['send_user'] = token_info['nickname']
    message['send_by'] = token_info['id']
    message['click_num'] = 0

    # 判断 users
    if message['users']:
        for user_id in message['users']:
            message['users'] = str(user_id)
            db.execute(insert(sys_message).values(**message))
            db.commit()
    else:
        users = [item['id'] for item in par_type.to_json(db.execute(select(
            admin_account)).all()) if item]
        for user_id in users:
            db.execute(insert(sys_message).values(**message))
            db.commit()

    return http.respond(status=200)