# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Request, Security, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders
from typing import Optional
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import time
import os

from utils import resp_200, resp_400, resp_500, resp_404, resf_200, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user, page_total
from backend.crud import getUser, getDept, getPost, getRole
from backend.core import check_jwt_token
from backend.scheams import (
    Token, Result, Account, AccountUpdate,
    ModifyPassword, BackendSetting, UserIDList,
    UserHome, UserId, QueryUser, ChangeSort,
    ChangeStatus, Ids
)
from backend.db import MyRedis

router = APIRouter()


@router.get(path="/system/getInfo", response_model=Result, summary="获取用户信息")
async def user_info(request: Request, token: str = Depends(check_jwt_token), db: AsyncSession = Depends(get_db)):
    user = await getUser.getUserInfo(db, token)
    routers = await getUser.getUserRouters(db, user)
    user["backend_setting"] = await getUser.getUserSetting(db, user)
    return resp_200(data={"codes": routers["codes"], "roles": [user["userId"]], "routers": routers["menus"],
                          "user": user})


@router.post(path="/system/user/updateInfo", response_model=Result, summary="更新用户信息")
async def update_user(user: AccountUpdate, token: str = Depends(check_jwt_token), db: AsyncSession = Depends(get_db)):
    if await getUser.update(db, id=user.id, obj_in=user.dict()): return resp_200(msg="更新成功")


@router.post(path="/system/user/modifyPassword", response_model=Result, summary="更新密码")
async def modify_password(paw: ModifyPassword, token: str = Depends(check_jwt_token),
                          db: AsyncSession = Depends(get_db)):
    if await getUser.updatePassword(db, paw=paw.dict(), user_id=token["id"]): return resp_200(msg="密码已更新")
    return resp_400(msg="密码验证错误，请重新输入")


@router.post(path="/user/updateSetting", response_model=Result, summary="更新系统设置")
async def update_setting(setting: BackendSetting, token: str = Depends(check_jwt_token),
                         db: AsyncSession = Depends(get_db)):
    if await getUser.updateSetting(db, obj_in=setting.dict(), user_id=token["id"]): return resp_200(msg="设置更新成功！")


@router.get(path="/user/userDetail/{user_id:path}", response_model=Result, summary="获取用户详情")
async def get_user_detail(user_id: int, token: str = Depends(check_jwt_token), db: AsyncSession = Depends(get_db)):
    result = await getUser.get(db, id=user_id)
    result["backend_setting"] = await getUser.getUserSetting(db, user=result)
    result["dept_id"] = await getDept.userDept(db, user_id)
    result["roleList"] = await getRole.userRole(db, user_id)
    result["postList"] = await getPost.userPost(db, user_id)
    return resp_200(data=result)


@router.post(path="/system/user/save", response_model=Result, summary="添加用户")
async def save_user(user: Account, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    user_data = user.dict()
    del user_data["post_ids"], user_data["role_ids"], user_data["dept_id"]
    new_user_id = await getUser.create(db, obj_in=user_data)
    for post_id in user.post_ids: await getPost.createRelation(db, obj_in={"user_id": new_user_id, "post_id": post_id})
    for role_id in user.role_ids: await getRole.createRelation(db, obj_in={"user_id": new_user_id, "role_id": role_id})
    await getDept.createRelation(db, obj_in={"user_id": new_user_id, "dept_id": user.dept_id})
    return resp_200(msg="创建成功")


@router.put(path="/system/user/update/{id:path}", response_model=Result, summary="保存用户")
async def save_user(id: int, user: Account, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getPost.removeRelation(db, user_id=id), getRole.removeRelation(db, user_id=id), \
                                                  getPost.removeRelation(db, user_id=id)
    for post_id in user.post_ids: await getPost.createRelation(db, obj_in={"user_id": id, "post_id": post_id})
    for role_id in user.role_ids: await getRole.createRelation(db, obj_in={"user_id": id, "role_id": role_id})
    await getDept.createRelation(db, obj_in={"user_id": id, "dept_id": user.dict()["dept_id"]})
    return resp_200(msg="创建成功")


@router.delete(path="/system/user/delete", response_model=Result, summary="删除用户[逻辑删除]")
async def delete_user(user: UserIDList, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for id in user.ids: await getUser.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.get(path="/system/user/read/{id:path}", response_model=Result, summary="获取用户详情")
async def get_user_detail(id: int, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getUser.get(db, id))


@router.post(path="/system/user/clearCache", response_model=Result, summary="清理用户缓存")
async def clear_cache_user(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await db.flush()
    return resp_200(msg="已清除缓存")


@router.put(path="/system/user/changeStatus", response_model=Result, summary="修改用户状态")
async def change_status(user: ChangeStatus, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getUser.update(db, id=user.id, obj_in={"status": user.status})
    return resp_200(msg="修改成功")


@router.post(path="/system/user/export", response_model=Result, summary="导出用户")
async def export_user(page: int = Body(...), pageSize: int = Body(...), db: AsyncSession = Depends(get_db),
                      token: str = Depends(check_jwt_token)):
    result = await getUser.get_multi(db, pageIndex=page, pageSize=pageSize)
    data = []
    for item in result: data.append([item[k] for k in item])
    wb = Workbook()
    ws = wb.active
    ws.title = "user"
    for i in dataframe_to_rows(pd.DataFrame(data=data, columns=[str(k) for k in result[0].keys()])): ws.append(i)
    save_file_name = os.path.abspath(os.path.join(os.getcwd(), "..")) \
                     + "/static/user_file_export/" + str(int(time.time()))
    wb.save(save_file_name + ".xls")
    return resf_200(filename=str(int(time.time())), path=save_file_name + '.xls')


@router.post(path="/system/user/downloadTemplate", response_model=Result, summary="下载导出用户模板")
async def down_user_template(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resf_200(
        path=os.path.abspath(os.path.join(os.getcwd(), "..")) + "/static/user_file_export/template_user.xls")


@router.post(path="/system/user/setHomePage", response_model=Result, summary="设置用户首页")
async def set_home_user(user: UserHome, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getUser.update(db, id=user.id, obj_in=user.dict())
    return resp_200(msg="设置成功")


@router.put(path="/system/user/initUserPassword", response_model=Result, summary="重制用户密码 ：123456")
async def init_password(user: UserId, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getUser.update(db, id=user.id, obj_in={"password": "123456"})
    return resp_200(msg="密码已充值")


@router.put(path="/system/user/recovery", response_model=Result, summary="恢复被删除的数据")
async def recovery_user(user: Ids, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for ids in user.ids: await getUser.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(path="/system/user/index", response_model=Result, summary="分页获取系统用户列表")
async def get_user_page(page: int, pageSize: int,
                        orderBy: Optional[str] = "",
                        orderType: Optional[str] = "",
                        dept_id: Optional[str] = "",
                        role_id: Optional[str] = "",
                        post_id: Optional[str] = "",
                        username: Optional[str] = "",
                        nickname: Optional[str] = "",
                        phone: Optional[str] = "",
                        email: Optional[str] = "",
                        maxDate: Optional[str] = "",
                        minDate: Optional[str] = "",
                        status: Optional[str] = "",
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(check_jwt_token)):
    query_obj = {"phone": phone, "email": email, "nickname": nickname, "username": username, "status": status,
                 "maxDate": maxDate, "minDate": minDate}
    result = await getUser.getQuery(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj, dept_id=dept_id)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page,
                                                                "totalPage": result["page_total"]}})


@router.get(path="/system/user/recycle", response_model=Result, summary="展示回收站用户")
async def recycle_user(page: int, pageSize: int,
                       orderBy: Optional[str] = "",
                       orderType: Optional[str] = "",
                       dept_id: Optional[str] = "",
                       role_id: Optional[str] = "",
                       post_id: Optional[str] = "",
                       username: Optional[str] = "",
                       nickname: Optional[str] = "",
                       phone: Optional[str] = "",
                       email: Optional[str] = "",
                       maxDate: Optional[str] = "",
                       minDate: Optional[str] = "",
                       status: Optional[str] = "",
                       db: AsyncSession = Depends(get_db),
                       token: str = Depends(check_jwt_token)):
    query_obj = {"phone": phone, "email": email, "nickname": nickname, "username": username, "status": status,
                 "maxDate": maxDate, "minDate": minDate}
    result = await getUser.getQueryReclcle(db, pageIndex=page, pageSize=pageSize, query_obj=query_obj, dept_id=dept_id)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page,
                                                                "totalPage": result["page_total"]}})
