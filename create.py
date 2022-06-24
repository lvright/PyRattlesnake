# -*- coding: utf-8 -*-

from admin import *
from utils import *

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# 创建app
app = FastAPI(
    title='PyRattlesnake',
    description="""PyRattlesnake 是基于FASTAPI模块，配备了Web开发过程所需的工具和代码块""",
    version='0.0.1',
    docs_url='/api/docs',  # 自定义文档地址
    redoc_url=None,
    openapi_url='/api/openapi.json',
    openapi_tags=tags
)

# fastapi 蓝图
app.include_router(router)

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins='http://localhost:2800/',
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 请求拦截器 捕获请求日志
@app.middleware('http')
async def request_info(request: Request, call_next):
    response = await call_next(request)
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    # do something with body ...

    if request.method not in ['GET', 'OPTIONS'] \
            and request.url.path not in ['/admin/getConfigByKey', '/admin/info',
                                         '/admin/login', '/admin/logout']:

        success = True
        message = 'OK'
        if response.status_code != 200:
            success = False
            message = 'ERROR'

        ip_location = tackle.get_request_ip_info(request.client.host)['ip_location']
        username = db.query(sys_login_log).filter_by(ip=request.client.host).first()

        db.execute(sys_oper_log.insert().values(
            **{
                'username': dict(username)['username'],
                'method': request.method,
                'router': request.url.path,
                'ip': request.client.host,
                'ip_location': ip_location,
                'request_data': json.dumps(request.path_params)
                                or json.dumps(request.query_params)
                                or json.dumps(request.body())
                                or json.dumps(request.json())
                                or json.dumps(request.form()),
                'response_code': response.status_code,
                'response_data': json.dumps({
                    'status': response.status_code,
                    'success': success,
                    'message': message,
                    'timestamp': now_timestamp,
                }),
                'created_by': now_timestamp,
                'updated_by': now_timestamp,
                'created_at': now_date_time,
                'updated_at': now_date_time,
            }
        ))
        db.commit()

    return Response(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

# 静态文件设置
app.mount('/static', StaticFiles(directory='./static'), name='static')