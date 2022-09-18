# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Result, Token, Role, BaseRole, DeleteIds, ChangeSort, ChangeStatus, RoleDataScope
from backend.models import UserDept
from backend.crud import CRUDBase, getRole
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis
from utils import resp_200

router = APIRouter()

@router.get(path="/system/role/list", response_model=Result, summary="获取角色列表")
async def get_role_list(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getRole.userRole(db, user_id=token["id"]))

@router.get(path="/system/role/index", response_model=Result, summary="获取角色分页列表")
async def get_role_page(
    page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "",
    name: Optional[str] = "", code: Optional[str] = "", status: Optional[str] = "",
    maxDate: Optional[str] = "", minDate: Optional[str] = "",
    db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    total = await getRole.get_number(db)
    result = await getRole.getQuery(db, pageIndex=page, pageSize=pageSize, query_obj={"code": code, "name": name, "status": status, "maxDate": maxDate, "minDate": minDate})
    return resp_200(data={"items": result, "pageInfo": {"total": total, "currentPage": page, "totalPage": page_total(total, pageSize)}})

@router.get(path="/system/role/recycle", response_model=Result, summary="获取被删除角色分页列表")
async def get_role_page(
    page: int, pageSize: int, orderBy: Optional[str] = "", orderType: Optional[str] = "",
    name: Optional[str] = "", code: Optional[str] = "", status: Optional[str] = "",
    maxDate: Optional[str] = "", minDate: Optional[str] = "",
    db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    total = await getRole.get_number(db)
    result = await getRole.getQueryReclcle(db, pageIndex=page, pageSize=pageSize, query_obj={"code": code, "name": name, "status": status, "maxDate": maxDate, "minDate": minDate})
    return resp_200(data={"items": result, "pageInfo": {"total": total, "currentPage": page, "totalPage": page_total(total, pageSize)}})

@router.post(path="/system/role/save", response_model=Result, summary="添加角色")
async def save_role(role: BaseRole, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getRole.create(db, obj_in=role.dict())
    return resp_200(msg="添加成功")

@router.put(path="/system/role/update/{id:path}", response_model=Result, summary="编辑角色")
async def update_role(id: int, role: BaseRole, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getRole.update(db, id, obj_in=role.dict())
    return resp_200(msg="编辑成功")

@router.put(path="/system/role/changeStatus", response_model=Result, summary="修改角色状态")
async def change_status_dept(role: ChangeStatus, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getRole.update(db, id=role.id, obj_in={"status": role.status})
    return resp_200(msg="修改成功")

@router.delete(path="/system/role/delete", response_model=Result, summary="删除角色[逻辑删除]")
async def delete_role(role: DeleteIds, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for id in role.ids: await getRole.tombstone(db, id)
    return resp_200(msg="删除成功")

@router.put(path="/system/role/numberOperation", response_model=Result, summary="修改角色列表排序")
async def num_operation_dept(role: ChangeSort, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getRole.getChangeSort(db, obj_in=role.dict())
    return resp_200(msg="修改成功")

@router.get(path="/system/role/getDeptByRole/{id:path}", response_model=Result, summary="获取数据权限")
async def get_dept_by_role(id: int, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    result = await getRole.get_all(db)
    dept_list = [{"id": id, "depts": [{"id": int(dept_id), "pivot": {"role_id": id, "dept_id": int(dept_id)}} for item in result for dept_id in str(item["dept_ids"]).split(",") if dept_id]}]
    return resp_200(data=dept_list)

@router.put(path="/system/role/dataPermission/{id:path}", response_model=Result, summary="保存角色数据")
async def update_dept_by_role(id: int, role: RoleDataScope, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    if role.dept_ids:
        for dept in role.dept_ids: await getRole.update(db, id, obj_in={"data_scope": role.data_scope, "dept_ids": str(dept)})
    return resp_200(msg="保存成功")