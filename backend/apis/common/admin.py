# -*- coding: utf-8 -*-

import os
import time
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, Body, UploadFile, File
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db
from backend.core import check_jwt_token, get_password_hash
from backend.crud import getUser, getDept, getPost, getRole
from backend.scheams import (
    Result, Account, AccountUpdate,
    ModifyPassword, BackendSetting, UserIDList,
    UserHome, UserId, ChangeStatus, Ids
)
from utils import resp_200, resp_400, resf_200

router = APIRouter()


@router.get(
    path="/system/getInfo",
    response_model=Result,
    summary="获取用户信息"
)
async def user_info(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    user = await getUser.getUserInfo(db, token)
    routers = await getUser.getUserRouters(db, user)
    user.setdefault("backend_setting", await getUser.getUserSetting(db, user))
    return resp_200(
        data={
            "codes": routers["codes"],
            "roles": [user["userId"]],
            "routers": routers["menus"],
            "user": user
        }
    )


@router.post(
    path="/system/user/updateInfo",
    response_model=Result,
    summary="更新用户信息"
)
async def update_user(
        user: AccountUpdate,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    if await getUser.update(db, id=user.id, obj_in=user.dict()):
        return resp_200(msg="更新成功")


@router.post(
    path="/system/user/modifyPassword",
    response_model=Result,
    summary="更新密码"
)
async def modify_password(
        password: ModifyPassword,
        token: str = Depends(check_jwt_token),
        db: AsyncSession = Depends(get_db)
):
    if await getUser.updatePassword(db, password=password.dict(), user=token):
        return resp_200(msg="密码已更新")
    return resp_400(msg="密码验证错误，请重新输入")


@router.post(
    path="/user/updateSetting",
    response_model=Result,
    summary="更新系统设置"
)
async def update_setting(
        setting: BackendSetting,
        token: str = Depends(check_jwt_token),
        db: AsyncSession = Depends(get_db)
):
    if await getUser.updateSetting(db, obj_in=setting.dict(), user_id=token["id"]):
        return resp_200(msg="设置更新成功！")


@router.get(
    path="/user/userDetail/{user_id:path}",
    response_model=Result,
    summary="获取用户详情"
)
async def get_user_detail(
        user_id: int, token:
        str = Depends(check_jwt_token),
        db: AsyncSession = Depends(get_db)
):
    result = {}
    result = await getUser.get(db, id=user_id)
    result.setdefault("backend_setting", await getUser.getUserSetting(db, user=result))
    result.setdefault("dept_id", await getDept.userDept(db, user_id))
    result.setdefault("roleList", await getRole.userRole(db, user_id))
    result.setdefault("postList", await getPost.userPost(db, user_id))
    print("result", result)
    return resp_200(data=result)


@router.post(
    path="/system/user/save",
    response_model=Result,
    summary="添加用户"
)
async def save_user(
        user: Account,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    user_data = user.dict()
    user_data.setdefault("password", get_password_hash(user_data["password"]))
    for key in ["post_ids", "role_ids", "dept_id"]: user_data.pop(key)
    new_user_id = await getUser.create(db, user_data)
    if user.post_ids:
        create_relation_post = [{"user_id": new_user_id, "post_id": post_id} for post_id in user.post_ids]
        await getPost.createRelation(db, *create_relation_post)
    if user.role_ids:
        create_relation_role = [{"user_id": new_user_id, "role_id": role_id} for role_id in user.role_ids]
        await getRole.createRelation(db, *create_relation_role)
    await getDept.createRelation(db, {"user_id": new_user_id, "dept_id": user.dept_id})
    return resp_200(msg="创建成功")


@router.put(
    path="/system/user/update/{id:path}",
    response_model=Result,
    summary="保存用户"
)
async def update_user(
        id: int,
        user: Account,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getPost.removeRelation(db, id), getRole.removeRelation(db, id), getPost.removeRelation(db, id)
    user_data = user.dict()
    user_data.setdefault("password", get_password_hash(user_data["password"]))
    await getUser.update(db, id, obj_in=user_data)
    if user.post_ids:
        update_post_result = [{"user_id": id, "post_id": post_id} for post_id in user.post_ids]
        await getPost.createRelation(db, *update_post_data)
    if user.role_ids:
        update_role_result = [{"user_id": id, "role_id": role_id} for role_id in user.role_ids]
        await getRole.createRelation(db, *update_role_data)
    if user.dept_id:
        await getDept.createRelation(db, {"user_id": id, "dept_id": user.dept_id})
    return resp_200(msg="创建成功")


@router.delete(
    path="/system/user/delete",
    response_model=Result,
    summary="删除用户[逻辑删除]"
)
async def delete_user(
        user: UserIDList,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for id in user.ids:
        await getUser.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.get(
    path="/system/user/read/{id:path}",
    response_model=Result,
    summary="获取用户详情"
)
async def get_user_detail(
        id: int, db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getUser.get(db, id))


@router.post(
    path="/system/user/clearCache",
    response_model=Result,
    summary="清理用户缓存"
)
async def clear_cache_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await db.flush()
    return resp_200(msg="已清除缓存")


@router.put(
    path="/system/user/changeStatus",
    response_model=Result,
    summary="修改用户状态"
)
async def change_status(
        user: ChangeStatus,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getUser.update(db, id=user.id, obj_in={"status": user.status})
    return resp_200(msg="修改成功")


@router.post(
    path="/system/user/export",
    response_model=Result,
    summary="导出用户"
)
async def export_user(
        page: int = Body(...),
        pageSize: int = Body(...),
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
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


@router.post(
    path="/system/user/import",
    summary="导入用户"
)
async def import_user(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    pass


@router.post(
    path="/system/user/downloadTemplate",
    response_model=Result,
    summary="下载导出用户模板"
)
async def down_user_template(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resf_200(
        path=os.path.abspath(os.path.join(os.getcwd(), "..")) + "/static/user_file_export/template_user.xls"
    )


@router.post(
    path="/system/user/setHomePage",
    response_model=Result,
    summary="设置用户首页"
)
async def set_home_user(
        user: UserHome,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getUser.update(db, id=user.id, obj_in=user.dict())
    return resp_200(msg="设置成功")


@router.put(
    path="/system/user/initUserPassword",
    response_model=Result,
    summary="重制用户密码 ：123456"
)
async def init_password(
        user: UserId,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getUser.update(db, id=user.id, obj_in={"password": get_password_hash("123456")})
    return resp_200(msg="密码已充值")


@router.put(
    path="/system/user/recovery",
    response_model=Result,
    summary="恢复被删除的数据"
)
async def recovery_user(
        user: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for ids in user.ids:
        await getUser.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(
    path="/system/user/index",
    response_model=Result,
    summary="分页获取系统用户列表"
)
async def get_user_page(
        page: int, pageSize: int,
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
        token: str = Depends(check_jwt_token)
):
    result = await getUser.getQuery(
        db,
        pageIndex=page,
        pageSize=pageSize,
        queryObj={
            "phone": phone,
            "email": email,
            "nickname": nickname,
            "username": username,
            "status": status,
            "maxDate": maxDate,
            "minDate": minDate
        },
        dept_id=dept_id,
        delete="0"
    )
    return resp_200(data={
        "items": result["data"],
        "pageInfo": {
            "total": result["total"],
            "currentPage": page,
            "totalPage": result["page_total"]
        }
    })


@router.get(
    path="/system/user/recycle",
    response_model=Result,
    summary="展示回收站用户"
)
async def recycle_user(
        page: int, pageSize: int,
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
        token: str = Depends(check_jwt_token)
):
    result = await getUser.getQuery(
        db,
        pageIndex=page,
        pageSize=pageSize,
        queryObj={
            "phone": phone,
            "email": email,
            "nickname": nickname,
            "username": username,
            "status": status,
            "maxDate": maxDate,
            "minDate": minDate
        },
        dept_id=dept_id,
        delete="1"
    )
    return resp_200(data={
        "items": result["data"],
        "pageInfo": {
            "total": result["total"],
            "currentPage": page,
            "totalPage": result["page_total"]
        }
    })

