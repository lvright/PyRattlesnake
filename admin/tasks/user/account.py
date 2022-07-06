# -*- coding: utf-8 -*-
from admin import *
from admin.tasks import *


@celery.task
def get_user_info(token_info):
    # 根据返回的 token 解密后获得当前账户 userid 查询 userid 账户信息
    user_info = par_type.to_json(db.execute(select(admin_account).where(
        admin_account.c.id == token_info['id'])).first())
    # 获取当前账户关联菜单权限
    roles_relation = par_type.to_json(db.execute(select(admin_roles_account).where(
        admin_roles_account.c.userId == token_info['id'])).first())
    if user_info and roles_relation:
        # 根据 admin_menu_account 关联表查询菜单
        admin_menu_list = par_type.to_json(db.execute(
            select(admin_system_menu,
                   admin_menu_account).where(admin_system_menu.c.status != '1',
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
                    'icon': items['icon'],
                    'title': items['title'],
                    'type': items['type'],
                    'hidden': bool(int(items['hidden'])),
                    'hiddenBreadcrumb': bool(items['hiddenBreadcrumb']),
                }
                del items['hidden'], items['hiddenBreadcrumb'], items['icon'], items['title'], items['type']
                items['children'] = [menu for menu in admin_menu_list if menu['parent_id'] == items['menu_id']]
                if items['parent_id'] == 0: menu_list.append(items)
            # 查询 backend_setting 系统设置
            user_setting = par_type.to_json(db.execute(select(
                backend_setting).where(backend_setting.c.user_id == token_info['id'])).first())
            del user_info['password']
            user_setting['layoutTags'] = bool(user_setting['layoutTags'])
            user_info['backend_setting'] = user_setting
            return {
                'codes': codes,
                'roles': [token_info['userId']],
                'routers': menu_list,
                'user': user_info
            }
    return False


@celery.task
def user_update_info(user_info, token_info):
    # 在修改账户接口中删除 AdminUpdateInfo model 的 dept_id
    del user_info['dept_id']
    try:
        db.execute(update(admin_account).where(
            admin_account.c.userId == token_info['userId']).values(**user_info))
        db.commit()
    except Exception as e:
        log.error(e)
        return False
    return True


@celery.task
def update_user_password(password, token_info):
    user_password = par_type.to_json(db.execute(
        select(admin_account).where(
               admin_account.c.password == password['oldPassword'])).first())
    if password['newPassword'] == password['newPassword_confirmation']:
        return {'status': 500, 'message': '新密码与确认密码不一致'}
    if user_password:
        try:
            db.execute(update(admin_account).where(
                admin_account.c.userId == token_info['userId']).values(
                password=password['newPassword']))
            db.commit()
        except Exception as e:
            log.error(e)
            return False
        return True
    return {'status': 500, 'message': '旧密码错误'}


@celery.task
def into_user_password(userId, token_info):
    try:
        db.execute(update(admin_account).where(
            admin_account.c.id == userId).values(password='123456'))
        db.commit()
    except Exception as e:
        log.error(str(e))
        return False
    return True


@celery.task
def get_all_user_list(page, pageSize, orderBy, orderType, dept_id, role_id, post_id,
                      username, nickname, phone, email, maxDate, minDate, token_info):
    user_list = []
    offset_page = (page - 1) * pageSize
    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([phone, email, nickname, username]):
        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(
            select(admin_account).where(and_(admin_account.c.username.like('%' + username + '%'),
                                             admin_account.c.nickname.like('%' + nickname + '%'),
                                             admin_account.c.phone.like('%' + phone + '%'),
                                             admin_account.c.email.like('%' + email + '%')))
            .limit(pageSize).offset(offset_page)).all())
        # 更新 data 列表数据
        for item in fuzzy_range_data: user_list.append(item)

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(
            admin_account).where(minDate <= admin_account.c.created_at,
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
    # 根据部门 ID 返回用户
    if dept_id:
        relation = []
        for id in dept_id.split(','):
            user_relation = par_type.to_json(db.execute(select(
                admin_dept_account).where(admin_dept_account.c.deptId == id)).first())
            if user_relation: relation.append(user_relation)
        if relation: user_list = [
            item for item in user_list
            for dept in relation
            if dept['userId'] == item['id']
        ]
    # 根据角色 ID 返回用户
    if role_id:
        relation = []
        for id in role_id.split(','):
            user_relation = par_type.to_json(db.execute(select(
                admin_roles_account).where(admin_roles_account.c.roleId == id)).first())
            if user_relation: relation.append(user_relation)
        if relation: user_list = [
            item for item in user_list
            for role in relation
            if role['roleId'] == item['id']
        ]
    # 根据岗位 ID 返回用户
    if post_id:
        relation = []
        for id in post_id.split(','):
            user_relation = par_type.to_json(db.execute(select(
                admin_post_account).where(admin_post_account.c.postId == id)).first())
            if user_relation: relation.append(user_relation)
        if relation: user_list = [
            item for item in user_list
            for post in relation
            if post['postId'] == item['id']
        ]

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
    return results


@celery.task
def get_dept_user_list(token_info):
    user_dept_list = par_type.to_json(db.execute(select(admin_dept)).all())
    dept_list = []
    # 建立部门树状数据
    if user_dept_list:
        user_dept_list = [
            {
                'id': dept['id'],
                'label': dept['name'],
                'parent_id': dept['parent_id'],
                'value': dept['id']
            } for dept in user_dept_list
        ]
        for items in user_dept_list:
            items['children'] = [dept for dept in user_dept_list if dept['parent_id'] == items['id']]
            if items['parent_id'] == 0: dept_list.append(items)
    return dept_list


@celery.task
def get_role_user_list(token_info):
    return par_type.to_json(db.execute(select(admin_roles)).all())


@celery.task
def get_post_user_list(token_info):
    return par_type.to_json(db.execute(select(admin_post)).all())


@celery.task
def get_user_online_list(page, pageSize, username, orderBy, orderType, token_info):
    online_user_list = data_base.redis.keys()
    online_user_data = []
    if online_user_list:
        for item in online_user_list:
            name = str(item).split(':')[1]
            if username:
                online_user = par_type.to_json(db.execute(select(
                    admin_account).where(admin_account.c.username == name,
                                         admin_account.c.username.like('%' + username + '%'))).first())
            else:
                online_user = par_type.to_json(db.execute(select(
                    admin_account).where(admin_account.c.username == name)).first())
            if online_user:
                user_dept = par_type.to_json(db.execute(select(
                    admin_dept_account).where(admin_dept_account.c.userId == online_user['id'])).first())
                dept = par_type.to_json(db.execute(select(
                    admin_dept).where(admin_dept.c.id == user_dept['deptId'])).first())
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
    return results


@celery.task
def take_user_kick(online_user, token_info):
    user_info = par_type.to_json(db.execute(select(
        admin_account).where(admin_account.c.id == online_user['id']).first()))
    if user_info:
        data_base.redis.delete('user_token:' + user_info['username'])
        return True


@celery.task
def get_user_template(token_info):
    # 模板路径
    template_user_file = project_file_path + '/static/user_file_export/template_user.xls'

    # open 模板文件
    def template_user():
        with open(template_user_file, 'rb') as f: yield from f
    return template_user_file


@celery.task
def user_import_file(file: bytes, token_info):
    # 当前时间戳
    time_now = str(int(time.time()))
    # 导入文件路径
    import_file = project_file_path + '/static/user_file_export/{}.xls'.format(time_now)
    # 保存导入文件
    with open(import_file, 'wb') as f:
        f.write(file)
    # 使用 pandas 读取导入文件
    import_file_pd = pd.read_excel(
        import_file,
        sheet_name='user',
        index_col=0
    )
    # 插入创建时间
    import_file_pd.insert(
        loc=7,
        column='created_by',
        value=now_timestamp
    )
    import_file_pd.insert(
        loc=8,
        column='created_at',
        value=now_date_time
    )
    # 插入默认密码
    import_file_pd.insert(
        loc=9,
        column='password',
        value='123456'
    )
    # 插入默认用户状态 0 表示正常
    import_file_pd.insert(
        loc=10,
        column='status',
        value=0
    )
    try:
        # 使用 pandas sql io 直接为 admin_account 表插入新的用户数据
        pd.io.sql.to_sql(
            import_file_pd,
            'admin_account',
            data_base.engine,
            schema='pysql',
            if_exists='append'
        )
        # 保存提交数据
        data_base.engine.dispose()
    except Exception as e:
        log.error(e)
        return False
    return True


@celery.task
def user_export_file(ids, token_info):
    if ids:
        # 根据 ids 列表循环查询用户数据
        user_list = [item for id in ids for item in par_type.to_json(db.execute(select(
            admin_account).where(admin_account.c.id == id)).all()) if item]
    else:
        # 查询全部
        user_list = par_type.to_json(db.execute(select(admin_account)).all())
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
    return save_file_name + '.xls'


@celery.task
def get_user_data(page, pageSize, orderBy, orderType, dept_id, username,
                  nickname, phone, email, status, maxDate, minDate, token_info):
    user_list = []
    offset_page = (page - 1) * pageSize
    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([phone, email, nickname, username, status]):
        # 按传参条件查询
        fuzzy_range_data = par_type.to_json(db.execute(select(
            admin_account).where(and_(admin_account.c.username.like('%' + username + '%'),
                                      admin_account.c.nickname.like('%' + nickname + '%'),
                                      admin_account.c.phone.like('%' + phone + '%'),
                                      admin_account.c.email.like('%' + email + '%'),
                                      admin_account.c.status.like('%' + status + '%')))
                                                       .limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        if fuzzy_range_data:
            for item in fuzzy_range_data: user_list.append(item)
    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = par_type.to_json(db.execute(select(
            admin_account).where(minDate <= admin_account.c.created_at,
                                 maxDate >= admin_account.c.created_at)
                                                      .limit(pageSize).offset(offset_page)).all())
        # 更新data列表数据
        if time_range_data:
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
        dept_relation = par_type.to_json(db.execute(select(
            admin_dept_account).where(admin_dept_account.c.deptId == int(dept_id))).all())
        if dept_relation:
            user_list = [item for item in user_list for dept in dept_relation if dept['userId'] == item['id']]

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
    return results


@celery.task
def read_user_info(userId, token_info):
    user_info = par_type.to_json(db.execute(select(
        admin_account).where(admin_account.c.id == userId)).first())
    if user_info:
        # 关联查询公共方法 通过关联表查询用户所关联数据
        def get_relation(tabel, data_tabel, ids):
            data_list = []
            relation_list = par_type.to_json(db.execute(select(tabel).where(tabel.c.userId == user_info['id'])).all())
            if relation_list:
                for id in [relation[ids] for relation in relation_list]:
                    ids = par_type.to_json(db.execute(select(data_tabel).where(data_tabel.c.id == id)).all())
                    for item in ids: data_list.append(item)
            return data_list
        # 调用公共查询方法 查出用户所属部门、角色、岗位
        user_info['postList'] = get_relation(admin_post_account, admin_post, 'postId')
        user_info['roleList'] = get_relation(admin_roles_account, admin_roles, 'roleId')
        user_info['dept_id'] = get_relation(admin_dept_account, admin_dept, 'deptId')
        # 用户用户绑定的系统设置
        user_info['backend_setting'] = par_type.to_json(db.execute(select(
            backend_setting).where(backend_setting.c.id == userId)).first())
    return user_info


@celery.task
def create_user_data(account, token_info):
    user_info = {
        'username': account['username'],
        'status': account['status'],
        'phone': account['phone'],
        'nickname': account['nickname'],
        'email': account['email'],
        'password': '123456',
        'dashboard': account['dashboard'],
        'created_at': now_date_time,
        'created_by': now_timestamp,
        'remark': account['remark'],
        'avatar': account['avatar']
    }
    # 插入添加数据
    user_id = db.execute(insert(admin_account).values(**user_info)).lastrowid
    db.commit()

    # 插入数据公共方法关联表 用户关联部门、角色、岗位
    def set_relation(tabel, ids, id_name):
        try:
            for id in account[ids]:
                db.execute(insert(tabel).values(
                    **{id_name: id, 'userId': user_id}))
                db.commit()
        except Exception as e:
            log.error(e)
            db.rollback()
    # 调用插入公共方法 插入关联表
    set_relation(admin_dept_account, 'dept_id', 'deptId')
    set_relation(admin_roles_account, 'role_ids', 'roleId')
    set_relation(admin_post_account, 'post_ids', 'postId')
    return True


@celery.task
def delete_user_data(userId, token_token):
    # 删除指定用户
    try:
        for id in userId.split(','):
            db.execute(delete(admin_account).where(admin_account.c.id == id))
            for tabel in [admin_post_account, admin_dept_account, admin_roles_account]:
                db.execute(delete(tabel).where(tabel.c.userId == id))
    except Exception as e:
        # 报错时生成日志并回滚
        log.error(e)
        db.rollback()
        return False
    return True


@celery.task
def update_user_data(id, account, token_info):
    # 更新数据公共方法关联表 用户关联部门、角色、岗位
    def update_user_relation(tabel, ids, id_name):
        try:
            db.execute(delete(tabel).where(tabel.c.userId == id))
            for up_id in account[ids]:
                db.execute(tabel.insert().values(
                    **{id_name: up_id, 'userId': id}))
                db.commit()
        except Exception as e:
            log.error(e)
            db.rollback()
    update_user_relation(admin_dept_account, 'dept_id', 'deptId')
    update_user_relation(admin_roles_account, 'role_ids', 'roleId')
    update_user_relation(admin_post_account, 'post_ids', 'postId')
    # 过滤用户表以外的参数
    del account['dept_id'], account['role_ids'], account['post_ids']
    # 添加更新时间
    account['updated_at'] = now_date_time
    account['updated_by'] = now_timestamp
    # 更新用户
    db.execute(update(admin_account).where(admin_account.c.id == account['id']).values(**account))
    db.commit()
    return True


@celery.task
def change_user_status(id, status, token_info):
    try:
        db.execute(update(admin_account).where(
            admin_account.c.id == id).values(status=status))
        db.commit()
    except Exception as e:
        log.error(e)
        return False
    return True


@celery.task
def set_home_view(id, dashboard, token_info):
    try:
        db.execute(update(admin_account).where(
            admin_account.c.id == id).values(dashboard=dashboard))
        db.commit()
    except Exception as e:
        log.error(e)
        return False
    return True
