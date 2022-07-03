# -*- coding: utf-8 -*-

from celery import Celery


celery = Celery('admin')

celery.config_from_object('admin.core.conf')


if __name__ == '__main__':

    # TODO 启动服务: celery -A admin.core worker -l info

    celery.start()