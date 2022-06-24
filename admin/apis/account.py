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


@router.post(path='/user/updateInfo', summary='修改账号信息', tags=['用户'])
async def admin_edit_info(user_info: admin.AdminUpdateInfo, token_info: str = Depends(http.token)):

    """

    Args:
        user_info: 用户信息
        token_info: token 认证

    Returns:

    """

    # 格式化
    user_info = dict(user_info)
    # 在修改账户接口中删除 AdminUpdateInfo model 的 dept_id
    del user_info['dept_id']

    db.execute(update(admin_account).where(
        admin_account.c.userId == token_info['userId']).values(**user_info))
    db.commit()

    return http.respond(status=200)


@router.post(path='/user/modifyPassword', summary='修改账户密码', tags=['用户'])
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
            minDate <= admin_account.c.created_at,
            maxDate >= admin_account.c.created_at).limit(pageSize).offset(offset_page)))
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
        dept_relation = [item for id in dept_id.split(',')
                         for item in par_type.to_json(db.execute(select(
                         admin_dept_account).where(admin_dept_account.c.deptId == id).all()))]

        user_list = [item for item in user_list
                     for dept in dept_relation
                     if dept['userId'] == item['id']]

    # 根据角色 ID 返回用户
    if role_id:
        role_relation = [item for id in role_id.split(',')
                         for item in par_type.to_json(db.execute(select(
                         admin_roles_account).where(admin_roles_account.c.roleId == id).all()))]

        user_list = [item for item in user_list
                     for role in role_relation
                     if role['userId'] == item['id']]

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
                admin_account).where(admin_account.c.username == username)).first())

            if online_user:
                user_dept = par_type.to_json(db.execute(select(admin_dept_account).where(
                    admin_dept_account.c.userId == online_user['id'])).first())

                dept = par_type.to_json(db.execute(select(admin_dept).where(
                    admin_dept.c.id == user_dept['deptId'])).first())

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
async def user_kick(online_user: admin.OnlineUser, token_info: str = Depends(http.token)):
    """

    Args:
        online_user: 在线用户
        token_info: token 认证

    Returns: respond

    """

    online_user = dict(online_user)
    user_info = par_type.to_json(db.execute(select(admin_account).where(
        admin_account.c.id == online_user['id']).first()))
    if user:
        data_base.redis.delete('user_token:' + user_info['username'])

        return http.respond(status=200)


@router.post(path='/user/clearCache', summary='更新账户缓存', tags=['用户'])
async def role_clear_cache():
    """

    Returns: respond

    """

    return http.respond(status=200)


@router.post(path='/user/downloadTemplate', summary='下载导入模板', tags=['用户'])
def user_download_template(token_info: str = Depends(http.token)):
    # 模板路径
    template_user_file = project_file_path + '/static/user_file_export/template_user.xls'

    # open 模板文件
    def template_user():
        with open(template_user_file, 'rb') as f:
            yield from f

    # 返回模板文件流
    response = FileResponse(
        status_code=200,
        path=template_user_file
    )

    return response


@router.post(path='/user/import', summary='导入用户数据', tags=['用户'])
async def user_import(file: bytes = File(...), token_info: str = Depends(http.token)):
    # 当前时间戳
    time_now = str(int(time.time()))

    # 导入文件路径
    import_file = project_file_path + '/static/user_file_export/{}.xls'.format(time_now)

    # 保存导入文件
    with open(import_file, 'wb') as f:
        f.write(file)

    # 使用 pandas 读取导入文件
    import_file_pd = pd.read_excel(import_file,
                                   sheet_name='user',
                                   index_col=0)
    # 插入创建时间
    import_file_pd.insert(loc=7,
                          column='created_by',
                          value=str(now_timestamp))
    import_file_pd.insert(loc=8,
                          column='created_at',
                          value=now_date_time)
    # 插入默认密码
    import_file_pd.insert(loc=9,
                          column='password',
                          value='123456')
    # 插入默认用户状态 0 表示正常
    import_file_pd.insert(loc=10,
                          column='status',
                          value=0)

    try:
        # 使用 pandas sql io 直接为 admin_account 表插入新的用户数据
        await pd.io.sql.to_sql(
            import_file_pd,
            'admin_account',
            data_base.engine,
            schema='pysql',
            if_exists='append'
        )
        # 保存提交数据
        data_base.engine.dispose()
    except Exception as e:
        log.log_error(e)
        return http.respond(status=500)

    return http.respond(status=200)


@router.post(path='/role/userExport', summary='导出用户', tags=['用户'])
async def user_export(ids: Any = Body(...), token_info: str = Depends(http.token)):
    """

    Args:
        ids: 用户ID
        token_info: token 认证

    Returns: FileResponse 文件流 -> bytes

    """

    if ids:
        # 根据 ids 列表循环查询用户数据
        user_list = [item for _id in ids for item in par_type.to_json(db.execute(select(
            admin_account).where(admin_account.c.id == _id).all())) if item]
    else:
        # 查询全部
        user_list = par_type.to_json(db.execute(select(admin_account).all()))

    data = []
    # 格式化数据
    for item in user_list:
        set = [item[k] for k in item]
        data.append(set)

    # pandas 模块转化 excel .xls格式
    user_pd_frame = pd.DataFrame(data=data, columns=[str(k) for k in user_list[0].keys()])

    # 生成 excel
    wb = Workbook()
    ws = wb.active
    ws.title = 'user'

    # 循环数据
    for i in dataframe_to_rows(user_pd_frame): ws.append(i)

    # 使用当前时间戳命名文件
    time_now = str(int(time.time()))

    # 文件存储路径
    save_file_name = project_file_path + '/static/user_file_export/' + time_now

    # 保存文件
    wb.save(save_file_name + '.xls')

    # fastapi FileResponse 返回文件流
    results = FileResponse(
        status_code=200,
        path=save_file_name + '.xls',
    )

    return results


@router.get(path='/user/pageIndex', summary='获取用户列表', tags=['用户'])
async def get_user_list(
        # 列表筛选条件
        page: int,
        pageSize: int,
        orderBy: Optional[str] = None,
        orderType: Optional[str] = None,
        dept_id: Optional[str] = '',
        username: Optional[str] = '',
        nickname: Optional[str] = '',
        phone: Optional[str] = '',
        email: Optional[str] = '',
        status: Optional[str] = '',
        maxDate: Optional[str] = '',
        minDate: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):
    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序类型
        dept_id: 岗位ID
        username: 用户名称
        nickname: 用户昵称
        phone: 手机号
        email: 用户邮箱
        status: 用户状态
        maxDate: 最大时间
        minDate: 最小时间
        _: 时间戳
        token_info: token 认证

    Returns: user_list 用户列表 -> list

    """

    user_list = []
    offset_page = (page - 1) * pageSize

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([phone, email, nickname, username, status]):

        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(admin_account).where(and_(
            admin_account.c.username.like('%' + username + '%'), admin_account.c.nickname.like('%' + nickname + '%'),
            admin_account.c.phone.like('%' + phone + '%'), admin_account.c.email.like('%' + email + '%'),
            admin_account.c.status.like('%' + status + '%'))).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in fuzzy_range_data: user_list.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(admin_account).where(
            minDate <= admin_account.c.created_at,
            maxDate >= admin_account.c.created_at).limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        for item in time_range_data: user_list.append(item)

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        user_list = par_type.to_json(db.execute(select(
            admin_account).order_by(desc(orderBy)).limit(pageSize).offset(offset_page)).all())

    elif orderType == 'ascending':
        user_list = par_type.to_json(db.execute(select(
            admin_account).order_by(orderBy).limit(pageSize).offset(offset_page)).all())
    # 如果没有查询条件则按分页查询
    else:
        user_list = par_type.to_json(db.execute(select(
            admin_account).limit(pageSize).offset(offset_page)).all())

    # 根据部门ID 返回用户
    if dept_id:
        dept_relation = [item for id in dept_id.split(',')
                         for item in par_type.to_json(db.execute(select(
                         admin_dept_account).where(admin_dept_account.c.deptId == id)).all())]

        user_list = [item for item in user_list
                     for dept in dept_relation
                     if dept['userId'] == item['id']]

    total = db.query(func.count(admin_dept_account.c.id)).scalar()
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


@router.get(path='/user/userRead/{userId:path}', summary='查看账户信息', tags=['用户'])
async def read_user(userId: int, token_info: str = Depends(http.token)):
    """

    Args:
        userId: 用户ID
        token_info: token 认证

    Returns: user_info 用户列表 -> list

    """

    user_info = par_type.to_json(db.execute(select(
        admin_account).where(admin_account.c.id == userId).first()))

    if user_info:

        # 关联查询公共方法 通过关联表查询用户所关联数据
        def get_relation(relation_tabel, data_tabel, ids):
            relation_list = par_type.to_json(db.execute(select(
                relation_tabel).where(relation_tabel.c.userId == user_info['id']).all()))

            data_list = []
            if relation_list:
                for id in [relation[ids] for relation in relation_list]:
                    ids = db.execute(select(data_tabel).where(data_tabel.c.id == id).all())
                    for item in ids: data_list.append(item)

            return data_list

        # 调用公共查询方法 查出用户所属部门、角色、岗位
        user_info['postList'] = get_relation(admin_post_account, admin_post, 'postId')
        user_info['roleList'] = get_relation(admin_roles_account, admin_roles, 'roleId')
        user_info['dept_id'] = get_relation(admin_dept_account, admin_dept, 'deptId')

        # 用户用户绑定的系统设置
        user_info['backend_setting'] = par_type.to_json(db.execute(select(
            backend_setting).where(backend_setting.c.id == 1).first()))

    return http.respond(status=200, data=user_info)


@router.post(path='/user/userSave', summary='添加用户', tags=['用户'])
async def create_user(account: admin.User, token_info: str = Depends(http.token)):
    """

    Args:
        account: 用户信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化参数
    acc = dict(account)
    # 过滤用户表以外的参数
    del acc['dept_id'], acc['role_ids'], acc['post_ids']

    # 添加创建时间
    acc['created_at'] = now_date_time
    acc['created_by'] = now_timestamp

    # 插入添加数据
    user_id = db.execute(insert(admin_account).values(**acc)).lastrowid
    db.commit()

    user_info = par_type.to_json(account)

    # 插入数据公共方法关联表 用户关联部门、角色、岗位
    def set_relation(tabel, ids, id_name):
        for id in user_info[ids]:
            db.execute(insert(tabel).values(**{id_name: id, 'userId': user_id}))
            db.commit()

    # 调用插入公共方法 插入关联表
    if user_info['dept_id']:
        set_relation(admin_dept_account, 'dept_id', 'deptId')
    if user_info['role_ids']:
        set_relation(admin_roles_account, 'role_ids', 'roleId')
    if user_info['post_ids']:
        set_relation(admin_post_account, 'post_ids', 'postId')

    return http.respond(status=200)


@router.delete(path='/user/userDelete/{userId:path}', summary='删除用户', tags=['用户'])
async def delete_user(userId: str, token_token: str = Depends(http.token)):
    """

    Args:
        userId: 用户ID
        token_token: token 认证

    Returns: respond

    """

    # 删除指定用户
    try:
        for id in userId.split(','):
            db.execute(delete(admin_account).where(admin_account.c.id == id))
            # 删除关联表
            db.execute(delete(admin_post_account).where(admin_post_account.c.userId == id))
            db.execute(delete(admin_dept_account).where(admin_dept_account.c.userId == id))
            db.execute(delete(admin_roles_account).where(admin_roles_account.c.userId == id))
            db.commit()
    except Exception as e:
        # 报错时生成日志并回滚
        log.log_error(e)
        db.rollback()
        return http.respond(status=500)

    return http.respond(status=200)


@router.put(path='/role/userUpdate/{id:path}', summary='编辑用户', tags=['用户'])
async def update_user(id: int, account: admin.User, token_info: str = Depends(http.token)):
    """

    Args:
        id: 用户ID
        account: 用户信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化 Models 参数
    acc = dict(account)
    # 过滤用户表以外的参数
    del acc['dept_id'], acc['role_ids'], acc['post_ids']

    # 添加更新时间
    acc['updated_at'] = now_date_time
    acc['updated_by'] = now_timestamp

    # 更新数据
    db.execute(update(admin_account).where(admin_account.c.id == acc['id']).values(acc))

    user_info = par_type.to_json(account)

    # 更新数据公共方法关联表 用户关联部门、角色、岗位
    def up_relation(tabel, ids, id_name):
        try:
            # 先删除用户关联表中所有关联数据
            db.execute(tabel.delete().where(tabel.c.userId == id))
            # 再重新插入新的关联数据
            for user_id in user_info[ids]:
                db.execute(tabel.insert().values(**{id_name: user_id, 'userId': id}))
                db.commit()
        except Exception as e:
            # 错误回滚 日志打印
            log.log_error(e)
            db.rollback()
            return http.respond(status=500)

    # 调用更新数据公共方法
    if user_info['dept_id']:
        up_relation(admin_dept_account, 'dept_ids', 'deptId')
    if user_info['role_ids']:
        up_relation(admin_roles_account, 'role_ids', 'roleId')
    if user_info['post_ids']:
        up_relation(admin_post_account, 'post_ids', 'postId')

    return http.respond(status=200)


@router.put(path='/role/changeStatus', summary='更改用户状态', tags=['用户'])
async def change_status(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):
    """

    Args:
        id: 用户ID
        status: 用户状态
        token_info: token 认证

    Returns: respond

    """

    db.execute(update(admin_account).where(admin_account.c.id == id).values(status=status))
    db.commit()

    return http.respond(status=200)


@router.post(path='/role/setHomePage', summary='设置用户登录首页', tags=['用户'])
def set_home_page(
        id: int = Body(...),
        dashboard: str = Body(...),
        token_info: str = Depends(http.token)
):
    """

    Args:
        id: 用户ID
        dashboard: 用户首页参数
        token_info: token 认证

    Returns: respond

    """

    db.execute(update(admin_account).where(admin_account.c.id == id).values(dashboard=dashboard))
    db.commit()

    return http.respond(status=200)