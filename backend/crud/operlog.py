# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from backend.apis.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import OAuth2PasswordRequestForm

from backend.core import setting, create_access_token, celery
from backend.scheams import Result, Token, Operlogger
from backend.models import OperLog
from backend.crud import CRUDBase
from backend.apis.deps import get_db, get_current_user, get_redis
from backend.db import MyRedis
from utils import resp_200, SetRedis, by_ip_get_address


class CRUBoperLog(CRUDBase[OperLog, Operlogger]):

    pass

getOperLog = CRUBoperLog(OperLog)