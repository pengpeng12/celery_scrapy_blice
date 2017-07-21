# -*- coding: utf-8 -*-
import scrapy,re,sys,json,time
import tencentSourceList
from scrapy import log
from tencent.items import *
import MySQLdb,socket,time
socket.setdefaulttimeout(5)
db = MySQLdb.connect("10.27.216.133","aliPa","6y3*p*o$Uj>1s$H","ysali",port=6306)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
createTime = time.strftime("%Y-%m-%d",time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

urlLists = [i for i in cursor.fetchmany(cursor.execute('select vc_url,vc_name,vc_infoid from tencent_infoMovie'))]

class MovieinfoSpider(scrapy.Spider):
    name = "movieData"
    allowed_domains = ["qq.com"]
    start_urls = urlLists

    def start_requests(self):
        for url,name,infoid in self.start_urls:
            newUrl = "http://v.qq.com/x/cover/"+url.split("/")[-1].strip()
            yield self.make_requests_from_url(name,newUrl,infoid)

    def make_requests_from_url(self,name,newUrl,infoid):
        return scrapy.Request(meta={"name":name,"infoid":infoid},url=newUrl)

    def parse(self, response):
        log.msg("load url >>%s"%response.url,level=log.INFO)
        sourceCodes = response.body
        if re.search(r'class="video_score">(.+?)</span>',sourceCodes):#评分
            score = re.search(r'class="video_score">(.+?)</span>',sourceCodes).group(1)
        else:
            score = None

        tagsUrl = "http://v.qq.com/detail"+"/"+response.url.split("/")[-1][0]+"/"+response.url.split("/")[-1]

        yield scrapy.Request(meta={"name":response.meta["name"],"infoid":response.meta["infoid"],\
                                    "score":score,"v_url":response.url},url=tagsUrl,callback=self.parseTags)

    def parseTags(self,response):
        log.msg("parse tags...",level=log.INFO)
        codes = response.body
        if re.search(r'<div class="mod_figure_detail mod_figure_detail_en cf">[\s\S]*?<div class="detail_video">',codes):
            tagsSplitCon = re.search(r'<div class="mod_figure_detail mod_figure_detail_en cf">[\s\S]*?<div class="detail_video">',codes).group(0)
            newTags = re.search(r'<span class="mark_v">.+?alt="(.+?)"',tagsSplitCon).group(1) if re.search(r'<span class="mark_v">.+?alt="(.+?)"',tagsSplitCon) else ""
        else:
            newTags = None

        idlist = response.url.split("/")[-1].split(".")[0]
        jsonUrl = "http://data.video.qq.com/fcgi-bin/data?tid=70&&appid=20001212&appkey=b4789ed0ec69d23a&otype=json&idlist="+"".join(idlist)

        yield scrapy.Request(meta={"name":response.meta["name"],"infoid":response.meta["infoid"],\
                                    "score":response.meta["score"],"v_url":response.meta["v_url"],\
                                    "newTags":newTags},url=jsonUrl,callback=self.parseJson)

    def parseJson(self,response):
        movieDataItems = TencentItemMovieData()
        log.msg("parse json >> %s"%response.url,level=log.INFO)
        jsonData = response.body
        if re.search('"allnumc":(.+?),',jsonData):#历史总播放
            totalPlayTimes = re.search('"allnumc":(.+?),',jsonData).group(1)
        else:
            totalPlayTimes = None

        if re.search(r'"tdnumc":(.+?),',jsonData):#今日总播放
            todayPlayTimes =re.search(r'"tdnumc":(.+?),',jsonData).group(1)
        else:
            todayPlayTimes = None
            
        if todayPlayTimes == "null":
            todayPlayTimes = None

        if re.search(r'"allnumc_m":(.+?),',jsonData):#正片总播放量
            normalPlayTimes = re.search(r'"allnumc_m":(.+?),',jsonData).group(1)
        else:
            normalPlayTimes = None

        if re.search(r'"tdnumc_m":(\d{1,10})',jsonData):#正片今日播放
            normalTodayPlayTimes = re.search(r'"tdnumc_m":(\d{1,10})',jsonData).group(1)
        else:
            normalTodayPlayTimes = None



        movieDataItems["v_class"] = "电影"
        movieDataItems["v_name"] = response.meta["name"].strip()
        movieDataItems["v_url"] = response.meta["v_url"].strip()
        movieDataItems["v_totalPlayCount"] = totalPlayTimes
        movieDataItems["v_score"] = response.meta["score"]
        movieDataItems["v_todayPlayCount"] = todayPlayTimes
        movieDataItems["v_videoPlayCount"] = normalPlayTimes
        movieDataItems["v_videoTodayPlayCount"] = normalTodayPlayTimes
        movieDataItems["v_tags"] = response.meta["newTags"]
        movieDataItems["v_date"] = createTime
        movieDataItems["v_infoid"] = response.meta["infoid"]

        yield movieDataItems











