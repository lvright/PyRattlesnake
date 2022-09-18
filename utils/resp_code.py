# -*- coding: utf-8 -*-

from typing import Union, Any, Optional
from starlette import status
from starlette.responses import Response
from fastapi.responses import ORJSONResponse, FileResponse
from utils.logger import logger

def resp_200(*, data: Any = '', msg: str = "OK") -> Response:
    logger.info(msg)
    return ORJSONResponse(status_code=status.HTTP_200_OK, content={'code': 200, 'message': msg, 'data': data, "success": True})

def resp_400(code: int = 400, data: str = None, msg: str = "请求错误(400)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'code': code, 'message': msg, 'data': data, "success": False})


def resp_401(*, data: str = None, msg: str = "未授权，请重新登录(401)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'code': 401, 'message': msg, 'data': data, "success": False})


def resp_403(*, data: str = None, msg: str = "拒绝访问(403)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'code': 403, 'message': msg, 'data': data, "success": False})


def resp_404(*, data: str = None, msg: str = "请求出错(404)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'code': 404, 'message': msg, 'data': data, "success": False})


def resp_422(*, data: str = None, msg: Union[list, dict, str] = "不可处理的实体") -> Response:
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          content={'code': 422, 'message': msg, 'data': data, "success": False})


def resp_500(*, data: str = None, msg: Union[list, dict, str] = "服务器错误(500)") -> Response:
    return ORJSONResponse(headers={'Access-Control-Allow-Origin': '*'},
                          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          content={'code': 500, 'message': msg, 'data': data, "success": False})


def resp_502(*, data: str = None, msg: str = "网络错误(502)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_502_BAD_GATEWAY, content={'code': 502, 'message': msg, 'data': data, "success": False})

# ------------------------------------------- 文件流 -------------------------------------------

def resf_200(*, filename: str = None, path: str = None, msg: str = "请求成功") -> FileResponse:
    return FileResponse(status_code=status.HTTP_200_OK, filename=filename, path=path)

# ------------------------------------------- 以下不常用 -------------------------------------------

def resp_406(*, data: str = None, msg: str = "请求的格式不可得(406)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content={'code': 406, 'message': msg, 'data': data, "success": False})


def resp_408(*, data: str = None, msg: str = "请求超时(408)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_408_REQUEST_TIMEOUT, content={'code': 408, 'message': msg, 'data': data, "success": False})


def resp_410(*, data: str = None, msg: str = "请求的资源被永久删除，且不会再得到的(410)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_410_GONE, content={'code': 410, 'message': msg, 'data': data, "success": False})


def resp_501(*, data: str = None, msg: str = "服务未实现(501)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED, content={'code': 501, 'message': msg, 'data': data, "success": False})


def resp_503(*, data: str = None, msg: str = "服务不可用(503)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                          content={'code': 503, 'message': msg, 'data': data, "success": False})


def resp_504(*, data: str = None, msg: str = "网络超时(504)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_504_GATEWAY_TIMEOUT, content={'code': 504, 'message': msg, 'data': data, "success": False})


def resp_505(*, data: str = None, msg: str = "HTTP版本不受支持(505)") -> Response:
    return ORJSONResponse(status_code=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
                          content={'code': 505, 'message': msg, 'data': data, "success": False})
