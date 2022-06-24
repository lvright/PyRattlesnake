# -*- coding: utf-8 -*-

from admin import *


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

    # 查询登录账户和密码
    user_info = par_type.to_json(db.execute(
        select(admin_account).where(admin_account.c.userId == form.username,
                                    admin_account.c.password == form.password)).first())

    ip_config = {
        'username': user_info['username'], 'ip': request.client.host,
        'login_time': now_date_time, 'status': 0, 'message': '登陆成功'
    }

    if user_info:
        del user_info['password']
        # token
        token = jwt_token.encode(user_info)
        db.execute(
            update(admin_account).where(admin_account.c.id == user_info['id']).values(
                **{'login_ip': request.client.host, 'login_time': now_date_time}))

        data_base.redis.set('user_token:' + user_info['username'], token, ex=3000)

        db.execute(insert(sys_login_log).values(**ip_config))
        db.commit()

        return http.respond(status=200, data={'token': token})

    ip_config['message'] = '账户或密码错误'
    db.execute(insert(sys_login_log).values(**ip_config))
    db.commit()

    return http.respond(status=200)


@router.post(path='/logout', summary='退出登录', tags=['登录'])
def logout(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token auth
    Returns: respond 200

    """

    data_base.redis.delete(token_info['username'])

    return http.respond(status=200)
