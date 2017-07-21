#coding=utf-8

from mysql_connection import weboDataBase
from redis_connection import Redis_blice


sql = "select vc_url from tencent_video limit 20000"

mysql_url_list = weboDataBase().getInfoFromDatabase(sql,type=0)

r = Redis_blice.connection_pool()
for url in mysql_url_list:
    r.lpush('tencent',url)