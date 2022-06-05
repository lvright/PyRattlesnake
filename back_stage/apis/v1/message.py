# -*- coding: utf-8 -*-

from back_stage import *

@router.websocket(path='/message.io?token={token:path}')
async def message_io(websocket: WebSocket, token: str):

    await manager.connect(websocket)
    await manager.broadcast('OK')

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)

    except WebSocketDisconnect as e:
        log.log_error(e)
        manager.disconnect(websocket)
        await manager.broadcast(f'用户离开')

@router.get(path='/user/notice/index', summary='获取系统通知')
def get_notice(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
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
            'totalPage': page
        }
    })

@router.post(path='/notice/save', summary='发送通知')
def notice_save(notice: admin.Notice, token_info: str = Depends(http.token)):

    """发送通知"""

    if notice.users is not None:

        notice = dict(notice)

        notice['created_at'] = now_date_time
        notice['created_by'] = now_timestamp

        for user_id in notice['users']:

            notice['users'] = str(user_id)

            db.execute(sys_message.insert().values(**notice))
            db.commit()

        return http.respond(200, True, '发送成功')

    return http.respond(500, False, '请选择发送的用户')

@router.put(path='/notice/update/{id:path}', summary='编辑通知')
def notice_save(id: int, notice: admin.Notice, token_info: str = Depends(http.token)):

    """发送通知"""

    notice = dict(notice)

    del notice['users']

    notice['updated_at'] = now_date_time
    notice['updated_by'] = now_timestamp

    db.execute(sys_message.update().where(sys_message.c.id == id).values(**notice))
    db.commit()

    return http.respond(200, True, '发送成功')


@router.delete(path='/notice/delete/{ids:path}', summary='删除部门')
async def delete_dept(ids: str, token_info: str = Depends(http.token)):

    """删除部门"""

    try:
        for id in ids.split(','):
            db.execute(sys_message.delete().where(sys_message.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚 日志打印
        log.log_error(e)
        db.rollback()

    return http.respond(200, True, '已删除')