# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------用户管理模块----------

@router.post(path='/role/clearCache', summary='更新账户缓存')
async def role_clear_cache():

    """清除账户缓存"""

    return http.respond(200, True, 'OK')

@router.post(path='/role/downloadTemplate', summary='下载导入模板')
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

@router.post(path='/role/import', summary='导入用户数据')
async def user_import(file: bytes = File(...), token_info: str = Depends(http.token)):

    # 当前时间戳
    time_now = str(int(time.time()))

    # 导入文件路径
    import_file = project_file_path + '/static/user_file_export/{}.xls'.format(time_now)

    # 保存导入文件
    with open(import_file, 'wb') as f:
        f.write(file)

    # 使用 pandas 读取导入文件
    import_file_pd = pd.read_excel(import_file, sheet_name='user', index_col=0)

    # 插入创建时间
    import_file_pd.insert(loc=7, column='created_by', value=str(now_timestamp))
    import_file_pd.insert(loc=8, column='created_at', value=now_date_time)

    # 插入默认密码
    import_file_pd.insert(loc=9, column='password', value='123456')

    # 插入默认用户状态 0 表示正常
    import_file_pd.insert(loc=10, column='status', value=0)

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
        return http.respond(500, False, '导入失败，请检查导入文件')

    return http.respond(200, True, '导入成功')

@router.post(path='/role/userExport', summary='导出用户')
async def user_export(ids: Any = Body(...), token_info: str = Depends(http.token)):

    """导出用户表"""

    if ids:
        # 根据 ids 列表循环查询用户数据
        user_list = [dict(item) for _id in ids for item in db.query(admin_account).filter_by(id=_id).all() if item]
    else:

        # 查询全部
        user_list = [dict(item) for item in db.query(admin_account).all() if item]

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
    return FileResponse(
        status_code=200,
        path=save_file_name + '.xls',
    )

@router.get(path='/role/pageIndex', summary='获取用户列表')
async def get_roles_list(
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

    """获取用户列表"""

    account_list = []

    # 筛选式查询 any判断传参有值时 介入查询条件
    if any([phone, email, nickname, username, status]):

        # 按传参条件查询
        fuzzy_range_data = db.query(admin_account).filter(
            and_(
                admin_account.c.username.like('%' + username + '%'),
                admin_account.c.nickname.like('%' + nickname + '%'),
                admin_account.c.phone.like('%' + phone + '%'),
                admin_account.c.email.like('%' + email + '%'),
                admin_account.c.status.like('%' + status + '%')
            ),
        ).limit(pageSize).offset((page - 1) * pageSize)

        # 更新data列表数据
        for item in fuzzy_range_data:
            account_list.append(dict(item))

    # 如果传日期范围则查询日期范围数据
    elif all([maxDate, minDate]):
        time_range_data = db.query(admin_account).filter(
            minDate <= admin_account.c.created_at,
            maxDate >= admin_account.c.created_at
        ).limit(pageSize).offset((page - 1) * pageSize)

        # 更新data列表数据
        for item in time_range_data:
            account_list.append(dict(item))

    # 升降序筛选 根据 orderBy 字段决定筛选的字段，desc 表示升序
    elif orderType == 'descending':
        account_list = [dict(acc) for acc in db.query(admin_account).order_by(desc(orderBy)).limit(pageSize).offset((page - 1) * pageSize) if acc]

    elif orderType == 'ascending':
        account_list = [dict(acc) for acc in db.query(admin_account).order_by(orderBy).limit(pageSize).offset((page - 1) * pageSize) if acc]

    # 如果没有查询条件则按分页查询
    else:
        account_list = [dict(acc) for acc in db.query(admin_account).limit(pageSize).offset((page - 1) * pageSize) if acc]

    # 根据部门ID 返回用户
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

    total = db.query(func.count(sys_oper_log.c.id)).scalar()

    return http.respond(200, True, 'OK', {
        'items': account_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': math.ceil(total / pageSize)
        }
    })

@router.get(path='/role/userRead/{userId:path}', summary='查看账户信息')
async def read_user(userId: int, token_info: str = Depends(http.token)):

    """查询某个用户详情信息"""

    admin_info = db.query(admin_account).filter_by(id=userId).first()

    if admin_info:
        admin_info = dict(admin_info)

        # 关联查询公共方法 通过关联表查询用户所关联数据
        def get_relation_data(relation_tabel, data_tabel, ids):
            relation_list = db.query(relation_tabel).filter_by(userId=admin_info['id']).all()

            data_list = []
            if relation_list:
                for _id in [dict(relation)[ids] for relation in relation_list]:
                    _ids = db.query(data_tabel).filter_by(id=_id).all()
                    for item in _ids: data_list.append(dict(item))
            return data_list

        # 调用公共查询方法 查出用户所属部门、角色、岗位
        admin_info['postList'] = get_relation_data(
            admin_post_account,
            admin_post,
            'postId'
        )
        admin_info['roleList'] = get_relation_data(
            admin_roles_account,
            admin_roles,
            'roleId'
        )
        admin_info['dept_id'] = get_relation_data(
            admin_dept_account,
            admin_dept,
            'deptId'
        )

        # 用户用户绑定的系统设置
        admin_info['backend_setting'] = dict(db.query(backend_setting).filter_by(id=1).first()) or {}

    return http.respond(200, True, 'OK', admin_info)

@router.post(path='/role/userSave', summary='添加账户')
async def create_user(account: admin.User, token_info: str = Depends(http.token)):

    """添加用户"""

    # 格式化参数
    acc = dict(account)

    # 过滤用户表以外的参数
    del acc['dept_id'], acc['role_ids'], acc['post_ids']

    # 添加创建时间
    acc['created_at'] = now_date_time
    acc['created_by'] = now_timestamp

    # 插入添加数据
    user_id = db.execute(admin_account.insert().values(acc)).lastrowid
    db.commit()

    # 插入数据公共方法关联表 用户关联部门、角色、岗位
    def set_relation(tabel, ids, id_name):
        for _id in dict(account)[ids]:
            db.execute(tabel.insert().values({id_name: _id, 'userId': user_id}))
            db.commit()

    # 调用插入公共方法 插入关联表
    if dict(account)['dept_id']:
        set_relation(
            admin_dept_account,
            'dept_id',
            'deptId'
        )
    if dict(account)['role_ids']:
        set_relation(
            admin_roles_account,
            'role_ids',
            'roleId'
        )
    if dict(account)['post_ids']:
        set_relation(
            admin_post_account,
            'post_ids',
            'postId'
        )

    return http.respond(200, True, '创建成功')

@router.delete(path='/role/userDelete/{userId:path}', summary='删除账户')
async def delete_user(userId: str, token_token: str = Depends(http.token)):

    """删除用户"""

    # 删除指定用户
    try:
        for user_id in userId.split(','):
            db.execute(admin_account.delete().where(admin_account.c.id == int(user_id)))
            # 删除关联表
            db.execute(admin_post_account.delete().where(admin_post_account.c.userId == user_id))
            db.execute(admin_dept_account.delete().where(admin_dept_account.c.userId == user_id))
            db.execute(admin_roles_account.delete().where(admin_roles_account.c.userId == user_id))
            db.commit()
    except Exception as e:
        # 报错时生成日志并回滚
        log.log_error(e)
        db.rollback()
        return http.respond(500, False, str(e))

    return http.respond(200, True, '已删除')

@router.put(path='/role/userUpdate/{id:path}', summary='编辑账户')
async def update_user(id: int, account: admin.User, token_info: str = Depends(http.token)):

    """编辑用户"""

    # 格式化 Models 参数
    acc = dict(account)

    # 过滤用户表以外的参数
    del acc['dept_id'], acc['role_ids'], acc['post_ids']

    # 添加更新时间
    acc['updated_at'] = now_date_time
    acc['updated_by'] = now_timestamp

    # 更新数据
    db.execute(admin_account.update().where(admin_account.c.id == acc['id']).values(acc))

    # 更新数据公共方法关联表 用户关联部门、角色、岗位
    def up_relation(tabel, ids, id_name):
        try:
            # 先删除用户关联表中所有关联数据
            db.execute(tabel.delete().where(tabel.c.userId == id))
            # 再重新插入新的关联数据
            for _id in dict(account)[ids]:
                db.execute(tabel.insert().values({id_name: _id, 'userId': id}))
                db.commit()
        except Exception as e:
            # 错误回滚 日志打印
            log.log_error(e)
            db.rollback()
            return http.respond(500, False, str(e))

    # 调用更新数据公共方法
    if dict(account)['dept_id']:
        up_relation(
            admin_dept_account,
            'dept_ids',
            'deptId'
        )
    if dict(account)['role_ids']:
        up_relation(
            admin_roles_account,
            'role_ids',
            'roleId'
        )
    if dict(account)['post_ids']:
        up_relation(
            admin_post_account,
            'post_ids',
            'postId'
        )

    return http.respond(200, True, '编辑成功')

@router.put(path='/role/changeStatus', summary='更改用户状态')
async def change_status(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """修改用户状态"""

    db.execute(admin_account.update().where(admin_account.c.id == id).values(status=status))
    db.commit()

    return http.respond(200, True, '已变更状态')

@router.post(path='/role/setHomePage', summary='设置用户登录首页')
def set_home_page(
        id: int = Body(...),
        dashboard: str = Body(...),
        token_info: str = Depends(http.token)
):

    """设置账户登录首页"""

    db.execute(admin_account.update().where(admin_account.c.id == id).values(dashboard=dashboard))
    db.commit()

    return http.respond(200, True, '设置成功')