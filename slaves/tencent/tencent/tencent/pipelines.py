# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tencent.items import *
import MySQLdb,time
from loadJson import LoadJson
from slaves.tencent.tencent.tencent.items import TencentItemMovieInfo, TencentItemMovieInfoUpdate, TencentItemTvInfo, \
    TencentItemTvInfoUpdate, TencentItemVarietyVideo, TencentItemCartoonVideo, TencentItemCartoonVideoData, \
    TencentItemVarietyVideoData, TencentItemMovieData, TencentItemTVData, TencentItemCartoonData, \
    TencentItemMovieComment, TencentItemTVComment, TencentItemVarietyComment

createTime = time.strftime("%Y-%m-%d",time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

data_cartoon_list = list()
data_tv_list = list()
data_movie_list = list()
info_cartoon_list = list()

class TencentPipeline(object):
    def process_item(self, item, spider):
        self.host = spider.settings.get('MYSQL_HOST')
        self.port = spider.settings.get('MYSQL_PORT')
        self.usr = spider.settings.get('MYSQL_USR')
        self.pwd = spider.settings.get('MYSQL_PWD')
        self.db = spider.settings.get('MYSQL_DB')
        self.conn = MySQLdb.connect(host=self.host, port=self.port,
                                    user=self.usr, passwd=self.pwd, db=self.db,
                                    charset="utf8", use_unicode=True)
        if isinstance(item,TencentItemMovieInfo):
            cursor = self.conn.cursor()
            itemList = (item["vc_class"],item["vc_name"],item["vc_url"],item["vc_type"],\
                        item["vc_release"],item["vc_area"],item["vc_directors"],item["vc_mainActors"],\
                        item["vc_tags"],item["vc_detail"],item["nm_isVip"],item["nm_isSelf"],item["nm_isForeshow"],\
                        item["nm_isPay"],item["vc_startTime"],item["vc_endTime"],createTime,\
                        0,0,item["vc_imgUrl"],item["vc_length"],item["vc_label"],item["infoid"]
                        )
            proName = "pro_add_tencent_infoMovie"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            data_tv_list.append(item["infoid"])
            return item

        if isinstance(item,TencentItemMovieInfoUpdate):
            cursor = self.conn.cursor()
            itemList = (item["vc_class"],item["vc_name"],item["vc_url"],item["vc_type"],\
                        item["vc_release"],item["vc_area"],item["vc_directors"],item["vc_mainActors"],\
                        item["vc_tags"],item["vc_detail"],item["nm_isVip"],item["nm_isSelf"],item["nm_isForeshow"],\
                        item["nm_isPay"],item["vc_startTime"],item["vc_endTime"],createTime,\
                        0,0,item["vc_imgUrl"],item["vc_length"],item["vc_label"],item["infoid"]
                        )
            proName = "pro_add_tencent_infomovie_update"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            return item


        if isinstance(item,TencentItemTvInfo):
            cursor = self.conn.cursor()

            itemList = ("电视剧",item["name"],item["url"],item["imgUrl"],item["totalType"],item["year"],item["area"],\
                        item["lag"],item["directors"],item["mainActors"],item["tags"],item["zjs"],item["detail"],item["isVip"],\
                        item["isSelf"],item["isPay"],item["isTencent"],item["newTags"],createTime,item["bieName"],item["isNearby"],item["infoid"])
            proName = "pro_add_tencent_infoTV"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            return item

        if isinstance(item,TencentItemTvInfoUpdate):
            cursor = self.conn.cursor()

            itemList = ("电视剧",item["name"],item["url"],item["imgUrl"],item["totalType"],item["year"],item["area"],\
                        item["lag"],item["directors"],item["mainActors"],item["tags"],item["zjs"],item["detail"],item["isVip"],\
                        item["isSelf"],item["isPay"],item["isTencent"],item["newTags"],createTime,item["bieName"],item["isNearby"],item["infoid"])
            proName = "pro_add_tencent_infotv_update"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            return item


        if isinstance(item,TencentItemVarietyVideo):
            cursor = self.conn.cursor()
            itemList = (item["v_url"],item["v_urlInfo"],item["v_name"],item["v_type"],item["v_nameInfo"],item["v_class"],\
                        item["v_tvYear"],item["v_imgUrl"],item["v_presenters"],item["v_guests"],item["v_length"],item["v_date"],\
                        item["v_publishTime"],item["v_infoid"],item["v_videoid"])
            proName = "pro_add_tencent_video"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            return item

        if isinstance(item,TencentItemCartoonVideo):
            cursor = self.conn.cursor()
            itemList = (item["v_url"],item["v_urlInfo"],item["v_name"],item["v_type"],item["v_nameInfo"],item["v_class"],\
                        item["v_tvYear"],item["v_imgUrl"],item["v_presenters"],item["v_guests"],item["v_length"],item["v_date"],\
                        item["v_publishTime"],item["v_infoid"],item["v_videoid"])
            proName = "pro_add_tencent_video"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            info_cartoon_list.append(item["v_infoid"])
            return item

        if isinstance(item,TencentItemCartoonVideoData):
            cursor = self.conn.cursor()
            itemList = (item["v_date"],item["v_class"],item["v_name"],item["v_url"],item["v_types"],item["v_playCount"],\
                        item["v_likeCount"],item["v_unlikeCount"],item["v_scoreQQ"],item["v_scoreDB"],item["v_isVip"],\
                        item["v_isSelf"],item["v_isPay"], item["v_videoid"])
            proName = "pro_add_tencent_videoData"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            return item

        if isinstance(item,TencentItemVarietyVideoData):
            cursor = self.conn.cursor()
            itemList = (item["v_date"],item["v_class"],item["v_name"],item["v_url"],item["v_types"],item["v_playCount"],\
                        item["v_likeCount"],item["v_unlikeCount"],item["v_scoreQQ"],item["v_scoreDB"],item["v_isVip"],\
                        item["v_isSelf"],item["v_isPay"], item["v_videoid"])
            proName = "pro_add_tencent_videoData"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            return item



        if isinstance(item,TencentItemMovieData):
            cursor = self.conn.cursor()

            itemList = (item["v_class"],item["v_name"],item["v_url"],item["v_totalPlayCount"],item["v_score"],\
                        item["v_todayPlayCount"],item["v_videoPlayCount"],item["v_videoTodayPlayCount"],\
                        item["v_tags"],item["v_date"],item["v_infoid"])
            proName = "pro_add_tencent_data"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            data_movie_list.append(item["v_infoid"])
            return item

        if isinstance(item,TencentItemTVData):
            cursor = self.conn.cursor()

            itemList = (item["v_class"],item["v_name"],item["v_url"],item["v_totalPlayCount"],item["v_score"],\
                        item["v_todayPlayCount"],item["v_videoPlayCount"],item["v_videoTodayPlayCount"],\
                        item["v_tags"],item["v_date"],item["v_infoid"])
            proName = "pro_add_tencent_data"

            cursor.callproc(proName,itemList)
            self.conn.commit()
            data_tv_list.append(item["v_infoid"])
            return item


        if isinstance(item,TencentItemCartoonData):
            '''"动漫",title,url,totalPlayCount,score,todayTotalPlayCount,videoTotalPlayCount,todayVideoTotalPlayCount,tag,createTime,infoid'''
            # cursor = self.conn.cursor()
            #
            # itemList = (item["vc_class"],item["vc_name"],item["vc_url"],item["totalPlayCount"],item["score"],\
            #             item["todayTotalPlayCount"],item["videoTotalPlayCount"],item["todayVideoTotalPlayCount"],\
            #             item["tag"],item["createTime"],item["infoid"])
            # proName = "pro_add_tencent_data"
            #
            # cursor.callproc(proName,itemList)
            # self.conn.commit()
            # data_cartoon_list.append(item["infoid"])
            return item

        #电影评论
        if isinstance(item,TencentItemMovieComment):
            LoadJson().loadJsonToFile(plat="tencent",vclass="movie",items=item)
            return item

        #电视剧评论
        if isinstance(item,TencentItemTVComment):
            LoadJson().loadJsonToFile(plat="tencent",vclass="tv",items=item)
            return item

        #综艺评论
        if isinstance(item,TencentItemVarietyComment):
            LoadJson().loadJsonToFile(plat="tencent",vclass="variety",items=item)
            return item


##关闭和打开爬虫的时候执行的代码##

    def close_spider(self, spider):

        self.host = spider.settings.get('MYSQL_HOST')
        self.port = spider.settings.get('MYSQL_PORT')
        self.usr = spider.settings.get('MYSQL_USR')
        self.pwd = spider.settings.get('MYSQL_PWD')
        self.db = spider.settings.get('MYSQL_DB')
        self.conn = MySQLdb.connect(host=self.host, port=self.port,
                                    user=self.usr, passwd=self.pwd, db=self.db,
                                    charset="utf8", use_unicode=True)

        #cartoonData
        if spider.name == "cartoonData":
            itemList = ("tencent_data","动漫")
            cursor = self.conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            self.conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            for infoid in data_cartoon_list:
                sql = "update tencent_infocartoon SET nm_datastatus=1 WHERE vc_infoid=%s"
                args = (infoid,)
                cursor.execute(sql,args)
            self.conn.commit()

        #movieData
        if spider.name == "movieData":
            itemList = ("tencent_data","电影")
            cursor = self.conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            self.conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            for infoid in data_movie_list:
                sql = "update tencent_infomovie SET nm_datastatus=1 WHERE vc_infoid=%s"
                args = (infoid,)
                cursor.execute(sql,args)
            self.conn.commit()
        #tvData
        if spider.name == "tvData":
            itemList = ("tencent_data","电视剧")
            cursor = self.conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            self.conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            for infoid in data_movie_list:
                sql = "update tencent_infotv SET nm_datastatus=1 WHERE vc_infoid=%s"
                args = (infoid,)
                cursor.execute(sql,args)
            self.conn.commit()

        #cartoonVideo
        if spider.name == "cartoonVideo":
            itemList = ("tencent_video","动漫")
            cursor = self.conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            self.conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

            for videoid in list(set(info_cartoon_list)):
                sql = "update tencent_infocartoon SET nm_videostatus=1 WHERE vc_infoid=%s"
                args = (videoid,)
                cursor.execute(sql,args)
            self.conn.commit()

        #varietyVideo
        if spider.name == "varietyVideo":
            itemList = ("tencent_video","综艺")
            cursor = self.conn.cursor()
            proName = "pro_add_video_sync_status"
            cursor.callproc(proName,itemList)
            self.conn.commit()
            print "ok,all tasks done !",spider.name,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())


    def open_spider(self, spider):

        self.host = spider.settings.get('MYSQL_HOST')
        self.port = spider.settings.get('MYSQL_PORT')
        self.usr = spider.settings.get('MYSQL_USR')
        self.pwd = spider.settings.get('MYSQL_PWD')
        self.db = spider.settings.get('MYSQL_DB')
        self.conn = MySQLdb.connect(host=self.host, port=self.port,
                                    user=self.usr, passwd=self.pwd, db=self.db,
                                    charset="utf8", use_unicode=True)

        if spider.name == "cartoonData":
            cursor = self.conn.cursor()
            sql = "update tencent_infocartoon SET nm_datastatus=%s"
            args = (0,)
            cursor.execute(sql,args)
            self.conn.commit()


        if spider.name == "movieData":
            cursor = self.conn.cursor()
            sql = "update tencent_infomovie SET nm_datastatus=%s"
            args = (0,)
            cursor.execute(sql,args)
            self.conn.commit()

        if spider.name == "tvData":
            cursor = self.conn.cursor()
            sql = "update tencent_infotv SET nm_datastatus=%s"
            args = (0,)
            cursor.execute(sql,args)
            self.conn.commit()

        if spider.name == "cartoonVideo":
            cursor = self.conn.cursor()
            sql = "update tencent_infocartoon SET nm_videostatus=%s"
            args = (0,)
            cursor.execute(sql,args)
            self.conn.commit()

        if spider.name == "varietyVideo":
            cursor = self.conn.cursor()
            sql = "update tencent_infovariety SET nm_videostatus=%s"
            args = (0,)
            cursor.execute(sql,args)
            self.conn.commit()














