# -*- coding: utf-8 -*-

from celery import Celery

celery = Celery(
    'admin',
    broker='redis://127.0.1:6379/1',
    backend='redis://127.0.1:6379/2'
)

# 添加 celery 配置
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
    result_expires=3600
)