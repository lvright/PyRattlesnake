# -*- coding: utf-8 -*-
import json

from back_stage import *

@router.websocket(path='/message.io')
async def message_io(token: str, websocket: WebSocket):

    """ WebSocket 系统消息"""

    token_info = jwt_token.decode(token)

    mess = db.query(sys_message).where(
        and_(
            sys_message.c.click_num == 0,
            sys_message.c.users.like('%' + str(token_info['id']) + '%')
        )
    ).all()

    mess = [dict(item) for item in mess if item]

    db.flush()

    data = {'event': 'ev_new_message', 'message': '你有一条新的消息', 'data': mess}
    data = json.dumps(data, indent=2)

    print('返回消息：', data)

    await manager.connect(websocket)
    await manager.broadcast(data)

    try:
        while True:
            get_mess = await websocket.receive_text()
            print('接收心跳:' + get_mess)
            await manager.send_personal_message(data, websocket)
            await manager.broadcast(data)

    except WebSocketDisconnect as e:
        log.log_error(e)
        manager.disconnect(websocket)
        await manager.broadcast('账户登出')

@router.get(path='/user/notice/index', summary='获取系统通知')
async def get_notice(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        type: Optional[str] = '',
        title: Optional[str] = '',
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """获取系统通知"""

    notice_list = []

    if any([type, title]):
        notice = db.query(sys_message).where(
            and_(
                sys_message.c.title.like('%' + title + '%'),
                sys_message.c.type.like('%' + type + '%')
            )
        ).limit(pageSize).all()

        notice_list = [dict(item) for item in notice if item]

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        notice_list = [dict(item) for item in db.query(sys_message).order_by(desc(orderBy)).limit(pageSize) if item]

    elif orderType == 'ascending':
        notice_list = [dict(item) for item in db.query(sys_message).order_by(orderBy).limit(pageSize) if item]

    else:
        notice_list = [dict(item) for item in db.query(sys_message).limit(pageSize).all() if item]

    return http.respond(200, True, 'OK', {
        'items': notice_list,
        'pageInfo': {
            'total': len(notice_list),
            'currentPage': page,
            'totalPage': math.ceil(len(notice_list) / pageSize)
        }
    })

@router.post(path='/notice/save', summary='发送通知')
async def notice_save(notice: admin.SystemNotification, token_info: str = Depends(http.token)):

    """发送通知"""

    notice = dict(notice)

    notice['created_at'] = now_date_time
    notice['created_by'] = now_timestamp

    if notice.users is not None:
        for user_id in notice['users']:
            notice['users'] = str(user_id)
            db.execute(sys_message.insert().values(**notice))
            db.commit()
    else:
        users = [dict(item)['id'] for item in db.query(admin_account).all() if item]
        for user_id in users:
            db.execute(sys_message.insert().values(**notice))
            db.commit()

    return http.respond(200, True, '发送成功')

@router.put(path='/notice/update/{id:path}', summary='编辑通知')
async def notice_save(id: int, notice: admin.SystemNotification, token_info: str = Depends(http.token)):

    """发送通知"""

    notice = dict(notice)

    del notice['users']

    notice['updated_at'] = now_date_time
    notice['updated_by'] = now_timestamp

    db.execute(sys_message.update().where(sys_message.c.id == id).values(**notice))
    db.commit()

    return http.respond(200, True, '发送成功')

@router.delete(path='/notice/delete/{ids:path}', summary='删除消息')
async def delete_dept(ids: str, token_info: str = Depends(http.token)):

    """删除消息"""

    try:
        for id in ids.split(','):
            db.execute(sys_message.delete().where(sys_message.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.log_error(e)
        db.rollback()

    return http.respond(200, True, '已删除')

@router.get(path='/queueMessage/sendList', summary='获取已发送信息')
async def send_message_list(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """获取已发送信息"""

    if orderType == 'descending':

        send_message = [
            dict(item) for item in db.query(sys_message).where(
                sys_message.c.send_by == token_info['id']
            ).order_by(desc(orderBy)).limit(pageSize).all() if item
        ]

    elif orderType == 'ascending':

        send_message = [
            dict(item) for item in db.query(sys_message).where(
                sys_message.c.send_by == token_info['id']
            ).order_by(orderBy).limit(pageSize).all() if item
        ]

    else:

        send_message = [
            dict(item) for item in db.query(sys_message).where(
                sys_message.c.send_by == token_info['id']
            ).limit(pageSize).all() if item
        ]

    return http.respond(200, True, '获取成功', send_message)

@router.get(path='/queueMessage/readMessage/{id:path}', summary='获取消息详情')
async def read_status_update(id: int, token_infi: str = Depends(http.token)):

    """获取消息详情"""

    read_message = db.query(sys_message).where(sys_message.c.id == id).first()

    if read_message:

        read_message = dict(read_message)

        db.execute(sys_message.update().where(sys_message.c.id == id).values(
            **{
                'click_num': read_message['click_num'] + 1,
                'read_status': 1,
            }
        ))
        db.commit()

    return http.respond(200, True, '获取成功', dict(read_message))

@router.delete(path='/queueMessage/delete/{ids:path}', summary='删除消息')
async def message_delete(ids: str, token_info: str = Depends(http.token)):

    """删除消息"""

    try:
        for id in ids.split(','):
            db.execute(sys_message.delete().where(sys_message.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.log_error(e)
        db.rollback()

    return http.respond(200, True, '已删除')

@router.get(path='/queueMessage/getReceiveUser', summary='获取消息接收人')
async def read_status_update(
        page: int,
        pageSize: int,
        id: Optional[int] = 0,
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """获取消息详情"""

    user_message = db.query(sys_message).where(sys_message.c.id == id).all()

    users = []

    for user_id in dict(user_message)['users'].split(','):
        users = db.query(admin_account).where(admin_account.c.id == user_id).limit(pageSize).all()

    users = [dict(item) for item in users if item]

    return http.respond(200, True, '获取成功', users)

@router.get(path='/queueMessage/receiveList', summary='获取接收信息')
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

    """获取接收信息"""

    receive_message = []

    # 定义 orderBy 参数
    orderBy = orderBy.split('.')[0] or 'created_at'

    # orderBy 方法
    def message_order_by(where_sql, order_by_sql):

        """

        Args:
            where_sql: where 条件 sql
            order_by_sql:  升降序 desc

        Returns: message_list

        """

        if orderType == 'descending':

            message_data = db.query(sys_message).where(where_sql)\
                .order_by(desc(order_by_sql)).limit(pageSize).all()

        elif orderType == 'ascending':

            message_data = db.query(sys_message).where(where_sql)\
                .order_by(order_by_sql).limit(pageSize).all()

        else:

            message_data = db.query(sys_message).where(where_sql)\
                .limit(pageSize).all()

        message_list = [dict(item) for item in message_data if item]

        return message_list

    if any([content_type, read_status]):

        if read_status == 'all':

            receive_message = message_order_by(
                and_(
                    sys_message.c.content_type.like('%' + content_type + '%'),
                    sys_message.c.send_by == token_info['id']
                ), orderBy
            )

        else:

            receive_message = message_order_by(
                and_(
                    sys_message.c.content_type.like('%' + content_type + '%'),
                    sys_message.c.read_status.like('%' + read_status + '%'),
                    sys_message.c.send_by == token_info['id']
                ), orderBy
            )

    else:

        receive_message = [
            dict(item) for item in db.query(sys_message).where(
                sys_message.c.send_by == token_info['id']
            ).limit(pageSize).all() if item
        ]

    if receive_message:
        for item in receive_message:
            item['send_user'] = {'nickname': item['send_user']}

    return http.respond(200, True, '获取成功', receive_message)

@router.post(path='/queueMessage/sendPrivateMessage', summary='发送通知')
async def notice_save(message: admin.SystemMessage, token_info: str = Depends(http.token)):

    """发送通知"""

    message = dict(message)

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
            db.execute(sys_message.insert().values(**message))
            db.commit()
    else:
        users = [dict(item)['id'] for item in db.query(admin_account).all() if item]
        for user_id in users:
            db.execute(sys_message.insert().values(**message))
            db.commit()

    return http.respond(200, True, '发送成功')