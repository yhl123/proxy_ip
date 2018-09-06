# -*- coding: utf-8 -*-
from celery import Celery
app = Celery('demo')
app.config_from_object('celery_app.celeryconfig')

# worker启动命令（Windows）:需要额外安装 pip install eventlet
# celery -A celery_app worker --loglevel=info -P eventlet
# worker启动命令（linux）:
# celery -A celery_app worker --loglevel=info -P eventlet
# beat启动命令:
# celery beat -A celery_app
