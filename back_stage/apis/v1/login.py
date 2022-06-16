# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------登录模块----------

@router.post(path='/login', summary='后台登录')
async def admin_login(login_info: admin.AdminLogin, request: Request):

    """后台登录"""

    # 查询登录账户和密码
    admin_info = db.query(admin_account).filter_by(userId=login_info.username, password=login_info.password).first()

    ip_info = {}

    get_ip_info = requests.get(Config.get_ip_url, {'ip': request.client.host, 'token': Config.get_ip_token})

    if get_ip_info.status_code == 200:

        ip_location = get_ip_info.json()['data']

        if request.client.host == '0.0.0.0' or '127.0.0.1':
            ip_info['ip_location'] = '本地测试'
        else:
            ip_info['ip_location'] = '{}-{}-{}-{}:{}' \
                .format(
                ip_location[0], ip_location[1],
                ip_location[2], ip_location[3],
                ip_location[4]
            )

        ip_info['username'] = dict(admin_info)['username']
        ip_info['ip'] = request.client.host
        ip_info['login_time'] = now_date_time
        ip_info['status'] = 0

    if admin_info:

        admin_info = dict(admin_info)
        del admin_info['password']

        # token 加密
        token = jwt_token.encode(dict(admin_info))

        db.execute(admin_account.update().where(admin_account.c.id == admin_info['id']).values(
            **{'login_ip': request.client.host, 'login_time': now_date_time}
        ))
        db.commit()

        data_base.redis.set('user_token:' + admin_info['username'], token, ex=3000)

        ip_info['message'] = '登录成功'
        db.execute(sys_login_log.insert().values(**ip_info))
        db.commit()

        return http.respond(200, True, '登陆成功', {'token': token})

    ip_info['message'] = '账户或密码错误'
    db.execute(sys_login_log.insert().values(**ip_info))
    db.commit()

    return http.respond(500, False, '账户或密码错误')

@router.post(path='/logout', summary='退出登录')
def logout(token_info: str = Depends(http.token)):

    """退出登录"""

    data_base.redis.delete(token_info['username'])

    return http.respond(200, True, '退出成功')