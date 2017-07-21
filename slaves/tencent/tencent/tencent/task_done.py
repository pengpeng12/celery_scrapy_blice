# -*- coding: utf-8 -*-
import scrapy,sys,logging
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb,time
from scrapy import signals


class Task_done(object):


    @classmethod
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_opend(self,spider):

        MYSQL_PORT = spider.settings.get("MYSQL_PORT")
        MYSQL_HOST = spider.settings.get("MYSQL_HOST")
        MYSQL_DB = spider.settings.get("MYSQL_DB")
        MYSQL_USR = spider.settings.get("MYSQL_USR")
        MYSQL_PWD = spider.settings.get("MYSQL_PWD")

        conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                                    user=MYSQL_USR, passwd=MYSQL_PWD, db=MYSQL_DB,
                                    charset="utf8", use_unicode=True)

        if spider.name == "tvData":
            cursor = conn.cursor()
            sql = "update tencent_infocartoon SET nm_datastatus=%s"
            args = (0)
            cursor.execute(sql,args)
            conn.commit()

    def spider_closed(self, spider):

        MYSQL_PORT = spider.settings.get("MYSQL_PORT")
        MYSQL_HOST = spider.settings.get("MYSQL_HOST")
        MYSQL_DB = spider.settings.get("MYSQL_DB")
        MYSQL_USR = spider.settings.get("MYSQL_USR")
        MYSQL_PWD = spider.settings.get("MYSQL_PWD")

        conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                                    user=MYSQL_USR, passwd=MYSQL_PWD, db=MYSQL_DB,
                                    charset="utf8", use_unicode=True)
        # if spider.name == "cartoonData":
        #     itemList = ("tencent_data","动漫")
        #     cursor = conn.cursor()
        #     proName = "pro_add_video_sync_status"
        #     cursor.callproc(proName,itemList)
        #     conn.commit()
        #     print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # if spider.name == "cartoonVideo":
        #     itemList = ("tencent_video","动漫")
        #     cursor = conn.cursor()
        #     proName = "pro_add_video_sync_status"
        #     cursor.callproc(proName,itemList)
        #     conn.commit()
        #     print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        if spider.name == "cartoonVideoData":
            itemList = ("tencent_videodata","动漫")
            cursor = conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # if spider.name == "movieData":
        #     itemList = ("tencent_data","动漫")
        #     cursor = conn.cursor()
        #     proName = "pro_add_video_sync_status"
        #     cursor.callproc(proName,itemList)
        #     conn.commit()
        #     print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        if spider.name == "movieInfo":
            itemList = ("tencent_infomovie",-1)
            cursor = conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        if spider.name == "tvInfo":
            itemList = ("tencent_infotv",-1)
            cursor = conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # if spider.name == "tvData":
        #     itemList = ("tencent_data","电视剧")
        #     cursor = conn.cursor()
        #     proName = "pro_add_video_sync_status"
        #     cursor.callproc(proName,itemList)
        #     conn.commit()
        #     print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # if spider.name == "varietyVideo":
        #     itemList = ("tencent_video","综艺")
        #     cursor = conn.cursor()
        #     proName = "pro_add_video_sync_status"
        #     cursor.callproc(proName,itemList)
        #     conn.commit()
        #     print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        if spider.name == "varietyVideoData":
            itemList = ("tencent_videodata","综艺")
            cursor = conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # if spider.name == 'tvData':
        #     for infoid in infoidlist:
        #         sql = "update tencent_infocartoon SET nm_datastatus=1 WHERE vc_infoid='%s'"
        #         args = (infoid)
        #         cursor.execute(sql,args)
        #     conn.commit()
        #
        # else:
        #     print spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"error -- 001"