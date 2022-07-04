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

    user_token = celery.AsyncResult(to_login.delay(par_type.to_json(form), request.client.host).id).get()
    if user_token:
        return http.respond(status=200, data=user_token)
    return http.respond(status=500, message='账户或密码错误')


@router.post(path='/logout', summary='退出登录', tags=['登录'])
async def logout(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token auth
    Returns: respond

    """

    celery.AsyncResult(login_out.delay(token_info['username']).id).get()
    return http.respond(status=500)