# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------用户账户模块----------

@router.post(path='/info', summary='获取账号信息')
async def admin_info(token_info: str = Depends(http.token)):

    """获取账号信息"""

    # 根据返回的 token 解密后获得当前账户 userid 查询 userid 账户信息
    admin_info = db.query(admin_account).filter_by(userId=token_info['userId']).first()

    if admin_info:
        admin_info = dict(admin_info)

        # 根据 admin_role_relation 关联表查询菜单
        admin_menu_list = [
            dict(menu) for menu in db.query(admin_system_menu, admin_menu_account).filter(
                admin_menu_account.c.role_id == admin_info['id'],
                admin_system_menu.c.id == admin_menu_account.c.menu_id
            ).all()
        ]

        # 处理返回的路由结构
        if admin_menu_list:
            menu_list = []
            for items in admin_menu_list:
                items['meta'] = {
                    'hidden': bool(int(items['hidden'])),
                    'hiddenBreadcrumb': bool(items['hiddenBreadcrumb']),
                    'icon': items['icon'],
                    'title': items['title'],
                    'type': items['type']
                }
                del items['hidden'], items['hiddenBreadcrumb'], items['icon'], items['title'], items['type']

                # 过滤停用状态菜单
                if items['status'] == '0':
                    items['children'] = [
                        menu for menu in admin_menu_list
                        if menu['parent_id'] == items['menu_id']
                        # 过滤停用状态菜单
                        if menu['status'] == '0'
                    ]

                    if items['parent_id'] == 0: menu_list.append(items)

            # 获取系统配置
            back_setting = db.query(backend_setting).filter_by(user_id=token_info['id']).first()

            # 插入 backend_setting 系统设置
            admin_info['backend_setting'] = dict(back_setting)

            return http.respond(200, True, '加载完成', {
                'codes': ['*'],
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
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
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
                admin_account.c.email.like('%' + email + '%'),
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
            'totalPage': page
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
async def get_role_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """按角色获取用户"""

    roles = [dict(role) for role in db.query(admin_roles).all() if role]

    return http.respond(200, True, 'OK', roles)

@router.get(path='/user/getPostList', summary='按岗位获取用户')
async def get_post_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """按岗位获取用户"""

    post_list = [dict(post) for post in db.query(admin_post).all() if post]

    return http.respond(200, True, 'OK', post_list)