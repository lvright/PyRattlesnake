# -*- coding: utf-8 -*-

broker_url = 'amqp://guest@localhost:5672'

result_backend = 'redis://localhost:6379/1'

imports = (
    'admin.tasks.user.login',
    'admin.tasks.user.account'
)

enable_utc = True

task_serializer = 'json'

result_serializer = 'json'

IGNORE_RESULT = True

WORKER_DISABLE_RATE_LIMITS = True

RESULT_EXPIRES = 3600

TASK_TIME_LIMIT = 600

TASK_DEFAULT_ROUTING_KEY = "default"

DEFAULT_QUEUE = 'default'

TASK_DEFAULT_EXCHANGE = "default"

TASK_DEFAULT_EXCHANGE_TYPE = "direct"

TIMEZONE = 'Asia/Shanghai'

TASK_ANNOTATIONS = {'*': {'rate_limit': '10/s'}}

WORKER_CONCURRENCY = 20

WORKER_PREFETCH_MULTIPLIER = 4

WORKER_MAX_TASKS_PER_CHILD = 200

TASK_COMPRESSION = 'zlib'

