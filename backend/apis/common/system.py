# -*- coding: utf-8 -*-

import os
import random
from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db, page_total
from backend.core import check_jwt_token
from backend.crud import getLoginLog, getOperLog, getBackendSetting, getDept, getRole, getPost, getUser, getAnnex
from backend.scheams import Result, BackendSetting, Ids
from utils import resp_200

router = APIRouter()


@router.put(
    path="/system/common/saveSysSetting",
    response_model=Result,
    summary="更新系统配置"
)
async def update_backend_setting(
        backend_setting: BackendSetting,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getBackendSetting.updateBackendSetting(db, user_id=token["id"], obj_in=backend_setting.dict())
    return resp_200(msg="更新成功")


@router.get(
    path="/system/common/getDeptTreeList",
    response_model=Result,
    summary="获取树状部门"
)
async def get_tree_dept(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getDept.deptTree(db))


@router.get(
    path="/system/common/getRoleList",
    response_model=Result,
    summary="获取角色列表"
)
async def get_role_list(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getRole.get_all(db))


@router.get(
    path="/system/common/getPostList",
    response_model=Result,
    summary="获取部门列表"
)
async def get_post_list(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getPost.get_all(db))


@router.post(
    path="/system/common/getUserInfoByIds",
    response_model=Result,
    summary="获取接收信息用户"
)
async def get_user_by_id(
        user: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = []
    for user_id in user.ids:
        result.append(await getUser.get(db, user_id))
    return resp_200(data=result)


@router.get(
    path="/system/clearAllCache",
    response_model=Result,
    summary="更新系统缓存"
)
async def get_system_clear(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await db.flush()
    return resp_200(msg="已清理缓存")


# 文件流 response model 不支持标准的 result 类型
@router.post(
    path="/system/uploadImage",
    summary="上传图片文件"
)
async def upload_image(
        image: UploadFile = File(...),
        isChunk: bool = Form(...),
        hash: str = Form(...),
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    contents = await image.read()
    savePath = "/static/attachment/" + image.filename
    with open(os.path.abspath("..") + savePath, "wb") as f: f.write(contents)
    result = {
        "object_name": str(random.randint(1, 100)),
        "origin_name": image.filename,
        "url": savePath,
        "size_byte": str(image.spool_max_size),
        "storage_mode": image.file.mode,
        "storage_path": "attachment",
        "size_info": str(image.spool_max_size/1000)+"KB",
        "suffix": image.filename.split(".")[1]
    }
    await getAnnex.create(db, obj_in=result)
    return resp_200(data=result, msg="上传成功")


@router.post(path="/system/uploadFile", summary="上传文件")
async def upload_image(
        file: UploadFile = File(...),
        isChunk: bool = Form(...),
        hash: str = Form(...),
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    contents = await file.read()
    savePath = "/static/attachment/" + file.filename
    with open(os.path.abspath("..") + savePath, "wb") as f: f.write(contents)
    await getAnnex.create(db, obj_in={
        "object_name": str(random.randint(1, 100)),
        "origin_name": file.filename,
        "url": savePath,
        "size_byte": str(file.spool_max_size),
        "storage_mode": file.file.mode,
        "storage_path": "attachment",
        "size_info": str(file.spool_max_size/1000)+"KB",
        "suffix": file.filename.split(".")[1]
    })
    return resp_200(data=result, msg="上传成功")


@router.get(
    path="/system/common/getLoginLogList",
    response_model=Result,
    summary="系统登录日志"
)
async def get_login_log(
        username: str,
        orderBy: str,
        orderType: str,
        pageSize: int,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    total = await getLoginLog.get_number(db)
    result = await getLoginLog.get_multi(
        db, orderBy="login_time", orderType="desc", pageIndex=1, pageSize=pageSize
    )
    result = [res for res in result if res["username"] == username and res]
    return resp_200(data={"items": result, "pageInfo": {
            "total": total, "currentPage": 1, "totalPage": page_total(total, pageSize)
        }
    })


@router.get(
    path="/system/common/getOperationLogList",
    response_model=Result,
    summary="系统访问日志"
)
async def get_oper_log(
        username: str,
        orderBy: str,
        orderType: str,
        pageSize: int,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    total = await getOperLog.get_number(db)
    result = await getOperLog.get_multi(
        db, orderBy="login_time", orderType="desc", pageIndex=1, pageSize=pageSize
    )
    result = [res for res in result if res["username"] == username and result]
    return resp_200(data={"items": result, "pageInfo": {
            "total": total, "currentPage": 1, "totalPage": page_total(total, pageSize)
        }
    })


@router.get(
    path="/system/common/getUserList",
    response_model=Result,
    summary="获取用户列表"
)
async def get_user_list(
        page: int, pageSize: int,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        dept_id: Optional[str] = "", role_id: Optional[str] = "", post_id: Optional[str] = "", status: Optional[str] = "",
        username: Optional[str] = "", nickname: Optional[str] = "", phone: Optional[str] = "", email: Optional[str] = "",
        maxDate: Optional[str] = "",  minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getUser.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj={
            "phone": phone, "email": email, "nickname": nickname, "username": username,
            "status": status, "maxDate": maxDate, "minDate": minDate
        }, dept_id=dept_id, delete="0"
    ))