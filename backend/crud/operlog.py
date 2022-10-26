# -*- coding: utf-8 -*-

from backend.crud import CRUDBase
from backend.models import OperLog
from backend.scheams import Operlogger


class CRUDOperLog(CRUDBase[OperLog, Operlogger]):
    pass


getOperLog = CRUDOperLog(OperLog)
