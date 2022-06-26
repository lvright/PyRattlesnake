# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  岗位管理模块
#  ---

@router.get(path='/post/postList', summary='获取岗位列表', tags=['岗位管理'])
async def get_post_list(_: int = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: post_list 部门列表 -> list

    """

    post_list = par_type.to_json(db.execute(select(admin_post)).all())

    return http.respond(status=200, data=post_list)


@router.get(path='/post/postIndex', summary='获取岗位分页列表', tags=['岗位管理'])
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

    """

    Args:
        page:  当前页
        pageSize: 分页数
        code: 岗位编码
        status: 岗位状态
        maxDate: 最大实际
        minDate: 最小时间
        orderBy: 排序
        orderType: 排序规则
        _: 时间戳
        token_info: token 认证

    Returns: posts_list 岗位列表 -> list

    """

    posts_list = []

    offset_page = (page - 1) * pageSize

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([code, status]):

        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(admin_post).where(and_(
            admin_post.c.code.like('%' + code + '%'),
            admin_post.c.status.like('%' + status + '%'))).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in fuzzy_range_data: posts_list.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([minDate, maxDate]):
        time_range_data = par_type.to_json(db.execute(select(admin_post).where(
            minDate <= admin_post.c.created_at,
            maxDate >= admin_post.c.created_at).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in time_range_data: posts_list.append(item)

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        posts_list = par_type.to_json(db.execute(select(
            admin_post).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all())
    elif orderType == 'ascending':
        posts_list = par_type.to_json(db.execute(select(
            admin_post).order_by(orderBy).limit(pageSize).offset(offset_page)).all())
    # 如果没有查询条件则按分页查询
    else:
        posts_list = par_type.to_json(db.execute(select(
            admin_post).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(admin_post.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': posts_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=posts_list)


@router.post(path='/post/postSave', summary='新增岗位', tags=['岗位管理'])
def post_save(post: admin.Post, token_info: str = Depends(http.token)):

    """

    Args:
        post: 岗位信息
        token_info: token 认证

    Returns: respond

    """

    post = dict(post)
    post['created_at'] = now_date_time
    post['created_by'] = now_timestamp

    db.execute(insert(admin_post).values(**post))
    db.commit()

    return http.respond(status=200)


@router.put(path='/post/postUpdate/{id:path}', summary='修改岗位', tags=['岗位管理'])
def post_save(id: int, post: admin.Post, token_info: str = Depends(http.token)):

    """

    Args:
        id: 岗位ID
        post: 岗位信息
        token_info: token 认证

    Returns: respond

    """

    post = dict(post)
    post['updated_at'] = now_date_time
    post['updated_by'] = now_timestamp

    db.execute(update(admin_post).where(admin_post.c.id == id).values(**post))
    db.commit()

    return http.respond(status=200)


@router.delete(path='/post/postDelete/{postId:path}', summary='删除岗位', tags=['岗位管理'])
def post_save(postId: str, token_info: str = Depends(http.token)):

    """

    Args:
        postId: 岗位ID
        token_info: token 认证

    Returns: respond

    """

    # 删除指定用户
    try:
        for user_id in postId.split(','):
            db.execute(delete(admin_post).where(admin_post.c.id == user_id))
            # 删除关联表
            db.execute(delete(admin_post_account).where(admin_post_account.c.postId == user_id))
            db.commit()
    except Exception as e:
        # 报错时生成日志并回滚
        log.error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)
