# -*- coding: utf-8 -*-

from admin import *

# TODO ----------岗位管理模块----------

@router.get(path='/post/postList', summary='获取岗位列表')
async def get_post_list(_: int = None, token_info: str = Depends(http.token)):

    """获取岗位列表"""

    post_list = [dict(post) for post in db.query(admin_post).all() if post]

    return http.respond(200, True, 'OK', post_list)

@router.get(path='/post/postIndex', summary='获取岗位分页列表')
async def get_post_list(
        page: int,
        pageSize: int,
        code: Optional[str] = '',
        status: Optional[str] = '',
        maxDate: Optional[str] = '',
        minDate: Optional[str] = '',
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """获取岗位分页列表"""

    posts_list = []

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([code, status]):

        # 按传参条件查询
        fuzzy_range_data = db.query(admin_post).filter(
            and_(
                admin_post.c.code.like('%' + code + '%'),
                admin_post.c.status.like('%' + status + '%'),
            ),
        ).limit(pageSize).offset((page - 1) * pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            posts_list.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([minDate, maxDate]):
        time_range_data = db.query(admin_post).filter(
            minDate <= admin_post.c.created_at,
            maxDate >= admin_post.c.created_at
        ).limit(pageSize).offset((page - 1) * pageSize)

        # 更新data列表数据
        for item in time_range_data:
            posts_list.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        posts_list = [
            dict(post) for post in db.query(admin_post).order_by(desc(orderBy))
            .limit(pageSize).offset((page - 1) * pageSize) if post
        ]

    elif orderType == 'ascending':
        posts_list = [
            dict(post) for post in db.query(admin_post).order_by(orderBy)
            .limit(pageSize).offset((page - 1) * pageSize) if post
        ]

    # 如果没有查询条件则按分页查询
    else:
        posts_list = [
            dict(post) for post in db.query(admin_post)
            .limit(pageSize).offset((page - 1) * pageSize) if post
        ]

    total = db.query(func.count(admin_post.c.id)).scalar()

    return http.respond(200, True, 'OK', {
        'items': posts_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': int(total / pageSize)
        }
    })

@router.post(path='/post/postSave', summary='新增岗位')
def post_save(post: admin.Post, token_info: str = Depends(http.token)):

    """新增岗位"""

    post = dict(post)

    post['created_at'] = now_date_time
    post['created_by'] = now_timestamp

    db.execute(admin_post.insert().values(**post))
    db.commit()

    return http.respond(200, True, '新增成功')

@router.put(path='/post/postUpdate/{id:path}', summary='修改岗位')
def post_save(id: int, post: admin.Post, token_info: str = Depends(http.token)):

    """修改岗位"""

    post = dict(post)

    post['updated_at'] = now_date_time
    post['updated_by'] = now_timestamp

    db.execute(admin_post.update().where(admin_post.c.id == id).values(**post))
    db.commit()

    return http.respond(200, True, '保存成功')

@router.delete(path='/post/postDelete/{postId:path}', summary='删除岗位')
def post_save(postId: str, token_info: str = Depends(http.token)):

    """删除岗位"""

    # 删除指定用户
    try:
        for user_id in postId.split(','):
            db.execute(admin_post.delete().where(admin_post.c.id == int(user_id)))
            # 删除关联表
            db.execute(admin_post_account.delete().where(admin_post_account.c.postId == user_id))
            db.commit()
    except Exception as e:
        # 报错时生成日志并回滚
        log.log_error(e)
        db.rollback()
        return http.respond(500, False, str(e))

    return http.respond(200, True, '已删除')
