# -*- coding: utf-8 -*-

from back_stage import *

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
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
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
        ).limit(pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            posts_list.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([minDate, maxDate]):
        time_range_data = db.query(admin_post).filter(
            minDate <= admin_post.c.created_at,
            maxDate >= admin_post.c.created_at
        ).all()

        # 更新data列表数据
        for item in time_range_data:
            posts_list.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        posts_list = [dict(post) for post in db.query(admin_post).order_by(desc(orderBy)).limit(pageSize) if post]

    elif orderType == 'ascending':
        posts_list = [dict(post) for post in db.query(admin_post).order_by(orderBy).limit(pageSize) if post]

    # 如果没有查询条件则按分页查询
    else:
        posts_list = [dict(post) for post in db.query(admin_post).limit(pageSize).all() if post]

    return http.respond(200, True, 'OK', {
        'items': posts_list,
        'pageInfo': {
            'total': len(posts_list),
            'currentPage': page,
            'totalPage': page
        }
    })

@router.post(path='/post/postSave', summary='新增岗位')
def post_save(token_info: str = Depends(http.token)):

    """新增岗位"""

    return http.respond(200, True, '新增成功')
