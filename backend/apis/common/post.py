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
from backend.scheams import Result, Token, PostStructure, ChangeSort, ChangeStatus, Ids
from backend.models import post
from backend.crud import CRUDBase, getPost
from backend.apis.deps import get_db, get_current_user, get_redis, page_total
from backend.db import MyRedis
from utils import resp_200

router = APIRouter()


@router.get(
    path="/system/post/list",
    response_model=Result,
    summary="获取岗位列表"
)
async def get_post_list(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getPost.userPost(db, user_id=token["id"]))


@router.post(
    path="/system/post/save",
    response_model=Result,
    summary="添加岗位"
)
async def save_post(
        post: PostStructure,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getPost.create(db, obj_in=post.dict())
    return resp_200(msg="添加成功")


@router.put(
    path="/system/post/update/{id:path}",
    response_model=Result,
    summary="保存岗位"
)
async def update_post(
        id: int, post: PostStructure,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getPost.update(db, id, obj_in=post.dict())
    return resp_200(msg="保存成功")


@router.put(
    path="/system/post/changeStatus",
    response_model=Result,
    summary="修改岗位状态"
)
async def change_status_post(
        post: ChangeStatus,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getPost.update(db, id=post.id, obj_in={"status": post.status})
    return resp_200(msg="修改成功")


@router.delete(
    path="/system/post/delete",
    response_model=Result,
    summary="删除岗位[逻辑删除]"
)
async def delete_post(
        post: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for id in post.ids:
        await getPost.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.put(
    path="/system/post/numberOperation",
    response_model=Result,
    summary="修改岗位列表排序"
)
async def sort_operation_dept(
        post: ChangeSort,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getPost.getChangeSort(db, obj_in=post.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/post/recovery",
    response_model=Result,
    summary="恢复被删除的数据"
)
async def recovery_post(
        post: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for ids in post.ids: await getPost.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(
    path="/system/post/index",
    response_model=Result,
    summary="获取岗位分页数据"
)
async def get_post_page(
        page: int, pageSize: int,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        name: Optional[str] = "",
        code: Optional[str] = "",
        status: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    queryData = {"code": code, "name": name, "status": status, "maxDate": maxDate, "minDate": minDate}
    return resp_200(data=await getPost.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj=queryData, delete="0"
    ))


@router.get(
    path="/system/post/recycle",
    response_model=Result,
    summary="获取岗位逻辑删除分页数据"
)
async def get_post_page(
        page: int, pageSize: int,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        name: Optional[str] = "",
        code: Optional[str] = "",
        status: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    queryData = {"code": code, "name": name, "status": status, "maxDate": maxDate, "minDate": minDate}
    return resp_200(data=await getPost.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj=queryData, delete="1"
    ))