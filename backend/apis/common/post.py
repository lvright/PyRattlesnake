# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, check_jwt_token, celery
from backend.scheams import Result, Token, Post
from backend.models import post
from backend.crud import CRUDBase, getPost
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis
from utils import resp_200

router = APIRouter()

@router.get(path="/system/post/list", summary="获取岗位列表")
async def get_post_list(db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    return resp_200(data=await getPost.userPost(db, user_id=token["id"]))