# -*- coding: utf-8 -*-

from backend.crud import CRUDBase
from backend.models import LoginLog
from backend.scheams import Loginlogger


class CRUDLoginLog(CRUDBase[LoginLog, Loginlogger]):
    pass


getLoginLog = CRUDLoginLog(LoginLog)
