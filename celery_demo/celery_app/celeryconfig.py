# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# Timezone
CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

CELERY_IMPORTS = (
    'celery_app.proxy_ip_live',
)

CELERYBEAT_SCHEDULE = {
    'proxy-ip-live-every-30-seconds': {
        'task': 'celery_app.proxy_ip_live.get_proxy_ip_live',
        'schedule': timedelta(seconds=30),  # 每 30 秒执行一次
    },
    'proxy-pool-len-every-2h-time': {
        'task': 'celery_app.proxy_ip_live.get_proxy_ip_count',
        'schedule': crontab(hour=2),  # 两小时执行一次
    },
}
