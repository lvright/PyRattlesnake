# -*- coding: utf-8 -*-

from celery import Celery

celery = Celery('backend')
celery.config_from_object('backend.core.conf.CeleryConf.imports')

if __name__ == '__main__':
    celery.start()