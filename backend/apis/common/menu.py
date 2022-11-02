# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db
from backend.core import check_jwt_token
from backend.crud import getMenu
from backend.scheams import Result, ChangeSort, ChangeStatus, Ids, MenuStructure
from utils import resp_200

router = APIRouter()


@router.get(
    path="/system/menu/tree",
    response_model=Result,
    summary="获取树状菜单"
)
async def get_tree_menu(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    return resp_200(data=await getMenu.menuTree(db))


@router.put(
    path="/system/menu/update/{id:path}",
    response_model=Result,
    summary="保存菜单"
)
async def update_menu(
        id: int, menu: MenuStructure,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getMenu.update(db, id, obj_in=menu.dict())
    return resp_200(msg="保存成功")


@router.post(
    path="/system/menu/save",
    response_model=Result,
    summary="添加菜单"
)
async def save_menu(
        menu: MenuStructure,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getMenu.create(db, obj_in=menu.dict())
    return resp_200(msg="添加成功")


@router.put(
    path="/system/menu/changeStatus",
    response_model=Result,
    summary="修改菜单状态"
)
async def change_status_menu(
        menu: ChangeStatus,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getMenu.update(db, id=menu.id, obj_in={"status": menu.status})
    return resp_200(msg="修改成功")


@router.delete(
    path="/system/menu/delete",
    response_model=Result,
    summary="删除菜单[逻辑删除]"
)
async def delete_menu(
        menu: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for id in menu.ids:
        await getMenu.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.put(
    path="/system/menu/numberOperation",
    response_model=Result,
    summary="修改菜单列表排序"
)
async def sort_operation_menu(
        menu: ChangeSort,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    await getMenu.getChangeSort(db, obj_in=menu.dict())
    return resp_200(msg="修改成功")


@router.put(
    path="/system/menu/recovery",
    response_model=Result,
    summary="恢复被删除的数据"
)
async def recovery_menu(
        menu: Ids,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    for ids in menu.ids:
        await getMenu.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(
    path="/system/menu/index",
    response_model=Result,
    summary="获取菜单分页列表"
)
async def get_menu_page(
        page: int, pageSize: int,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        name: Optional[str] = "",
        title: Optional[str] = "",
        hidden: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        status: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getMenu.getQuery(
        db,
        pageIndex=page,
        pageSize=pageSize,
        queryObj={
            "name": name,
            "title": title,
            "hidden": hidden,
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
    path="/system/menu/recycle",
    response_model=Result,
    summary="获取被删除菜单分页列表"
)
async def recycle_menu(
        page: int, pageSize: int,
        orderBy: Optional[str] = "",
        orderType: Optional[str] = "",
        name: Optional[str] = "",
        title: Optional[str] = "",
        hidden: Optional[str] = "",
        maxDate: Optional[str] = "",
        minDate: Optional[str] = "",
        status: Optional[str] = "",
        db: AsyncSession = Depends(get_db),
        token: str = Depends(check_jwt_token)
):
    result = await getMenu.getQuery(
        db,
        pageIndex=page,
        pageSize=pageSize,
        queryObj={
            "name": name,
            "title": title,
            "hidden": hidden,
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
