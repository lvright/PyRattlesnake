# -*- coding: utf-8 -*-

from admin import *


# TODO
#  ---
#  系统配置
#  ---

@router.post(path='/getConfigByKey', summary='getConfigByKey', tags=['系统服务'])
async def get_config_by_key(conf_key: admin.ConfigByKey):

    """

    Args:
        conf_key: 系统 key

    Returns: config_key 系统配置key -> str

    """

    conf_key = par_type.to_json(conf_key)

    config_key = par_type.to_json(db.execute(select(
        admin_extend).where(admin_extend.c.key == conf_key['key'])).first())

    return http.respond(status=200, data=config_key)


# TODO
#  ---
#  系统服务信息
#  ---

@router.get(path='/config/server/monitor', summary='获取系统服务信息', tags=['系统服务'])
async def server_monitor(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: results 系统服务监控信息 -> dict

    """

    # 服务监控
    cpu_proportion = psutil.cpu_times()
    cpu_core = psutil.cpu_count
    cpu_info = cpuinfo.get_cpu_info()
    mem = psutil.virtual_memory()
    swap = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    os_suers = psutil.users()

    # 换算基数
    base_num = 1000000000
    one_hundred_thousand = 100000
    ten_thousand = 10000
    a_thousand = 1000

    # 取值换算
    memory_free = round(mem.available / base_num, 2)
    memory_total = round(mem.total / base_num, 2)

    swap_free = round(swap.free / base_num, 2)
    swap_total = round(swap.total / base_num, 2)

    start_time = time.localtime(os_suers[0].started)
    run_time = round((int(time.time()) - os_suers[0].started) / ten_thousand, 2)

    results = {
        'cpu': {
            'free': round(cpu_proportion.idle / ten_thousand, 2),
            'usage': round(cpu_proportion.system / 1000 + cpu_proportion.user / a_thousand, 2),
            'cores': f'物理核心数：{str(cpu_core(logical=False))}个，逻辑核心数：{str(cpu_core())}个',
            'name': cpu_info['brand_raw'],
            'cache': round(cpu_info['l2_cache_size'] / 100, 2)
        },
        'memory': {
            'free': memory_free,
            'total': memory_total,
            'rate': mem.percent,
            'usage': round(memory_total - memory_free, 2),
        },
        'disk': {
            'free': swap_free,
            'rate': str(swap.percent) + '%',
            'total': swap_total,
            'usage': round(swap_total - swap_free, 2)
        },
        'net': {
            'receive_pack': str(round(net_io.bytes_sent / one_hundred_thousand, 2)),
            'receive_total': str(round(net_io.bytes_recv / one_hundred_thousand, 2)),
            'send_pack': str(round(net_io.packets_sent / ten_thousand, 2)),
            'send_total': str(round(net_io.packets_recv / ten_thousand, 2))
        },
        'pyenv': {
            'fastapi_version': fastapi.__version__,
            'py_rattlesnake_version': '0.0.1',
            'python_version': platform.python_version(),
            'project_path': project_file_path,
            'os': platform.system(),
            'uvicorn_version': uvicorn.__version__,
            'run_time': '已运行{}小时'.format(run_time),
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S', start_time)
        }
    }

    return http.respond(status=200, data=results)


@router.get(path='/config/redis', summary='获取缓存监控信息', tags=['系统服务'])
async def get_redis_config(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: results redis 缓存监控信息 -> dict

    """

    redis_info = data_base.redis.info()

    results = {
        'server': {
            'version': redis_info['redis_version'],
            'redis_mode': redis_info['redis_mode'],
            'aof_enabled': redis_info['aof_enabled'],
            'clients': redis_info['connected_clients'],
            'expired_keys': redis_info['expired_keys'],
            'port': redis_info['tcp_port'],
            'run_days': redis_info['uptime_in_days'],
            'sys_total_keys': len(data_base.redis.keys()),
            'use_memory': redis_info['used_memory_human'],
        },
        'keys': data_base.redis.keys()
    }

    return http.respond(status=200, data=results)


@router.post(path='/config/redisView', summary='查看redis key', tags=['系统服务'])
async def redis_view(redis_info: admin.RedisInfo, token_info: str = Depends(http.token)):

    """

    Args:
        redis_info: redis 信息
        token_info: token 认证

    Returns: respond

    """

    redis_info = dict(redis_info)
    redis_key = data_base.redis.get(redis_info['key'])

    results = {'content': redis_key}

    if redis_key:
        return http.respond(status=200, data=results)

    return http.respond(status=500)


@router.delete(path='/config/redisClear', summary='清除所有redis', tags=['系统服务'])
async def redis_delete(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: respond

    """

    redis_keys = data_base.redis.keys()

    if redis_keys:
        for key in redis_keys:
            data_base.redis.delete(key)

    return http.respond(status=200)


@router.delete(path='/config/redisDelete', summary='删除 redis key', tags=['系统服务'])
async def redis_delete(redis_info: admin.RedisInfo, token_info: str = Depends(http.token)):

    """

    Args:
        redis_info: redis 信息
        token_info: token 认证

    Returns: respond

    """

    redis_info = dict(redis_info)
    data_base.redis.delete(redis_info['key'])

    return http.respond(status=200)


# TODO
#  ---
#  系统配置
#  ---

@router.get(path='/getSysConfig', summary='系统配置信息', tags=['系统配置'])
async def get_sys_config():

    """

    Returns: config 系统配置信息 -> list

    """

    config = par_type.to_json(db.execute(select(admin_config)).all())

    return http.respond(200, True, 'OK', config)


@router.get(path='/config/getSystemConfig', summary='系统服务配置', tags=['系统配置'])
async def get_sys_config(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: config 系统配置信息 -> list

    """

    config = par_type.to_json(db.execute(select(admin_config)).all())

    return http.respond(200, True, 'OK', config)


@router.post(path='/config/saveSystemConfig', summary='保存系统信息配置', tags=['系统配置'])
async def save_system_config(config: admin.SystemConfig, token_info: str = Depends(http.token)):

    """

    Args:
        config: 系统配置信息
        token_info: token 认证

    Returns: respond

    """

    for key in dict(config):
        db.execute(update(admin_config).where(
            admin_config.c.key == key).values(value=dict(config)[key]))
        db.commit()

    return http.respond(status=200, message='已保存')


@router.get(path='/config/getExtendConfig', summary='扩展配置', tags=['系统配置'])
async def get_extend_config(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: extend 系统扩展配置 -> dict

    """

    extend = par_type.to_json(db.execute(select(admin_extend)).all())

    for ext in extend:
        ext['isSet'] = bool(ext['isSet'])
        ext['isVirtual'] = bool(ext['isVirtual'])
        del ext['id']

    return http.respond(status=200, data=extend)


@router.post(path='/config/save/extendConfig', summary='保存扩展配置', tags=['系统配置'])
async def save_extend(extend: admin.ExtendConfig, token_info: str = Depends(http.token)):

    """

    Args:
        extend: 系统配置信息
        token_info: token 认证

    Returns: respond

    """

    # 查询 key 是否已存在
    extend_all = par_type.to_json(db.execute(select(
        admin_extend).where(admin_extend.c.key == extend.key)).first())
    if extend_all is None:
        # 若 key 不存在则插入数据
        db.execute(insert(admin_extend).values(**dict(extend)))
        db.commit()
        return http.respond(status=200, message='添加成功')

    return http.respond(status=500, message='扩展配置key已存在，请重新添加')


@router.post(path='/config/update/updateExtendConfig', summary='更新扩展配置', tags=['系统配置'])
async def update_extend(extend: admin.ExtendConfig, token_info: str = Depends(http.token)):

    """

    Args:
        extend: 系统配置信息
        token_info: token 认证

    Returns: respond

    """

    db.execute(update(admin_extend).where(
        admin_extend.c.name == extend.name).values(**dict(extend)))
    db.commit()

    return http.respond(status=200, message='已保存')


@router.delete(path='/config/delete/deleteExtendConfig/{key:path}', summary='删除扩展配置', tags=['系统配置'])
async def del_extend(key: str, token_info: str = Depends(http.token)):

    """

    Args:
        name: 配置名称
        token_info: token 认证

    Returns: respond

    """

    db.execute(delete(admin_extend).where(admin_extend.c.key == key))
    db.commit()

    return http.respond(status=200)


@router.post(path='/config/clearCache', summary='清除系统配置缓存', tags=['系统配置'])
async def conf_clear_cache(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: respond

    """

    return http.respond(status=200)


@router.post(path='/user/clearSelfCache', summary='清除浏览器缓存', tags=['系统配置'])
async def conf_clear_cache(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: respond

    """

    return http.respond(status=200)


@router.post(path='/user/updateSetting', summary='修改系统设置', tags=['系统配置'])
async def update_setting(setting: admin.BackendSetting, token_info: str = Depends(http.token)):

    """

    Args:
        setting: 系统设置信息
        token_info: token 认证

    Returns: respond

    """

    setting = dict(setting)

    setting['layoutTags'] = int(setting['layoutTags'])

    db.execute(backend_setting.update().where(
        backend_setting.c.user_id == token_info['id']).values(**dict(setting)))
    db.commit()

    return http.respond(200, True, '系统设置修改成功')


# TODO
#  ---
#  数据字典
#  ---

@router.get(path='/config/apis/{code:path}', summary='根据code获取字典类型', tags=['数据字典'])
async def conf_apis(code: str, token_info: str = Depends(http.token)):

    """

    Args:
        code: 字典code值
        token_info: token 认证

    Returns: dictionary 数据字典列表 -> list

    """

    dictionary = par_type.to_json(db.execute(select(
        sys_dictionary_data).where(sys_dictionary_data.c.code == code)).all())

    if code:
        results = [{'id': item['id'], 'label': item['label'], 'value': item['value']}
                   for item in dictionary if item]

        return http.respond(status=200, data=results)


@router.get(path='/config/dictType', summary='数据字典类型', tags=['数据字典'])
async def dict_type(_: int, token_info: str = Depends(http.token)):

    """

    Args:
        _: 时间戳
        token_info: token 认证

    Returns:

    """

    dict_type = par_type.to_json(db.execute(select(sys_dictionary)).all())

    return http.respond(status=200, data=dict_type)


@router.put(path='/config/dictType/update/{id:path}', summary='更新数据字典类型', tags=['数据字典'])
async def dict_type(id: int, dict_type: admin.DictType, token_info: str = Depends(http.token)):

    """

    Args:
        id: 字典ID
        dict_type: 字典类型
        token_info: token 认证

    Returns: respond

    """

    # 格式化
    dict_type = dict(dict_type)
    # 插入更新时间
    dict_type['updated_by'] = now_timestamp
    dict_type['updated_at'] = now_date_time

    # 提交
    db.execute(update(sys_dictionary).where(sys_dictionary.c.id == id).values(**dict(dict_type)))
    db.commit()

    return http.respond(status=200)


@router.delete(path='/config/dictType/delete/{id:path}', summary='删除数据字典类型', tags=['数据字典'])
async def dict_type(id: int, token_info: str = Depends(http.token)):

    """

    Args:
        id: 字典ID
        token_info: token 认证

    Returns: respond

    """

    try:
        # 删除字典数据
        db.execute(delete(sys_dictionary).where(sys_dictionary.c.id == id))
        db.commit()
    except Exception as e:
        # 错误回滚 打印日志
        log.error(e)
        return http.respond(status=500)

    return http.respond(status=200)


@router.post(path='/config/dictType/save', summary='插入数据字典类型', tags=['数据字典'])
async def dict_type(dict_type: admin.DictType, token_info: str = Depends(http.token)):

    """

    Args:
        dict_type: 字典类型
        token_info: token 认证

    Returns: respond

    """

    # 格式化
    dict_type = dict(dict_type)
    # 提交创建时间
    dict_type['created_by'] = now_timestamp
    dict_type['created_at'] = now_date_time

    # 提交
    db.execute(insert(sys_dictionary_data).values(**dict(dict_type)))
    db.commit()

    return http.respond(status=200)

@router.get(path='/config/dictDate', summary='获取数据字典', tags=['数据字典'])
async def dict_type(
        page: Optional[int] = '',
        pageSize: Optional[int] = '',
        orderBy: Optional[str] = '',
        orderType: Optional[str] = '',
        code: Optional[str] = '',
        _: Optional[int] = None,
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        orderBy: 排序
        orderType: 排序类型
        code: 字典code值
        _: 时间戳
        token_info: token 认证

    Returns: dictionary 获取数据字典 -> list

    """

    offset_page = (page - 1) * pageSize

    dict_data = par_type.to_json(db.execute(select(sys_dictionary_data).where(
        sys_dictionary_data.c.code == code).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(sys_dictionary_data.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': dict_data,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.put(path='/config/dictDate/update/{id:path}', summary='更新数据字典', tags=['数据字典'])
async def dict_type(id: int, dict_data: admin.DictDate, token_info: str = Depends(http.token)):

    """

    Args:
        id: 数据字典ID
        dict_data: 数据字典信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化
    dict_data = dict(dict_data)
    # 插入更新时间
    dict_data['updated_by'] = now_timestamp
    dict_data['updated_at'] = now_date_time

    # 提交
    db.execute(update(sys_dictionary_data).where(sys_dictionary_data.c.id == id).values(**dict(dict_data)))
    db.commit()

    return http.respond(status=200)


@router.post(path='/config/dictDate/save', summary='插入数据字典', tags=['数据字典'])
async def dict_type(dict_data: admin.DictDate, token_info: str = Depends(http.token)):

    """

    Args:
        dict_data: 数据字典信息
        token_info: token 认证

    Returns: respond

    """

    # 格式化
    dict_data = dict(dict_data)
    # 插入创建时间
    dict_data['created_by'] = now_timestamp
    dict_data['created_at'] = now_date_time

    # 提交
    db.execute(insert(sys_dictionary).values(**dict(dict_data)))
    db.commit()

    return http.respond(status=200)


@router.delete(path='/config/dictDate/delete/{id:path}', summary='删除数据字典', tags=['数据字典'])
async def dict_type(id: Any, token_info: str = Depends(http.token)):

    """

    Args:
        id: 字典ID
        token_info: token 认证

    Returns: respond

    """

    try:
        # split 分割 id 删除字典数据
        for dict_id in id.split(','):
            db.execute(delete(sys_dictionary_data).where(sys_dictionary_data.c.id == dict_id))
            db.commit()
    except Exception as e:
        # 错误回滚 打印日志
        log.error(e)
        return http.respond(status=500)

    return http.respond(status=200)


@router.post(path='/config/dict/clearCache', summary='清除数据字典缓存', tags=['数据字典'])
async def dict_clear_cache(token_info: str = Depends(http.token)):

    """

    Args:
        token_info: token 认证

    Returns: respond

    """

    return http.respond(200, True, '已清除缓存')


@router.put(path='/config/dict/changeStatus', summary='修改数据字典状态', tags=['数据字典'])
async def dict_clear_cache(
        id: int = Body(...),
        status: str = Body(...),
        token_info: str = Depends(http.token)
):

    """

    Args:
        id: 数据字典ID
        status: 数据字典状态
        token_info: token 认证

    Returns: respond

    """

    db.execute(update(sys_dictionary).where(sys_dictionary.c.id == id).values(status=status))
    db.commit()

    return http.respond(status=200)