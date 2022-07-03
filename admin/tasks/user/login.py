# -*- coding: utf-8 -*-

from admin import *
from admin.tasks import *


@celery.task
def to_login(form, ip):

    # 查询登录账户和密码
    user_info = par_type.to_json(db.execute(select(
        admin_account).where(admin_account.c.userId == form['username'],
                             admin_account.c.password == form['password'])).first())

    login_ip = {
        'username': user_info['username'], 'ip': ip,
        'login_time': now_date_time, 'status': 0, 'message': '登陆成功'
    }

    if user_info:
        del user_info['password']
        # token
        token = jwt_token.encode(user_info)
        db.execute(
            update(admin_account).where(admin_account.c.id == user_info['id']).values(
                **{'login_ip': ip, 'login_time': now_date_time}))

        data_base.redis.set('user_token:' + user_info['username'], token, ex=3000)

        db.execute(insert(sys_login_log).values(**login_ip))
        db.commit()

        return {'token': token}

    login_ip['message'] = '账户或密码错误'
    db.execute(insert(sys_login_log).values(**ip_config))
    db.commit()

    return False


@celery.task
def login_out(username):

    try:
        data_base.redis.delete(username)
    except Exception as e:
        return False

    return True
