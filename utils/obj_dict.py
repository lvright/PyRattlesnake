# -*- coding: utf-8 -*-

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

def obj_as_dict(obj):
    """ ORM对象转字典 """
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs} if obj else None

def list_obj_as_dict(list_obj):
    """ ORM列表对象转字典 """
    return [obj_as_dict(obj) for obj in list_obj]
