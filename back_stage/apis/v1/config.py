# -*- coding: utf-8 -*-

from back_stage import *

# TODO ----------config系统配置模块----------

@router.post(path='/getConfigByKey', summary='getConfigByKey')
async def get_config_by_key():

    """getConfigByKey"""

    return http.respond(200, True, 'OK')

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

    db.execute(backend_setting.update().where(backend_setting.c.id == 1).values(**dict(setting)))
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
            'currentPage': pageSize,
            'totalPage': pageSize
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