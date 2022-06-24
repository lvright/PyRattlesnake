# -*- coding: utf-8 -*-

from admin import *

# TODO ----------系统附件管理----------

@router.get(path='/attachment/index', summary='获取附件内容', tags=['系统附件'])
async def get_attachment(
        page: int,
        pageSize: int,
        mime_type: Optional[str] = '',
        origin_name: Optional[str] = '',
        type: Optional[str] = '',
        _: Optional[int] = '',
        token_info: str = Depends(http.token)
):

    """

    Args:
        page: 当前页
        pageSize: 分页数
        mime_type: 文件属性
        origin_name: 文件名称
        type: 文件类型
        _: 时间戳
        token_info: token 认证

    Returns: file_data 文件列表 -> list

    """

    offset_page = (page - 1) * pageSize

    if mime_type:
        file_list = par_type.to_json(db.execute(select(attachment).where(
            attachment.c.mime_type == mime_type).limit(pageSize).offset(offset_page)).all())
    elif origin_name:
        file_list = par_type.to_json(db.execute(select(attachment).where(
            attachment.c.origin_name.like('%' + origin_name + '%')).limit(pageSize).offset(offset_page)).all())
    else:
        file_list = par_type.to_json(db.execute(select(
            attachment).limit(pageSize).offset(offset_page)).all())

    total = db.query(func.count(attachment.c.id)).scalar()
    total_page = math.ceil(total / pageSize)

    results = {
        'items': file_list,
        'pageInfo': {
            'total': total,
            'currentPage': page,
            'totalPage': total_page
        }
    }

    return http.respond(status=200, data=results)


@router.post(path='/attachment/uploadImage', summary='上传图片附件', tags=['系统附件'])
async def upload_image(image: UploadFile = File(...), token_info: str = Depends(http.token)):

    """

    Args:
        image: 图片文件流
        token_info: token 认证

    Returns: file_url 文件路径 -> str

    """

    # 存储文件夹 按日期来建立
    save_datetime = str(datetime.now().strftime('%Y%m%d'))

    # 如果不是媒体类型文件 则修改文件类型读取规则
    if files.filename.split('.')[1] != 'image':
        return http.respond(500, False, '上传的不是图片，而是其他文件')
    else:
        # 文件夹类型 XXX/XXX
        mime_type = files.content_type.split('/')[0]  # 文件类型
        file_suffix = files.content_type.split('/')[1]  # 后缀

        # 读取文件 bytes
        file_data = await files.read()

        # 存储的文件夹名称
        storage_path = project_file_path + '/static/attachment/' + save_datetime

        # 判断如果没有文件夹则新建
        if not os.path.exists(storage_path): os.makedirs(storage_path)

        # 存储后文件名称
        object_name = str(captcha.random_code()) + '.' + file_suffix

        # 存储前文件名称
        file_save_path = storage_path + '/' + object_name

        # 存储的路径
        file_url = '/static/attachment/' + save_datetime + '/' + object_name

        # 保存文件
        with open(file_save_path, 'wb') as f:
            f.write(file_data)

        # 将文件信息写入数据库并返回文件 id
        file_id = db.execute(insert(attachment).values(
            **{
                'storage_mode': "1",
                'origin_name': files.filename,
                'object_name': object_name,
                'mime_type': mime_type,
                'storage_path': save_datetime,
                'suffix': file_suffix,
                'size_byte': len(file_data),
                'size_info': str(files.spool_max_size) + 'KB',
                'url': file_url,
                'created_by': now_timestamp,
                'updated_by': now_timestamp,
                'created_at': now_date_time,
                'updated_at': now_date_time
            })).lastrowid
        db.commit()

        results = {'url': file_url, 'fileName': files.filename, 'id': file_id}

        return http.respond(status=200, data=results)

@router.post(path='/attachment/uploadFile', summary='上传文件附件', tags=['系统附件'])
async def upload_image(files: UploadFile = File(...), token_info: str = Depends(http.token)):

    """

    Args:
        files:
        token_info:

    Returns: file_url 文件路径 -> str

    """

    # 存储文件夹 按日期来建立
    save_datetime = str(datetime.now().strftime('%Y%m%d'))

    # 如果不是媒体类型文件 则修改文件类型读取规则
    if files.filename.split('.')[1] in ['image', 'video', 'audio']:
        # 文件夹类型 XXX/XXX
        mime_type = files.content_type.split('/')[0]  # 文件类型
        file_suffix = files.content_type.split('/')[1]  # 后缀
    else:
        # 文件夹类型 XXX/XXX
        mime_type = 'text'  # 文件类型
        file_suffix = files.filename.split('.')[1]  # 后缀

    # 读取文件 bytes
    file_data = await files.read()

    # 存储的文件夹名称
    storage_path = project_file_path + '/static/attachment/' + save_datetime

    # 判断如果没有文件夹则新建
    if not os.path.exists(storage_path): os.makedirs(storage_path)

    # 存储后文件名称
    object_name = str(captcha.random_code()) + '.' + file_suffix

    # 存储前文件名称
    file_save_path = storage_path + '/' + object_name

    # 存储的路径
    file_url = '/static/attachment/' + save_datetime + '/' + object_name

    # 保存文件
    with open(file_save_path, 'wb') as f:
        f.write(file_data)

    # 将文件信息写入数据库并返回文件 id
    file_id = db.execute(insert(attachment).values(**{
            'storage_mode': "1",
            'origin_name': files.filename,
            'object_name': object_name,
            'mime_type': mime_type,
            'storage_path': save_datetime,
            'suffix': file_suffix,
            'size_byte': len(file_data),
            'size_info': str(files.spool_max_size) + 'KB',
            'url': file_url,
            'created_by': now_timestamp,
            'updated_by': now_timestamp,
            'created_at': now_date_time,
            'updated_at': now_date_time,
        })).lastrowid
    db.commit()

    results = {'url': file_url, 'fileName': files.filename, 'id': file_id}

    return http.respond(status=200, data=results)

@router.delete(path='/attachment/delete/{ids:path}', summary='删除附件文件', tags=['系统附件'])
async def attachment_delete(ids: str, token_info: str = Depends(http.token)):

    """

    Args:
        ids: 文件ID
        token_info: token 认证

    Returns: respond

    """

    # 踹一踹
    try:
        # 分割 ids
        for id in ids.split(','):
            # 逐一提交删除
            db.execute(delete(attachment).where(attachment.c.id == id))
            db.commit()
    except Exception as e:
        # 错误回滚
        log.log_error(e)
        db.rollback()
        return http.respond(500, False, '删除失败')

    return http.respond(200, True, '删除成功')

@router.post(path='/attachment/saveNetworkImage', summary='保存网络图片', tags=['系统附件'])
async def save_network_image(
        url: str = Body(...),
        path: Optional[str] = Body(...),
        token_info: str = Depends(http.token)
):

    """

    Args:
        url: 网络图片地址
        path: 图片路径
        token_info: token 认证

    Returns: file_url 文件路径 -> str

    """

    # 存储文件夹 按日期来建立
    save_datetime = str(datetime.now().strftime('%Y%m%d'))

    # 存储图片名称
    file_name = str(captcha.random_code()) + '.' + 'jpeg'

    # 保存文件夹名称
    file_save = project_file_path + '/static/attachment/' + save_datetime

    # 存储的文件夹名称
    save_path = file_save + '/' + file_name

    # 判断如果没有文件夹则新建
    if not os.path.exists(file_save): os.makedirs(file_save)

    image_data = requests.get(url).content

    # 保存文件
    with open(save_path, 'wb') as f:
        f.write(image_data)
        f.close()

    image = open(save_path, 'rb').read()

    file_url = '/static/attachment/' + save_datetime + '/' + file_name

    # 将文件信息写入数据库并返回文件 id
    file_id = db.execute(insert(attachment).values(**{
            'storage_mode': "1",
            'origin_name': file_name,
            'object_name': file_name,
            'mime_type': 'image',
            'storage_path': save_datetime,
            'suffix': 'jpg',
            'size_byte': len(image),
            'size_info': str(len(image) / 100) + 'KB',
            'url': file_url,
            'created_by': now_timestamp,
            'updated_by': now_timestamp,
            'created_at': now_date_time,
            'updated_at': now_date_time,
        })).lastrowid
    db.commit()

    results = {'url': file_url, 'fileName': file_name, 'id': file_id}

    return http.respond(status=200, data=results)