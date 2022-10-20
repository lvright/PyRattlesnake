# -*- coding: utf-8 -*-

import celery
from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders
from typing import Optional

from utils import resp_200, resp_400, resp_500, resp_404, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user, page_total
from backend.crud import getLoginLog, getOperLog, getBackendSetting, getDept, getRole, getPost, getUser
from backend.core import check_jwt_token
from backend.scheams import Token, Result, BackendSetting, Ids
from backend.db import MyRedis

router = APIRouter()


@router.put(path="/system/common/saveSysSetting", response_model=Result, summary="更新系统配置")
async def update_backend_setting(backend_setting: BackendSetting, db: AsyncSession = Depends(get_db),
                                 token: str = Depends(check_jwt_token)):
    await getBackendSetting.updateBackendSetting(db, user_id=token["id"], obj_in=backend_setting.dict())
    return resp_200(msg="更新成功")


@router.get(path="/system/common/getDeptTreeList", response_model=Result, summary="获取树状部门")
async def get_tree_dept(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getDept.deptTree(db))


@router.get(path="/system/common/getRoleList", response_model=Result, summary="获取角色列表")
async def get_role_list(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getRole.get_all(db))


@router.get(path="/system/common/getPostList", response_model=Result, summary="获取部门列表")
async def get_post_list(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getPost.get_all(db))


@router.post(path="/system/common/getUserInfoByIds", response_model=Result, summary="获取接收信息用户")
async def get_user_by_id(user: Ids, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    result = []
    for user_id in user.ids: result.append(await getUser.get(db, user_id))
    return resp_200(data=result)


@router.post(path="/system/uploadImage", response_model=Result, summary="上传图片文件")
async def upload_image(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    pass


@router.get(path="/system/common/getLoginLogList", response_model=Result, summary="系统登录日志")
async def get_login_log(username: str, orderBy: str, orderType: str, pageSize: int, db: AsyncSession = Depends(get_db),
                        token: str = Depends(check_jwt_token)):
    total = await getLoginLog.get_number(db)
    result = await getLoginLog.get_multi(db, orderBy="login_time", orderType="desc", pageIndex=1, pageSize=pageSize)
    result = [res for res in result if res["username"] == username and res]
    return resp_200(data={"items": result,
                          "pageInfo": {"total": total, "currentPage": 1, "totalPage": page_total(total, pageSize)}})


@router.get(path="/system/common/getOperationLogList", response_model=Result, summary="系统登录日志")
async def get_oper_log(username: str, orderBy: str, orderType: str, pageSize: int, db: AsyncSession = Depends(get_db),
                       token: str = Depends(check_jwt_token)):
    total = await getOperLog.get_number(db)
    result = await getOperLog.get_multi(db, orderBy="login_time", orderType="desc", pageIndex=1, pageSize=pageSize)
    result = [res for res in result if res["username"] == username and result]
    return resp_200(data={"items": result,
                          "pageInfo": {"total": total, "currentPage": 1, "totalPage": page_total(total, pageSize)}})


@router.get(path="/system/common/getUserList", response_model=Result, summary="获取用户列表")
async def get_user_list(page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "",
                        dept_id: Optional[str] = "",role_id: Optional[str] = "", post_id: Optional[str] = "",
                        username: Optional[str] = "",nickname: Optional[str] = "",phone: Optional[str] = "",
                        email: Optional[str] = "", maxDate: Optional[str] = "", minDate: Optional[str] = "",
                        status: Optional[str] = "", db: AsyncSession = Depends(get_db),
                        token: str = Depends(check_jwt_token)):
    query_obj = {"phone": phone, "email": email, "nickname": nickname, "username": username, "status": status,
                 "maxDate": maxDate, "minDate": minDate}
    result = await getUser.getQuery(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj, dept_id=dept_id)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page,
                                                                "totalPage": result["page_total"]}})
