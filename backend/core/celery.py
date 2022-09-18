# -*- coding: utf-8 -*-

from celery import Celery

celery = Celery('backend')
celery.config_from_object('backend.core.conf.celconf')

if __name__ == '__main__':
    # TODO 启动服务: celery -A admin.core worker -l info
    celery.start()