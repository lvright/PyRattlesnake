# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi import APIRouter, Depends, Request, Security
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import MutableHeaders

from utils import resp_200, resp_400, resp_500, by_ip_get_address, ErrorUser
from backend.apis.deps import get_redis, get_db, get_current_user, check_jwt_token, page_total
from backend.crud import getDictData, getDictType
from backend.scheams import Token, Result, DictDate, DictClassify
from backend.db import MyRedis

router = APIRouter()

@router.get(path="/system/dataDict/list", summary="获取数据字典值")
async def get_dict_type(code: Optional[str] = None, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getDictData.getByCode(db, code=code))

@router.get(path="/system/dataDict/index", summary="分页获取数据字典数据")
async def get_dict_type(page: int, pageSize: int, type_id: Optional[int] = None, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    data = await getDictData.get_multi(db, pageIndex=page, pageSize=pageSize)
    total = await getDictData.get_number(db)
    return resp_200(data={"items": data, "pageInfo": {"total": total, "currentPage": page, "totalPage": page_total(total, pageSize)}})

@router.get(path="/system/dictType/index", summary="分页获取数据字典类型")
async def get_dict_type(page: int, pageSize: int, type_id: Optional[int] = None, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    data = await getDictType.get_multi(db, pageIndex=page, pageSize=pageSize)
    total = await getDictType.get_number(db)
    return resp_200(data={"items": data, "pageInfo": {"total": total, "currentPage": page, "totalPage": page_total(total, pageSize)}})

@router.put(path="/system/dictType/update/{id:path}", response_model=Result, summary="编辑数据字典分类")
async def update_dict_type(dict_type: DictClassify, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await getDictType.update(db, id, obj_in=dict_type.dict())
    return resp_200(msg="修改成功")

