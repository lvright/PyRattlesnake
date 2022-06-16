# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------config key----------

@router.post(path='/getConfigByKey', summary='getConfigByKey')
async def get_config_by_key(conf_key: admin.ConfigByKey):

    """getConfigByKey"""

    conf_key = dict(conf_key)
    config_key = db.query(admin_extend).filter_by(key=conf_key['key']).first()

    if config_key:
        config_key = dict(config_key)

    return http.respond(200, True, 'OK', config_key)

# TODO ----------系统服务信息----------

@router.get(path='/config/server/monitor', summary='获取系统服务信息')
def server_monitor(token_info: str = Depends(http.token)):

    """获取系统服务信息"""

    cpu_proportion = psutil.cpu_times()
    cpu_core = psutil.cpu_count
    cpu_info = cpuinfo.get_cpu_info()
    mem = psutil.virtual_memory()
    swap = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    os_suers = psutil.users()

    cpu = {
        'free': round(cpu_proportion.idle / 10000, 2),
        'usage': round(cpu_proportion.system / 1000 + cpu_proportion.user / 1000, 2),
        'cores': '物理核心数：{}个，逻辑核心数：{}个'.format(str(cpu_core(logical=False)), str(cpu_core())),
        'name': cpu_info['brand_raw'],
        'cache': round(cpu_info['l2_cache_size'] / 100, 2)
    }

    memory_free = round(mem.available / 1000000000, 2)
    memory_total = round(mem.total / 1000000000, 2)

    memory = {
        'free': memory_free,
        'total': memory_total,
        'rate': mem.percent,
        'usage': round(memory_total - memory_free, 2),
    }

    swap_free = round(swap.free / 1000000000, 2)
    swap_total = round(swap.total / 1000000000, 2)

    disk = {
        'free': swap_free,
        'rate': str(swap.percent) + '%',
        'total': swap_total,
        'usage': round(swap_total - swap_free, 2)
    }

    net = {
        'receive_pack': str(round(net_io.bytes_sent / 100000, 2)),
        'receive_total': str(round(net_io.bytes_recv / 100000, 2)),
        'send_pack': str(round(net_io.packets_sent / 10000, 2)),
        'send_total': str(round(net_io.packets_recv / 10000, 2))
    }

    start_time = time.localtime(os_suers[0].started)
    run_time = round((int(time.time()) - os_suers[0].started) / 10000, 2)

    pyenv = {
        'fastapi_version': fastapi.__version__,
        'py_rattlesnake_version': '0.0.1',
        'python_version': platform.python_version(),
        'project_path': os.path.abspath(os.path.join(os.getcwd(), "..")) + '/PyRattlesnake',
        'os': platform.system(),
        'uvicorn_version': uvicorn.__version__,
        'run_time': '已运行{}小时'.format(run_time),
        'start_time': time.strftime('%Y-%m-%d %H:%M:%S', start_time)
    }

    return http.respond(200, True, '获取成功', {
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'net': net,
        'pyenv': pyenv
    })

@router.get(path='/config/redis', summary='获取缓存监控信息')
def get_redis_config(token_info: str = Depends(http.token)):

    """获取缓存监控信息"""

    redis_info = data_base.redis.info()

    server = {
        'version': redis_info['redis_version'],
        'redis_mode': redis_info['redis_mode'],
        'aof_enabled': redis_info['aof_enabled'],
        'clients': redis_info['connected_clients'],
        'expired_keys': redis_info['expired_keys'],
        'port': redis_info['tcp_port'],
        'run_days': redis_info['uptime_in_days'],
        'sys_total_keys': len(data_base.redis.keys()),
        'use_memory': redis_info['used_memory_human'],
    }

    return http.respond(200, True, '获取成功', {
        'server': server,
        'keys': data_base.redis.keys()
    })

@router.post(path='/config/redisView', summary='查看redis key')
def redis_view(redis_info: admin.RedisInfo, token_info: str = Depends(http.token)):

    """查看 redis key"""

    redis_info = dict(redis_info)
    redis_key = data_base.redis.get(redis_info['key'])

    if redis_key:
        return http.respond(200, True, '获取成功', {'content':  redis_key})

    return http.respond(500, False, '找不到key，或key值已过期')

@router.delete(path='/config/redisClear', summary='一键清除redis')
def redis_delete(token_info: str = Depends(http.token)):

    """一键清除 redis"""

    redis_keys = data_base.redis.keys()

    if redis_keys:
        for key in redis_keys:
            data_base.redis.delete(key)

    return http.respond(200, True, '清除成功')

@router.delete(path='/config/redisDelete', summary='删除redis key')
def redis_delete(redis_info: admin.RedisInfo, token_info: str = Depends(http.token)):

    """删除redis key"""

    redis_info = dict(redis_info)

    data_base.redis.delete(redis_info['key'])

    return http.respond(200, True, '清除成功')

@router.get(path='/config/rely/index', summary='获取python依赖包')
def rely_index(
        page: int,
        pageSize: int,
        name: Optional[str] = '',
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        _: int = None,
        token_info: str = Depends(http.token)
):

    """获取python依赖包"""

    with open(project_file_path + '/requirements.txt', 'r') as f:
        if name:
            data = [
                {
                    'name': item.split('==')[0],
                    'version': 'v' + item.split('==')[1]
                } for item in f.read().split()
                if fuzz.ratio(item.split('==')[0], name)
            ]
        else:
            data = [
                {
                    'name': item.split('==')[0],
                    'version': 'v' + item.split('==')[1]
                } for item in f.read().split()
            ]

    return http.respond(200, True, '获取成功', {
        'items': data[page:page + pageSize],
        'pageInfo': {
            'total': len(data),
            'currentPage': page,
            'totalPage': math.ceil(len(data) / pageSize)
        }
    })


@router.get(path='/getSysConfig', summary='getSysConfig')
async def get_sys_config():

    """getSysConfig"""

    config = [dict(conf) for conf in db.query(admin_config).all() if conf]

    return http.respond(200, True, 'OK', config)

@router.get(path='/config/getSystemConfig', summary='系统信息配置')
async def get_sys_config(token_info: str = Depends(http.token)):

    """系统信息配置"""

    config = [dict(conf) for conf in db.query(admin_config).all() if conf]

    return http.respond(200, True, 'OK', config)

@router.post(path='/config/saveSystemConfig', summary='保存系统信息配置')
async def save_system_config(config: admin.SystemConfig, token_info: str = Depends(http.token)):

    """保存系统信息配置"""

    for key in dict(config):
        db.execute(admin_config.update().where(admin_config.c.key == key).values(value=dict(config)[key]))
        db.commit()

    return http.respond(200, True, 'OK')

@router.get(path='/config/getExtendConfig', summary='扩展配置')
async def get_extend_config(token_info: str = Depends(http.token)):

    """扩展配置"""

    extend = [dict(ext) for ext in db.query(admin_extend).all() if ext]

    for ext in extend:
        ext['isSet'] = bool(ext['isSet'])
        ext['isVirtual'] = bool(ext['isVirtual'])
        del ext['id']

    return http.respond(200, True, 'OK', extend)

@router.post(path='/config/save/extendConfig', summary='保存扩展配置')
async def save_extend(extend: admin.ExtendConfig, token_info: str = Depends(http.token)):

    """保存扩展配置"""

    # 查询 key 是否已存在
    extend_all = db.query(admin_extend).filter_by(key=extend.key).first()

    if extend_all is False:

        # 若 key 不存在则插入数据
        db.execute(admin_extend.insert().values(**dict(extend)))

        return http.respond(200, True, '保存成功')

    return http.respond(500, False, '配置key已存在，请重修改后保存')

@router.post(path='/config/update/updateExtendConfig', summary='更新扩展配置')
async def update_extend(extend: admin.ExtendConfig, token_info: str = Depends(http.token)):

    """更新扩展配置"""

    db.execute(admin_extend.update().where(admin_extend.c.name == extend.name).values(**dict(extend)))
    db.commit()

    return http.respond(200, True, '更新成功')

@router.delete(path='/config/update/deleteExtendConfig', summary='删除扩展配置')
async def del_extend(name: str, token_info: str = Depends(http.token)):

    """删除扩展配置"""

    db.execute(admin_extend.delete().where(admin_extend.c.name == name))
    db.commit()

    return http.respond(200, True, '已删除')

@router.post(path='/config/clearCache', summary='清楚系统配置缓存')
async def conf_clear_cache(token_info: str = Depends(http.token)):

    """清楚系统配置缓存"""

    return http.respond(200, True, '清楚成功')

@router.post(path='/user/clearSelfCache', summary='清楚浏览器缓存')
async def conf_clear_cache(token_info: str = Depends(http.token)):

    """清楚浏览器缓存"""

    return http.respond(200, True, '清除成功')

@router.post(path='/user/updateSetting', summary='修改系统设置')
async def update_setting(setting: admin.BackendSetting, token_info: str = Depends(http.token)):

    """修改系统设置"""

    setting = dict(setting)

    setting['layoutTags'] = int(setting['layoutTags'])

    db.execute(backend_setting.update().where(backend_setting.c.user_id == token_info['id']).values(**dict(setting)))
    db.commit()

    return http.respond(200, True, '系统设置修改成功')

# TODO ----------数据字典----------

@router.get(path='/config/apis/{code:path}', summary='根据code获取字典类型')
async def conf_apis(code: str, token_info: str = Depends(http.token)):

    """根据code获取字典类型"""

    result = db.query(sys_dictionary_data).where(sys_dictionary_data.c.code == code).all()

    if code:
        result = [
            {
                'id': dict(item)['id'],
                'label': dict(item)['label'],
                'value': dict(item)['value']
            } for item in result if item
        ]
        return http.respond(200, True, 'OK', result)

@router.get(path='/config/dictType', summary='数据字典类型')
async def dict_type(_: int, token_info: str = Depends(http.token)):

    """数据字典类型"""

    dict_type = [dict(item) for item in db.query(sys_dictionary).all() if item]

    return http.respond(200, True, '请求成功', dict_type)

@router.put(path='/config/dictType/update/{id:path}', summary='更新数据字典类型')
async def dict_type(id: int, dict_type: admin.DictType, token_info: str = Depends(http.token)):

    """更新数据字典类型"""

    # 格式化
    dict_type = dict(dict_type)

    # 插入更新时间
    dict_type['updated_by'] = now_timestamp
    dict_type['updated_at'] = now_date_time

    # 提交
    db.execute(sys_dictionary.update().where(sys_dictionary.c.id == id).values(**dict(dict_type)))
    db.commit()

    return http.respond(200, True, '保存成功')

@router.delete(path='/config/dictType/delete/{id:path}', summary='删除数据字典类型')
async def dict_type(id: int, token_info: str = Depends(http.token)):

    """删除数据字典类型"""

    try:
        # 删除字典数据
        db.execute(sys_dictionary.delete().where(sys_dictionary.c.id == id))
        db.commit()
    except Exception as e:
        # 错误回滚 打印日志
        log.log_error(e)
        return http.respond(500, False, '删除失败：{}'.format(str(e)))

    return http.respond(200, True, '保存成功')

@router.post(path='/config/dictType/save', summary='插入数据字典类型')
async def dict_type(dict_type: admin.DictType, token_info: str = Depends(http.token)):

    """插入数据字典类型"""

    # 格式化
    dict_type = dict(dict_type)

    # 提交创建时间
    dict_type['created_by'] = now_timestamp
    dict_type['created_at'] = now_date_time

    # 提交
    db.execute(sys_dictionary_data.insert().values(**dict(dict_type)))
    db.commit()

    return http.respond(200, True, '添加成功')

@router.get(path='/config/dictDate', summary='获取数据字典')
async def dict_type(
        page: Optional[int] = '',
        pageSize: Optional[int] = '',
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        code: Optional[str] = '',
        _: Optional[int] = '',
        token_info: str = Depends(http.token)
):

    """获取数据字典"""

    dict_data = [
        dict(item) for item in db.query(
            sys_dictionary_data
        ).where(
            sys_dictionary_data.c.code == code
        ).limit(pageSize) if item
    ]

    return http.respond(200, True, '请求成功', {
        'items': dict_data,
        'pageInfo': {
            'total': len(dict_data),
            'currentPage': page,
            'totalPage': math.ceil(len(dict_data) / pageSize)
        }
    })

@router.put(path='/config/dictDate/update/{id:path}', summary='更新数据字典')
async def dict_type(id: int, dict_data: admin.DictDate, token_info: str = Depends(http.token)):

    """更新数据字典"""

    # 格式化
    dict_data = dict(dict_data)

    # 插入更新时间
    dict_data['updated_by'] = now_timestamp
    dict_data['updated_at'] = now_date_time

    # 提交
    db.execute(sys_dictionary_data.update().where(sys_dictionary_data.c.id == id).values(**dict(dict_data)))
    db.commit()

    return http.respond(200, True, '保存成功')

@router.post(path='/config/dictDate/save', summary='插入数据字典')
async def dict_type(dict_data: admin.DictDate, token_info: str = Depends(http.token)):

    """插入数据字典"""

    # 格式化
    dict_data = dict(dict_data)

    # 插入创建时间
    dict_data['created_by'] = now_timestamp
    dict_data['created_at'] = now_date_time

    # 提交
    db.execute(sys_dictionary.insert().values(**dict(dict_data)))
    db.commit()

    return http.respond(200, True, '添加成功')

@router.delete(path='/config/dictDate/delete/{id:path}', summary='删除数据字典')
async def dict_type(id: Any, token_info: str = Depends(http.token)):

    """删除数据字典"""

    try:
        # split 分割 id 删除字典数据
        for _id in id.split(','):
            db.execute(sys_dictionary_data.delete().where(sys_dictionary_data.c.id == _id))
            db.commit()
    except Exception as e:
        # 错误回滚 打印日志
        log.log_error(e)
        return http.respond(500, False, '删除失败：{}'.format(str(e)))

    return http.respond(200, True, '保存成功')

@router.post(path='/config/dict/clearCache', summary='清除数据字典缓存')
async def dict_clear_cache(token_info: str = Depends(http.token)):

    """清除数据字典缓存"""

    return http.respond(200, True, '已清除缓存')

@router.put(path='/config/dict/changeStatus', summary='修改数据字典状态')
async def dict_clear_cache(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """修改数据字典状态"""

    db.execute(sys_dictionary.update().where(sys_dictionary.c.id == id).values(status=status))
    db.commit()

    return http.respond(200, True, '字典状态修改成功')