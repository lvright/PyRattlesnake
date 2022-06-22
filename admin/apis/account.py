# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  用户账户模块
#  ---

@router.post(path='/info', summary='获取账号信息', tags=['用户'])
async def get_info(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证
    Returns:
        codes: 权限功能
        roles: 角色名称
        routers: 路由
        user: 当前登录用户信息
    """

    # 根据返回的 token 解密后获得当前账户 userid 查询 userid 账户信息
    user_info = par_type.to_json(db.execute(
        select(admin_account).where(admin_account.c.id == token_info['id'])).first())

    # 获取当前账户关联菜单权限
    roles_relation = par_type.to_json(db.execute(
        select(admin_roles_account).where(admin_roles_account.c.userId == token_info['id'])).first())

    if user_info and roles_relation:
        # 根据 admin_menu_account 关联表查询菜单
        admin_menu_list = par_type.to_json(db.execute(
            select(admin_system_menu, admin_menu_account).where(admin_system_menu.c.status != '1',
                                                                admin_menu_account.c.role_id == roles_relation['roleId'],
                                                                admin_system_menu.c.id == admin_menu_account.c.menu_id)).all())
        # 处理返回的路由结构
        if admin_menu_list:
            menu_list = []
            codes = []

            for items in admin_menu_list:
                # superAdmin 拥有所有权限
                if token_info['username'] == 'superAdmin': codes = ['*'] or codes.append(items['title'])
                items['meta'] = {
                    'hidden': bool(int(items['hidden'])), 'hiddenBreadcrumb': bool(items['hiddenBreadcrumb']),
                    'icon': items['icon'], 'title': items['title'], 'type': items['type']
                }
                del items['hidden'], items['hiddenBreadcrumb'], items['icon'], items['title'], items['type']
                items['children'] = [menu for menu in admin_menu_list if menu['parent_id'] == items['menu_id']]
                if items['parent_id'] == 0: menu_list.append(items)

            # 插入 backend_setting 系统设置
            user_setting = par_type.to_json(db.execute(
                select(backend_setting).where(backend_setting.c.user_id == token_info['id'])).first())

            del user_info['password']
            user_setting['layoutTags'] = bool(user_setting['layoutTags'])
            user_info['backend_setting'] = user_setting

            return http.respond(status=200, data={
                'codes': codes, 'roles': [token_info['userId']],
                'routers': menu_list, 'user': user_info
            })

    return http.respond(status=500)


@router.post(path='/user/updateInfo', summary='修改账号信息')
async def admin_edit_info(edit_info: admin.AdminUpdateInfo, token_info: str = Depends(http.token)):
    """修改账号信息"""

    # 格式化
    edit_data = dict(edit_info)
    # 在修改账户接口中删除 AdminUpdateInfo model 的 dept_id
    del edit_data['dept_id']

    db.execute(update(admin_account).where(
        admin_account.c.userId == token_info['userId']).values(**edit_data))
    db.commit()

    return http.respond(status=200)


@router.post(path='/user/modifyPassword', summary='修改账户密码')
async def modify_password(password: admin.ModifyPassword, token_info: str = Depends(http.token)):

    """

    Args:
        password: 修改密码传参
        token_info: token 认证
    Returns:

    """

    db.execute(update(admin_account).where(
        admin_account.c.userId == token_info['userId']).values(password=password.newPassword))
    db.commit()

    return http.respond(status=200)


@router.put(path='/user/initUserPassword/{userId:path}', summary='初始化账户密码', tags=['用户'])
async def init_password(userId: int, token_info: str = Depends(http.token)):

    """

    Args:
        userId: 用户 id
        token_info: token 认证

    Returns:

    """

    db.execute(admin_account.update().where(
        admin_account.c.id == userId).values(password='123456'))
    db.commit()

    return http.respond(status=200)


@router.get(path='/user/getUserList', summary='按条件获取用户', tags=['用户'])
async def get_user_list(
        # 列表筛选条件
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        dept_id: Optional[str] = '',
        role_id: Optional[str] = '',
        post_id: Optional[str] = '',
        username: Optional[str] = '',
        nickname: Optional[str] = '',
        phone: Optional[str] = '',
        email: Optional[str] = '',
        maxDate: Optional[str] = '',
        minDate: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页面
        pageSize: 分页页数
        orderBy: 排序
        orderType: 排序类型
        dept_id: 部门ID
        role_id: 角色ID
        post_id: 岗位ID
        username: 用户名
        nickname: 用户昵称
        phone: 用户手机号
        email: 用户邮箱
        maxDate: 最大时间
        minDate: 最小时间
        _: 时间戳
        token_info: token 认证

    Returns: user_list 用户 -> list

    """

    user_list = []
    offset_page = (page - 1) * pageSize

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([phone, email, nickname, username]):
        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(admin_account).where(and_(
            admin_account.c.username.like('%' + username + '%'),
            admin_account.c.nickname.like('%' + nickname + '%'),
            admin_account.c.phone.like('%' + phone + '%'),
            admin_account.c.email.like('%' + email + '%'))).limit(pageSize).offset(offset_page)))
        # 更新 data 列表数据
        for item in fuzzy_range_data: user_list.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(admin_account).where(
            minDate <= admin_account.c.created_at, maxDate >= admin_account.c.created_at).limit(pageSize).offset(offset_page)))
        # 更新data列表数据
        for item in time_range_data: user_list.append(item)

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        user_list = par_type.to_json(db.execute(select(
            admin_account).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)))
    elif orderType == 'ascending':
        user_list = par_type.to_json(db.execute(select(
            admin_account).order_by(orderBy).limit(pageSize).offset(offset_page)))

    # 如果没有查询条件则按分页查询
    else:
        user_list = par_type.to_json(db.execute(select(
            admin_account).limit(pageSize).offset(offset_page)))

    # 根据部门 ID 返回用户
    if dept_id:
        dept_relation = [item for id in dept_id.split(',') for item in par_type.to_json(db.execute(select(
            admin_dept_account).where(admin_dept_account.c.deptId == id).all()))]
        user_list = [item for item in user_list for dept in dept_relation if dept['userId'] == item['id']]
    # 根据角色 ID 返回用户
    if role_id:
        role_relation = [item for id in role_id.split(',') for item in par_type.to_json(db.execute(select(
            admin_roles_account).where(admin_roles_account.c.roleId == id).all()))]
        user_list = [item for item in user_list for role in role_relation if role['userId'] == item['id']]
    # 根据岗位 ID 返回用户
    if post_id:
        post_relation = [item for id in post_id.split(',') for item in par_type.to_json(db.execute(select(
            admin_post_account).where(admin_post_account.c.postId == id)).all())]
        user_list = [item for item in user_list for post in post_relation if post['userId'] == item['id']]

    total = db.query(func.count(admin_post_account.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': user_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.get(path='/user/getDeptTreeList', summary='按部门获取用户', tags=['用户'])
async def get_user_list(_: int = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: dept_list 部门 -> list

    """

    user_dept_list = par_type.to_json(db.execute(select(admin_dept).all()))

    dept_list = []
    # 建立部门树状数据
    if user_dept_list:
        user_dept_list = [{'id': dept['id'], 'label': dept['name'],
                           'parent_id': dept['parent_id'], 'value': dept['id']} for dept in user_dept_list]
        for items in user_dept_list:
            items['children'] = [dept for dept in user_dept_list if dept['parent_id'] == items['id']]
            if items['parent_id'] == 0: dept_list.append(items)

    return http.respond(status=200, data=dept_list)


@router.get(path='/user/getRoleList', summary='按角色获取用户', tags=['用户'])
async def get_role_list(_: int = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 验证

    Returns: roles 角色 -> list

    """

    roles = par_type.to_json(db.execute(select(admin_roles).all()))

    return http.respond(status=200, data=roles)


@router.get(path='/user/getPostList', summary='按岗位获取用户', tags=['用户'])
async def get_post_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: posts 岗位 -> list

    """

    posts = par_type.to_json(db.execute(select(admin_post).all()))

    return http.respond(status=200, data=posts)


@router.get(path='/user/onlineUser/index', summary='获取在线用户', tags=['用户'])
def user_online(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 访问页数
        orderBy: 排序
        orderType: 排序类型
        _:
        token_info: token 认证

    Returns: user_data 在线用户 -> list

    """

    online_user_list = data_base.redis.keys()

    online_user_data = []
    if online_user_list:
        for item in online_user_list:
            username = str(item).split(':')[1]
            online_user = par_type.to_json(db.execute(select(
                admin_account).where(admin_account.c.username == username).first()))
            if online_user:
                user_dept = par_type.to_json(db.execute(select(admin_dept_account).where(
                    admin_dept_account.c.userId == online_user['id']).first()))
                dept = par_type.to_json(db.execute(select(admin_dept).where(admin_dept.c.id == user_dept['deptId']).first()))
                online_user['dept'] = dept['name']
                online_user_data.append(online_user)

    user_data = online_user_data[page - 1:page + pageSize]
    total = len(online_user_data)
    total_page = math.ceil(len(online_user_data) / pageSize)

    results = {
        'items': user_data,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.post(path='/user/onlineUser/kick', summary='强退用户', tags=['用户'])
def user_kick(online_user: admin.OnlineUser, token_info: str = Depends(http.token)):

    """

    Args:
        online_user: 在线用户
        token_info: token 认证

    Returns: respond

    """

    online_user = dict(online_user)

    user = par_type.to_json(db.execute(select(admin_account).where(
        admin_account.c.id == online_user['id']).first()))
    if user:
        user_name = user['username']
        data_base.redis.delete('user_token:' + user_name)

        return http.respond(status=200)