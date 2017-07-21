#coding=utf-8
import sys,os
pathjoin = os.path.dirname(__file__)
if sys.platform != "win32":
    sys.path.append("/".join(os.getcwd().split("/")[:-1]))

sys.path.append("/opt/vdb/reLyben/")

from job_maker.redis_connection import Redis_blice
import requests
from overfuc.addfuc import *
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from celery import platforms
platforms.C_FORCE_ROOT = True

from check_ips.spider_ip import nowip
from settings.celery_setting import app

@app.task(ignore_result=True)
def start(urllist):
    import base64
    import json
    import os

    json_data_list = base64.b64encode(json.dumps({'spider':urllist}))

    cmd = 'cd /opt/vdb/libin/celery_scrapy_blice/slaves/tencent/tencent/tencent/spiders/;' \
          'scrapy crawl cartoonData -a category={}'.format(json_data_list)

    print 'scrapy crawl cartoonData -a category={}'.format(json_data_list)
    os.system(cmd)

#不在数据库中存取任务状态，设置为True
# @app.task(ignore_result=True)
# def crawl(url):
#     start()



if __name__ == "__main__":
    pass
