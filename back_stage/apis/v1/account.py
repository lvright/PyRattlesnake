# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------用户账户模块----------

@router.post(path='/info', summary='获取账号信息')
async def admin_info(token_info: str = Depends(http.token)):

    """获取账号信息"""

    # 根据返回的 token 解密后获得当前账户 userid 查询 userid 账户信息
    admin_info = db.query(admin_account).filter_by(id=token_info['id']).first()

    # 获取当前账户关联菜单权限
    admin_role = db.query(admin_roles_account).filter_by(userId=token_info['id']).first()

    if admin_info:

        admin_info = dict(admin_info)
        admin_role = dict(admin_role)

        # 根据 admin_menu_account 关联表查询菜单
        admin_menu_list = [dict(menu) for menu in db.query(
            admin_system_menu,
            admin_menu_account
        ).where(
            admin_system_menu.c.status != '1').filter(
            admin_menu_account.c.role_id == admin_role['roleId'],
            admin_system_menu.c.id == admin_menu_account.c.menu_id
        ).all()]

        # 处理返回的路由结构
        if admin_menu_list:

            menu_list = []

            codes = []

            for items in admin_menu_list:

                codes.append(items['title'])

                items['meta'] = {
                    'hidden': bool(int(items['hidden'])),
                    'hiddenBreadcrumb': bool(items['hiddenBreadcrumb']),
                    'icon': items['icon'],
                    'title': items['title'],
                    'type': items['type']
                }

                del items['hidden'], items['hiddenBreadcrumb'], items['icon'], items['title'], items['type']

                items['children'] = [menu for menu in admin_menu_list if menu['parent_id'] == items['menu_id']]

                if items['parent_id'] == 0: menu_list.append(items)

            # superAdmin 拥有所有权限
            if token_info['username'] == 'superAdmin': codes = ['*']

            # 插入 backend_setting 系统设置
            user_setting = db.query(backend_setting).filter_by(user_id=token_info['id']).first()

            if user_setting:

                user_setting = dict(user_setting)

                user_setting['layoutTags'] = bool(user_setting['layoutTags'])
                admin_info['backend_setting'] = user_setting

            else:

                # 初始化用户 提供默认配置
                admin_info['backend_setting'] = {
                    'colorPrimary': '#536DFE',
                    'lang': 'zh_CN',
                    'layout': 'header',
                    'layoutTags': '1',
                    'theme': 'default'
                }

            return http.respond(200, True, '加载完成', {
                'codes': codes,
                'roles': [token_info['userId']],
                'routers': menu_list,
                'user': admin_info
            })

    return http.respond(500, False, '获取失败')

@router.post(path='/user/updateInfo', summary='修改账号信息')
async def admin_edit_info(edit_info: admin.AdminUpdateInfo, token_info: str = Depends(http.token)):

    """修改账号信息"""

    # 格式化
    edit_data = dict(edit_info)

    # 在修改账户接口中删除 AdminUpdateInfo model 的 dept_id
    del edit_data['dept_id']

    db.execute(admin_account.update().where(admin_account.c.userId == token_info['userId']).values(**edit_data))
    db.commit()

    return http.respond(200, True, '修改成功')

@router.post(path='/user/modifyPassword', summary='修改账户密码')
async def modify_password(password: admin.ModifyPassword, token_info: str = Depends(http.token)):

    """修改账户密码"""

    db.execute(admin_account.update().where(admin_account.c.userId == token_info['userId']).values(password=password.newPassword))
    db.commit()

    return http.respond(200, True, '密码修改成功')

@router.put(path='/user/initUserPassword/{userId:path}', summary='初始化账户密码')
async def init_password(userId: int, token_info: str = Depends(http.token)):

    """初始化账户密码"""

    db.execute(admin_account.update().where(admin_account.c.id == userId).values(password='123456'))
    db.commit()

    return http.respond(200, True, '已初始化密码')

@router.get(path='/user/getUserList', summary='按条件获取用户')
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

    """获取用户列表"""

    account_list = []

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([phone, email, nickname, username]):

        # 按传参条件查询
        fuzzy_range_data = db.query(admin_account).filter(
            and_(
                admin_account.c.username.like('%' + username + '%'),
                admin_account.c.nickname.like('%' + nickname + '%'),
                admin_account.c.phone.like('%' + phone + '%'),
                admin_account.c.email.like('%' + email + '%')
            ),
        ).limit(pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            account_list.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = db.query(admin_account).filter(
            minDate <= admin_account.c.created_at,
            maxDate >= admin_account.c.created_at
        ).all()

        # 更新data列表数据
        for item in time_range_data:
            account_list.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        account_list = [dict(acc) for acc in db.query(admin_account).order_by(desc(orderBy)).limit(pageSize) if acc]

    elif orderType == 'ascending':
        account_list = [dict(acc) for acc in db.query(admin_account).order_by(orderBy).limit(pageSize) if acc]

    # 如果没有查询条件则按分页查询
    else:
        account_list = [dict(acc) for acc in db.query(admin_account).limit(pageSize) if acc]

    # 根据部门 ID 返回用户
    if dept_id:
        dept_relation = [
            dict(item) for id in dept_id.split(',')
            for item in db.query(admin_dept_account).filter_by(deptId=id).all()
        ]
        account_list = [
            item for item in account_list
            for dept in dept_relation
            if dict(dept)['userId'] == item['id']
        ]

    # 根据角色 ID 返回用户
    if role_id:
        role_relation = [
            dict(item) for id in role_id.split(',')
            for item in db.query(admin_roles_account).filter_by(roleId=id).all()
        ]
        account_list = [
            item for item in account_list
            for role in role_relation
            if dict(role)['userId'] == item['id']
        ]

    # 根据岗位 ID 返回用户
    if post_id:
        post_relation = [
            dict(item) for id in post_id.split(',')
            for item in db.query(admin_post_account).filter_by(postId=id).all()
        ]
        account_list = [
            item for item in account_list
            for post in post_relation
            if dict(post)['userId'] == item['id']
        ]

    return http.respond(200, True, 'OK', {
        'items': account_list,
        'pageInfo': {
            'total': len(account_list),
            'currentPage': page,
            'totalPage': math.ceil(len(account_list) / pageSize)
        }
    })

@router.get(path='/user/getDeptTreeList', summary='按部门获取用户')
async def get_user_list(_: int = None, token_info: str = Depends(http.token)):

    """按部门获取用户"""

    admin_dept_list = db.query(admin_dept).all()

    # 建立部门树状数据

    dept_list = []

    if admin_dept_list:

        admin_dept_list = [dict(item) for item in admin_dept_list if item]

        admin_dept_list = [
            {
                'id': dept['id'],
                'label': dept['name'],
                'parent_id': dept['parent_id'],
                'value': dept['id']
            } for dept in admin_dept_list
        ]
        for items in admin_dept_list:
            items['children'] = [
                dept for dept in admin_dept_list
                if dept['parent_id'] == items['id']
            ]
            if items['parent_id'] == 0: dept_list.append(items)

    return http.respond(200, True, 'OK', dept_list)

@router.get(path='/user/getRoleList', summary='按角色获取用户')
async def get_role_list(_: int = None, token_info: str = Depends(http.token)):

    """按角色获取用户"""

    roles = [dict(role) for role in db.query(admin_roles).all() if role]

    return http.respond(200, True, 'OK', roles)

@router.get(path='/user/getPostList', summary='按岗位获取用户')
async def get_post_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """按岗位获取用户"""

    post_list = [dict(post) for post in db.query(admin_post).all() if post]

    return http.respond(200, True, 'OK', post_list)

@router.get(path='/user/onlineUser/index', summary='获取在线用户')
def user_online(
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """获取在线用户"""

    online_user_list = data_base.redis.keys()

    if online_user_list:

        online_user_data = []

        for item in online_user_list:
            online_user = db.query(admin_account).filter_by(username=item).first()

            user_dept = db.query(admin_dept_account).filter_by(userId=online_user['id']).first()
            dept = db.query(admin_dept).filter_by(id=dict(user_dept)['deptId']).first()

            online_user = dict(online_user)
            online_user['dept'] = dict(dept)['name']

            if online_user: online_user_data.append(dict(online_user))

        return http.respond(200, True, '获取成功', {
            'items': online_user_data,
            'pageInfo': {
                'total': len(online_user_data),
                'currentPage': page,
                'totalPage': math.ceil(len(online_user_data) / pageSize)
            }
        })

@router.post(path='/user/onlineUser/kick', summary='强退用户')
def user_kick(online_user: admin.OnlineUser, token_info: str = Depends(http.token)):

    """强退用户"""

    online_user = dict(online_user)

    user = db.query(admin_account).filter_by(id=online_user['id']).first()

    if user:
        user_name = dict(user)['username']
        data_base.redis.delete(user_name)

        return http.respond(200, True, '强退成功')