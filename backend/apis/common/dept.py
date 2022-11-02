# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db
from backend.core import check_jwt_token
from backend.crud import getDept
from backend.scheams import Result, DeptStructure, ChangeStatus, Ids, ChangeSort
from utils import resp_200

router = APIRouter()


@router.get(
    path="/system/dept/tree",
    response_model=Result,
    summary="获取树状部门"
)
async def get_tree_dept(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getDept.deptTree(db))


@router.post(
    path="/system/dept/save",
    response_model=Result,
    summary="添加部门"
)
async def save_dept(
        dept: DeptStructure,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDept.create(db, obj_in=dept.dict())
    return resp_200(msg="添加成功")


@router.put(
    path="/system/dept/update/{id:path}",
    response_model=Result,
    summary="保存部门"
)
async def update_dept(
        id: int,
        dept: DeptStructure,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDept.update(db, id, obj_in=dept.dict())
    return resp_200(msg="保存成功")


@router.put(
    path="/system/dept/changeStatus",
    response_model=Result,
    summary="修改部门状态"
)
async def change_status_dept(
        dept: ChangeStatus,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDept.update(db, dept.id, obj_in={"status": dept.status})
    return resp_200(msg="修改成功")


@router.delete(
    path="/system/dept/delete",
    response_model=Result,
    summary="删除部门[逻辑删除]"
)
async def delete_dept(
        dept: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for id in dept.ids:
        await getDept.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.put(
    path="/system/dept/numberOperation",
    response_model=Result,
    summary="修改部门列表排序"
)
async def sort_operation_dept(
        dept: ChangeSort,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getDept.getChangeSort(db, obj_in=dept.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/dept/recovery",
    response_model=Result,
    summary="恢复被删除的数据"
)
async def recovery_dept(
        dept: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for ids in dept.ids:
        await getDept.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(
    path="/system/dept/index",
    response_model=Result,
    summary="获取部门分页列表"
)
async def get_dept_page(
        page: int, pageSize: int,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        name: Optional[str] = "",
        leader: Optional[str] = "",
        phone: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        status: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getDept.getQuery(
        db,
        pageIndex=page,
        pageSize=pageSize,
        queryObj={
            "name": name,
            "leader": leader,
            "phone": phone,
            "status": status,
            "maxDate": maxDate,
            "minDate": minDate
        },
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
    path="/system/dept/recycle",
    response_model=Result,
    summary="获取被删除部门分页列表"
)
async def recycle_dept(
        page: int, pageSize: int,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        name: Optional[str] = "",
        leader: Optional[str] = "",
        phone: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        status: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getDept.getQuery(
        db,
        pageIndex=page,
        pageSize=pageSize,
        queryObj={
            "name": name,
            "leader": leader,
            "phone": phone,
            "status": status,
            "maxDate": maxDate,
            "minDate": minDate
        },
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
