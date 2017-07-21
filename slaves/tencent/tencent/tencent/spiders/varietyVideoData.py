# -*- coding: utf-8 -*-
import scrapy, re, sys, json, time
import tencentSourceList
from tencent.items import *
import MySQLdb, socket, time
from scrapy import log

socket.setdefaulttimeout(5)
db = MySQLdb.connect("10.27.216.133", "aliPa", "6y3*p*o$Uj>1s$H", "ysali", port=6306)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
createTime = time.strftime("%Y-%m-%d", time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

Urls = [i for i in cursor.fetchmany(
    cursor.execute("select vc_url,vc_nameInfo,vc_type,vc_name, vc_videoid from tencent_video where vc_class='综艺' "))]


class MovieinfoSpider(scrapy.Spider):
    name = "varietyVideoData"
    allowed_domains = ["qq.com"]
    start_urls = Urls

    def start_requests(self):
        for vc_url, vc_nameInfo, vc_type, vc_name, vc_videoid in self.start_urls:
            yield self.make_requests_from_url(vc_url, vc_nameInfo, vc_type, vc_name, vc_videoid)

    def make_requests_from_url(self, vc_url, vc_nameInfo, vc_type, vc_name, vc_videoid):
        videoData_url = "http://data.video.qq.com/fcgi-bin/data?tid=613&&appid=20001212&appkey=b4789ed0ec69d23a&otype=json&idlist={}".format(
            vc_videoid)
        return scrapy.Request(meta={"name": vc_name, "types": vc_type, "videoid": vc_videoid, \
                                    "url": vc_url}, url=videoData_url)

    def parse(self, response):
        codes1 = response.body
        if re.search(r'\{"view_all_count":(.+?)\}', codes1):
            playCount = re.search(r'\{"view_all_count":(.+?)\}', codes1).group(1)
            items = TencentItemVarietyVideoData()
            items["v_date"] = createTime
            items["v_class"] = "综艺"
            items["v_name"] = response.meta["name"]
            items["v_url"] = response.meta["url"]
            items["v_types"] = response.meta["types"]
            items["v_playCount"] = playCount
            items["v_likeCount"] = None
            items["v_unlikeCount"] = None
            items["v_scoreQQ"] = None
            items["v_scoreDB"] = None
            items["v_isVip"] = None
            items["v_isSelf"] = None
            items["v_isPay"] = None
            items["v_videoid"] = response.meta["videoid"]

            yield items

        else:
            new_videoData_url = "https://union.video.qq.com/fcgi-bin/data?tid=376&&appid=20001212&appkey=b4789ed0ec69d23a&otype=json&&idlist={}".format(
                    response.meta["videoid"])
            yield  scrapy.Request(url=new_videoData_url,callback=self.parse_new,meta={"name":response.meta["name"],"types":response.meta["types"],\
                                                                                      "videoid":response.meta["videoid"],"url":response.meta["url"]})


    def parse_new(self,response):
        codes2 = response.body
        if re.search(r'\{"view_all_count":(.+?)\}',codes2):
            playCount = re.search(r'\{"view_all_count":(.+?)\}',codes2).group(1)
        else:
            playCount = ""

        items = TencentItemVarietyVideoData()
        items["v_date"] = createTime
        items["v_class"] = "综艺"
        items["v_name"] = response.meta["name"]
        items["v_url"] = response.meta["url"]
        items["v_types"] = response.meta["types"]
        items["v_playCount"] = playCount
        items["v_likeCount"] = None
        items["v_unlikeCount"] = None
        items["v_scoreQQ"] = None
        items["v_scoreDB"] = None
        items["v_isVip"] = None
        items["v_isSelf"] = None
        items["v_isPay"] = None
        items["v_videoid"] = response.meta["videoid"]

        yield items



