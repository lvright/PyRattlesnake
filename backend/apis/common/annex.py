# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.apis.deps import get_db
from backend.core import check_jwt_token
from backend.crud import getAnnex
from backend.scheams import Result, Ids
from utils import resp_200

router = APIRouter()


@router.delete(path="/system/attachment/delete", response_model=Result, summary="删除附件[逻辑删除]")
async def delete_annex(annex: Ids, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for id in annex.ids: await getAnnex.tombstone(db, id)
    return resp_200(msg="删除成功")


@router.put(path="/system/attachment/recovery", response_model=Result, summary="恢复被删除的数据")
async def recovery_annex(annex: Ids, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    for ids in annex.ids: await getAnnex.update(db, ids, obj_in={"delete": 0})
    return resp_200(msg="恢复成功")


@router.get(path="/system/attachment/recycle", response_model=Result, summary="获取被删除附件分页列表")
async def recycle_annex(pageSize: int,
                        page: Optional[int],
                        orderBy: Optional[str] = "",
                        orderType: Optional[str] = "",
                        mime_type: Optional[str] = "",
                        origin_name: Optional[str] = "",
                        storage_mode: Optional[str] = "",
                        maxDate: Optional[str] = "",
                        minDate: Optional[str] = "",
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(check_jwt_token)):
    query_obj = {"origin_name": origin_name, "storage_mode": storage_mode, "mime_type": mime_type, "maxDate": maxDate,
                 "minDate": minDate}
    result = await getAnnex.getQueryReclcle(db, pageSize=pageSize, query_obj=query_obj)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page,
                                                                "totalPage": result["page_total"]}})


@router.get(path="/system/attachment/index", response_model=Result, summary="获取附件分页列表")
async def get_annex_page(pageSize: int,
                         page: Optional[int],
                         orderBy: Optional[str] = "",
                         orderType: Optional[str] = "",
                         mime_type: Optional[str] = "",
                         origin_name: Optional[str] = "",
                         storage_mode: Optional[str] = "",
                         maxDate: Optional[str] = "",
                         minDate: Optional[str] = "",
                         db: AsyncSession = Depends(get_db),
                         token: str = Depends(check_jwt_token)):
    query_obj = {"origin_name": origin_name, "storage_mode": storage_mode, "mime_type": mime_type, "maxDate": maxDate,
                 "minDate": minDate}
    print(query_obj)
    result = await getAnnex.getQuery(db, pageSize=pageSize, query_obj=query_obj)
    return resp_200(data={"items": result["data"], "pageInfo": {"total": result["total"], "currentPage": page,
                                                                "totalPage": result["page_total"]}})
