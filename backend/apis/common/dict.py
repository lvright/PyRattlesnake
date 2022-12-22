# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db, check_jwt_token
from backend.crud import getDictData, getDictType
from backend.scheams import Result, DictDate, DictClassify, ChangeStatus, Ids, ChangeSort
from utils import resp_200

router = APIRouter()


@router.get(
    path="/system/dataDict/list",
    response_model=Result,
    summary="获取数据字典值"
)
async def get_dict_type(
        code: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getDictData.getByCode(db, code=code))


@router.put(
    path="/system/dictType/update/{id:path}",
    response_model=Result,
    summary="编辑数据字典分类"
)
async def update_dict_data(
        id: int,
        dict_type: DictClassify,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictType.update(db, id, obj_in=dict_type.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/dictType/update/{id:path}",
    response_model=Result,
    summary="保存字典类型"
)
async def update_dict_type(
        id: int,
        dict_type: DictClassify,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictType.update(db, id, obj_in=dict_type.dict())
    return resp_200(msg="保存成功")


@router.post(
    path="/system/dictType/save",
    response_model=Result,
    summary="添加字典类型"
)
async def save_dict_type(
        dict_type: DictClassify,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictType.create(db, obj_in=dict_type.dict())
    return resp_200(msg="添加成功")


@router.put(
    path="/system/dictType/changeStatus",
    response_model=Result,
    summary="修改字典类型状态"
)
async def change_status_dict_type(
        dict_type: ChangeStatus,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictType.update(db, id=dict_type.id, obj_in={"status": dict_type.status})
    return resp_200(msg="修改成功")


@router.delete(
    path="/system/dictType/delete",
    response_model=Result,
    summary="删除字典类型[逻辑删除]"
)
async def delete_dict_type(
        dict_type: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for id in dict_type.ids:
        await getDictType.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.put(
    path="/system/dictType/numberOperation",
    response_model=Result,
    summary="修改字典类型列表排序"
)
async def sort_operation_dict_type(
        dict_type: ChangeSort,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictType.getChangeSort(db, obj_in=dict_type.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/dataDict/update/{id:path}",
    response_model=Result,
    summary="编辑数据字典"
)
async def update_dict_data(
        id: int, dict_data: DictDate,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictData.update(db, id, obj_in=dict_data.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/dataDict/update/{id:path}",
    response_model=Result,
    summary="保存数据字典"
)
async def update_dict_data(
        id: int,
        dict_data: DictDate,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictData.update(db, id, obj_in=dict_data.dict())
    return resp_200(msg="保存成功")


@router.post(
    path="/system/dataDict/save",
    response_model=Result,
    summary="添加数据字典"
)
async def save_dict_data(
        dict_data: DictDate,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictData.create(db, obj_in=dict_data.dict())
    return resp_200(msg="添加成功")


@router.put(
    path="/system/dataDict/changeStatus",
    response_model=Result,
    summary="修改数据字典状态"
)
async def change_dict_data(
        dict_data: ChangeStatus,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictData.changeStatus(db, id=dict_data.id, status=dict_data.status)
    return resp_200(msg="修改成功")


@router.delete(
    path="/system/dataDict/delete",
    response_model=Result,
    summary="删除数据字典[逻辑删除]"
)
async def delete_dict_data(
        dict_data: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for id in dict_data.ids:
        await getDictData.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.put(
    path="/system/dataDict/numberOperation",
    response_model=Result,
    summary="修改数据字典列表排序"
)
async def sort_operation_dict_data(
        dict_data: ChangeSort,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDictData.getChangeSort(db, obj_in=dict_data.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/dataDict/recovery",
    response_model=Result,
    summary="恢复字典类型被删除的数据"
)
async def recovery_dict_data(
        dict_data: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for ids in dict_data.ids:
        await getDictData.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.put(
    path="/system/dictType/recovery",
    response_model=Result,
    summary="恢复字典数据被删除的数据"
)
async def recovery_dict_type(
        dict_type: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for ids in dict_type.ids:
        await getDictType.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(
    path="/system/dictType/index",
    response_model=Result,
    summary="获取数据典类型分页列表"
)
async def get_dict_type_page(
        page: int, pageSize: int,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        name: Optional[str] = "", code: Optional[str] = "", status: Optional[str] = "",
        maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    queryData = {
        "name": name, "code": code, "status": status,
        "maxDate": maxDate, "minDate": minDate
    }
    return resp_200(data=await getDictType.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj=queryData, delete="0"
    ))


@router.get(
    path="/system/dictType/recycle",
    response_model=Result,
    summary="获取被删除获取数据典类型分页列表"
)
async def recycle_dict_type(
        page: int, pageSize: int,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        name: Optional[str] = "", code: Optional[str] = "", status: Optional[str] = "",
        maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    queryData = {
        "name": name, "code": code, "status": status,
        "maxDate": maxDate, "minDate": minDate
    }
    return resp_200(data=await getDictType.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj=queryData, delete="1"
    ))


@router.get(
    path="/system/dataDict/index",
    response_model=Result,
    summary="获取数据典分页列表"
)
async def get_dict_data_page(
        page: int, pageSize: int,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        name: Optional[str] = "", code: Optional[str] = "", type_id: Optional[int] = "", status: Optional[str] = "",
        maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    queryData = {
        "name": name, "code": code, "status": status,
        "type_id": type_id, "maxDate": maxDate, "minDate": minDate
    }
    return resp_200(data=await getDictData.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj=queryData, delete="0"
    ))


@router.get(
    path="/system/dataDict/recycle",
    response_model=Result,
    summary="获取被删除获取数据典分页列表"
)
async def recycle_dict_data(
        page: int, pageSize: int,
        orderBy: Optional[str] = "", orderType: Optional[str] = "",
        name: Optional[str] = "", code: Optional[str] = "", type_id: Optional[int] = "", status: Optional[str] = "",
        maxDate: Optional[str] = "", minDate: Optional[str] = "",
        db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)
):
    queryData = {
        "name": name, "code": code, "status": status,
        "type_id": type_id, "maxDate": maxDate, "minDate": minDate
    }
    return resp_200(data=await getDictData.getQuery(
        db, pageIndex=page, pageSize=pageSize, queryObj=queryData, delete="1"
    ))