# -*- coding: utf-8 -*-

from admin import *
from admin.tasks.user.account import *


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

    user_info = celery.AsyncResult(get_user_info.delay(token_info).id).get()
    return http.respond(status=200, data=user_info)


@router.post(path='/user/updateInfo', summary='修改账号信息', tags=['用户'])
async def user_edit_info(user_info: admin.AdminUpdateInfo, token_info: str = Depends(http.token)):

    """

    Args:
        user_info: 用户信息
        token_info: token 认证

    Returns: respond

    """

    user_update_info.delay(par_type.to_json(user_info), token_info)
    return http.respond(status=200, message='修改成功')


@router.post(path='/user/modifyPassword', summary='修改账户密码', tags=['用户'])
async def modify_password(password: admin.ModifyPassword, token_info: str = Depends(http.token)):

    """

    Args:
        password: 修改密码传参
        token_info: token 认证
    Returns: respond

    """

    update_password = celery.AsyncResult(update_user_password.delay(
        par_type.to_json(password), token_info).id).get()
    if update_password is True:
        return http.respond(status=200, message='已修改密码')
    elif update_password['status'] == 500:
        return http.respond(
            status=500,
            message=update_password['message']
        )


@router.put(path='/user/initUserPassword/{userId:path}', summary='初始化账户密码', tags=['用户'])
async def init_password(userId: int, token_info: str = Depends(http.token)):

    """

    Args:
        userId: 用户 id
        token_info: token 认证

    Returns: respond

    """

    celery.AsyncResult(into_user_password.delay(userId, token_info).id).get()
    return http.respond(status=200, message='密码已重置')


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
        _: Optional[int] = None,
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

    user_list = celery.AsyncResult(get_all_user_list.delay(page, pageSize, orderBy, orderType,
                                                           dept_id, role_id, post_id, username,
                                                           nickname, phone, email, maxDate,
                                                           minDate, token_info).id).get()
    return http.respond(status=200, data=user_list)


@router.get(path='/user/getDeptTreeList', summary='按部门获取用户', tags=['用户'])
async def user_dept_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: dept_user_list 部门 -> list

    """

    dept_user_list = celery.AsyncResult(get_dept_user_list.delay(token_info).id).get()
    return http.respond(status=200, data=dept_user_list)


@router.get(path='/user/getRoleList', summary='按角色获取用户', tags=['用户'])
async def get_role_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 验证

    Returns: user_role_list 角色 -> list

    """

    user_role_list = celery.AsyncResult(get_role_user_list.delay(token_info).id).get()
    return http.respond(status=200, data=user_role_list)


@router.get(path='/user/getPostList', summary='按岗位获取用户', tags=['用户'])
async def get_post_list(_: Optional[int] = None, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns: user_post_list 岗位 -> list

    """

    user_post_list = celery.AsyncResult(get_post_user_list.delay(token_info).id).get()
    return http.respond(status=200, data=user_post_list)


@router.get(path='/user/onlineUser/index', summary='获取在线用户', tags=['用户'])
async def user_online(
        page: int,
        pageSize: int,
        username: Optional[str] = '',
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        _: Optional[int] = None,
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

    user_online_list = celery.AsyncResult(get_user_online_list.delay(page, pageSize, username,
                                                                     orderBy, orderType, token_info).id).get()
    return http.respond(status=200, data=user_online_list)


@router.post(path='/user/onlineUser/kick', summary='强退用户', tags=['用户'])
async def user_kick(online_user: admin.OnlineUser, token_info: str = Depends(http.token)):

    """

    Args:
        online_user: 在线用户
        token_info: token 认证

    Returns: respond

    """

    take_user_kick.delay(par_type.to_json(online_user))
    return http.respond(status=200)


@router.post(path='/user/clearCache', summary='清除账户缓存', tags=['用户'])
async def role_clear_cache():

    """

    Returns: respond

    """

    return http.respond(status=200)


@router.post(path='/user/downloadTemplate', summary='下载导入模板', tags=['用户'])
def user_download_template(token_info: str = Depends(http.token)):

    """

    Returns: FileResponse

    """

    get_template_path = celery.AsyncResult(get_user_template.delay(token_info).id).get()
    return FileResponse(status_code=200, path=get_template_path)


@router.post(path='/user/import', summary='导入用户数据', tags=['用户'])
async def user_import(file: bytes = File(...), token_info: str = Depends(http.token)):

    """

    Returns: respond

    """

    celery.AsyncResult(user_import_file.delay(file, token_info).id).get()
    return http.respond(status=200)


@router.post(path='/user/userExport', summary='导出用户', tags=['用户'])
async def user_export(ids: Any = Body(...), token_info: str = Depends(http.token)):

    """

    Args:
        ids: 用户ID
        token_info: token 认证

    Returns: FileResponse 文件流 -> bytes

    """

    export_file = celery.AsyncResult(user_export_file.delay(ids, token_info).id).get()
    return FileResponse(status_code=200, path=export_file)


@router.get(path='/user/pageIndex', summary='获取用户列表', tags=['用户'])
async def get_user_index(
        # 列表筛选条件
        page: int,
        pageSize: int,
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        dept_id: Optional[str] = '',
        username: Optional[str] = '',
        nickname: Optional[str] = '',
        phone: Optional[str] = '',
        email: Optional[str] = '',
        status: Optional[str] = '',
        maxDate: Optional[str] = '',
        minDate: Optional[str] = '',
        _: Optional[int] = None,
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

    user_list = celery.AsyncResult(get_user_data.delay(page, pageSize, orderBy, orderType,
                                                       dept_id, username, nickname, phone,
                                                       email, status, maxDate, minDate, token_info).id).get()
    return http.respond(status=200, data=user_list)


@router.get(path='/user/userRead/{userId:path}', summary='查看账户信息', tags=['用户'])
async def read_user(userId: int, token_info: str = Depends(http.token)):

    """

    Args:
        userId: 用户ID
        token_info: token 认证

    Returns: user_info -> dict 用户信息

    """

    user_info = celery.AsyncResult(read_user_info.delay(userId, token_info).id).get()
    print(user_info)
    return http.respond(status=200, data=user_info)


@router.post(path='/user/userSave', summary='添加用户', tags=['用户'])
async def create_user(account: admin.User, token_info: str = Depends(http.token)):

    """

    Args:
        account: 用户信息
        token_info: token 认证

    Returns: respond

    """

    create_user = celery.AsyncResult(create_user_data.delay(
        par_type.to_json(account), token_info).id).get()
    if create_user:
        return http.respond(status=200)
    return http.respond(status=500)


@router.delete(path='/user/userDelete/{userId:path}', summary='删除用户', tags=['用户'])
async def delete_user(userId: str, token_info: str = Depends(http.token)):

    """

    Args:
        userId: 用户ID
        token_token: token 认证

    Returns: respond

    """

    delete_user_profile = celery.AsyncResult(delete_user_data.delay(userId, token_info).id).get()
    if delete_user_profile:
        return http.respond(status=200, message='已删除')
    return http.respond(status=500, message='删除失败')


@router.put(path='/user/userUpdate/{id:path}', summary='编辑用户', tags=['用户'])
async def update_user(id: int, account: admin.User, token_info: str = Depends(http.token)):

    """

    Args:
        id: 用户ID
        account: 用户信息
        token_info: token 认证

    Returns: respond

    """

    update_user = celery.AsyncResult(update_user_data.delay(id, par_type.to_json(account), token_info).id).get()
    if update_user:
        return http.respond(status=200, message='更新成功')
    return http.respond(status=500, message='更新失败')


@router.put(path='/user/changeStatus', summary='更改用户状态', tags=['用户'])
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

    get_change_status = celery.AsyncResult(change_user_status.delay(id, status, token_info).id).get()
    if get_change_status:
        return http.respond(status=200)
    return http.respond(status=500, message='用户状态更改失败')


@router.post(path='/user/setHomePage', summary='设置用户登录首页', tags=['用户'])
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

    set_home = celery.AsyncResult(set_home_view.delay(id, dashboard, token_info).id).get()
    if set_home:
        return http.respond(status=200)
    return http.respond(status=500)