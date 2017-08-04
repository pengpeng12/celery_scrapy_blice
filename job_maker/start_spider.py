#coding=utf-8

import os
import sys
import threading
pathjoin = os.path.dirname(__file__)
if sys.platform != "win32":
    sys.path.append("/".join(os.getcwd().split("/")[:-1]))

from check_ips.spider_ip import nowip
from slaves.crawl_split import splitList
from celery.utils.log import get_task_logger
from slaves.task_maker import app
from redis_connection import Redis_blice
from overfuc.addfuc import time_run

logger = get_task_logger(__name__)
handler = Redis_blice.connection_pool()
#urllist = list(set(handler.lrange("tencent",0,-1)))
from job_maker.redis_connection import Redis_blice
import time,socket,MySQLdb
socket.setdefaulttimeout(5)
db = MySQLdb.connect("10.27.216.133", "aliPa", "6y3*p*o$Uj>1s$H", "ysali", port=6306)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
createTime = time.strftime("%Y-%m-%d", time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

urllist = [i for i in
            cursor.fetchmany(cursor.execute('select vc_url,vc_name,vc_tags,vc_fews,vc_infoid from tencent_infoCartoon '))]

class task_maker:

    def __init__(self):


        #reguter the worker queue
        self.data_queue = "demo_queue"
        self.routing_key = "for_demo"

    def __str__(self):
        return "produce tasks for customers"


    @time_run
    def start_celery(self,urllis):
        #change the defult queue
        app.send_task('task_maker.start',args=(urllis,),\
                      queue=self.data_queue,routing_key=self.routing_key)


    #producer of more threads
    def start_maker(self):
        ulist = []
        uls = splitList(urllist,len(urllist)/5)
        for urllis in uls:
            th =threading.Thread(target=self.start_celery,args=(urllis,))
            ulist.append(th)
        for st in ulist:
            st.start()
        for jo in ulist:
            jo.join()



if __name__ == "__main__":

    task_maker().start_maker()

