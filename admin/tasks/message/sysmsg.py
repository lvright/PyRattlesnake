# -*- coding: utf-8 -*-
import celery

from admin import *
from admin.tasks import *


@celery.task
async def get_ws_message(token):
    pass