# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------登录模块----------

@router.get(path='/captcha', summary='获取图片验证码')
async def get_code_key():

    """获取图片验证码"""

    # 调用图片验证码模块获取 code 和 url
    get_code = captcha.code_img()

    # 暂不设置 redis

    if get_code:
        return http.respond(200, True, 'OK', {'codeUrl': get_code['img_url']})

@router.post(path='/login', summary='后台登录')
async def admin_login(login_info: admin.AdminLogin, request: Request):

    """后台登录"""

    # 查询登录账户和密码
    admin_info = db.query(admin_account).filter_by(userId=login_info.username, password=login_info.password).first()

    if admin_info:

        admin_info = dict(admin_info)

        del admin_info['password']

        # token 加密
        token = jwt_token.encode(dict(admin_info))

        db.execute(admin_account.update().where(admin_account.c.id == admin_info['id']).values(
            **{'login_ip': request.client.host, 'login_time': now_date_time}
        ))
        db.commit()

        data_base.redis.set(admin_info['username'], token, ex=3000)

        return http.respond(200, True, '登陆成功', {'token': token})

    return http.respond(500, False, '账户或密码错误')

@router.post(path='/logout', summary='退出登录')
def logout(token_info: str = Depends(http.token)):

    """退出登录"""

    data_base.redis.delete(token_info['username'])

    return http.respond(200, True, '退出成功')