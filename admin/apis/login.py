# -*- coding: utf-8 -*-

from admin import *
from admin.tasks.user.login import to_login, login_out


# TODO
#  ---
#  登录模块
#  ---

@router.post(path='/login', summary='后台登录', tags=['登录'])
async def login(form: admin.AdminLogin, request: Request):

    """

    Args:
        form: login form
        request: client host
    Returns: token

    """

    login_form = par_type.to_json(form)
    token_result = to_login.delay(login_form, request.client.host)
    result = AsyncResult(token_result.id)

    if result.get():
        user_token = result.get()
        return http.respond(status=200, data=user_token)

    return http.respond(status=500, message='账户或密码错误')


@router.post(path='/logout', summary='退出登录', tags=['登录'])
async def logout(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token auth
    Returns: respond

    """

    login_out_result = login_out.delay(token_info['username'])
    result = AsyncResult(login_out_result.id)

    if result.get():
        return http.respond(status=200)

    return http.respond(status=500)