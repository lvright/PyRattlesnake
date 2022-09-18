# -*- coding: utf-8 -*-

from typing import TypeVar, Generic, Optional, Union, List, Dict, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel

SchemasType = TypeVar("SchemasType", bound=BaseModel)

class Result(GenericModel, Generic[SchemasType]):
    """ 普通结果验证 """
    code: int
    data: Union[SchemasType, str, list, dict, bool]
    message: Optional[str]
    success: Optional[bool]


class ListModel(GenericModel, Generic[SchemasType]):
    """ 自定义结果 --> data 数据 """
    list: List[Union[SchemasType, Dict[str, Any]]]
    count: int


class ResultPlus(GenericModel, Generic[SchemasType]):
    """ 列表结果验证 """
    code: int
    data: ListModel[SchemasType]
    message: Optional[str]
    success: Optional[bool]