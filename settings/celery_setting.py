#coding=utf-8

from celery import Celery
from settings import reids_setting
from kombu import Exchange, Queue
broker = reids_setting.ali_redis["PASSWORD"]+"@"+reids_setting.ali_redis["IP"]
backend = reids_setting.ali_redis["PASSWORD"]+"@"+reids_setting.ali_redis["IP"]

app = Celery('crawl_task', broker='redis://:{}:6379/1'.format(broker),\
            backend='redis://:{}:6379/2'.format(backend))


# 官方推荐使用json作为消息序列化方式
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ROUTES ={
        'task_maker.crawl':{
        'queue':"demo_queue",'rounting_key':'for_demo',
        'queue':"demo_queue2",'rounting_key':'for_demo2'}

    },
    CELERY_QUEUES=(
        Queue('demo_queue',exchange=Exchange('demo_queue', type='direct'), routing_key='for_demo'),
        Queue('demo_queue2',exchange=Exchange('demo_queue2', type='direct'), routing_key='for_demo2'),
                  )

)
