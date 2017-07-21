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

class MovieinfoSpider(scrapy.Spider):
    urlListDabase = [i for i in cursor.fetchmany(cursor.execute('select vc_name,vc_url, vc_infoid from tencent_infotv'))]

    name = "tvData"
    allowed_domains = ["qq.com"]
    start_urls = urlListDabase

    def start_requests(self):
        for name,url,infoid in self.start_urls:
            newUrl = "http://v.qq.com/x/cover/"+url.split("/")[-1]
            yield self.make_requests_from_url(name,newUrl,infoid)

    def make_requests_from_url(self,name,newUrl,infoid):
        log.msg(newUrl+"<<INFO NEWURL>>",level=log.INFO)
        return scrapy.Request(meta={"name":name,"infoid":infoid},url=newUrl)

    def parse(self, response):
        idlist = response.url.split("/")[-1].split(".")[0]
        jsonUrl = "http://data.video.qq.com/fcgi-bin/data?tid=70&&appid=20001212&appkey=b4789ed0ec69d23a&otype=json&idlist="+"".join(idlist)
        sourceCodes = response.body
        log.msg(jsonUrl+"<<INFO jsonUrl>>",level=log.INFO)
        if re.search(r'video_score">(.*?)</span>',sourceCodes):#评分
            score = re.search(r'video_score">(.*?)</span>',sourceCodes).group(1)
        else:
            score = None

        yield scrapy.Request(meta={"name":response.meta["name"],"v_url":response.url,\
                                   "score":score,"infoid":response.meta["infoid"]},url=jsonUrl,callback=self.parseJson)

    def parseJson(self,response):
        tagsUrl = "http://v.qq.com/detail/"+response.meta["v_url"].split("/")[-1][0]+"/"+response.meta["v_url"].split("/")[-1]
        log.msg(tagsUrl+"<<INFO tagsUrl>>",level=log.INFO)
        jsonData = response.body
        if re.search('"allnumc":(.*?),',jsonData):#历史总播放
            totalPlayTimes = re.search('"allnumc":(.*?),',jsonData).group(1)
        else:
            totalPlayTimes = None

        if re.search(r'"tdnumc":(.*?),',jsonData):#今日总播放
            todayPlayTimes =re.search(r'"tdnumc":(.*?),',jsonData).group(1)
        else:
            todayPlayTimes = None
        if todayPlayTimes == "null":
            todayPlayTimes = None
        if re.search(r'"allnumc_m":(.*?),',jsonData):#正片总播放量
            normalPlayTimes = re.search(r'"allnumc_m":(.*?),',jsonData).group(1)
        else:
            normalPlayTimes = None

        if re.search(r'"tdnumc_m":(\d{1,10})',jsonData):#正片今日播放
            normalTodayPlayTimes = re.search(r'"tdnumc_m":(\d{1,10})',jsonData).group(1)
        else:
            normalTodayPlayTimes = None

        yield scrapy.Request(meta={"totalPlayTimes":totalPlayTimes,"todayPlayTimes":todayPlayTimes,\
                                   "normalPlayTimes":normalPlayTimes,"normalTodayPlayTimes":normalTodayPlayTimes,\
                                   "name":response.meta["name"],"v_url":response.meta["v_url"],"score":response.meta["score"],"infoid":response.meta["infoid"]},\
                             url=tagsUrl,callback=self.Infotags)

    def Infotags(self,response):

        TVDataItems = TencentItemTVData()
        codes = response.body
        if re.search(r'<div class="mod_figure_detail mod_figure_detail_en cf">[\s\S]*?<div class="detail_video">',codes):
            tagsSplitCon = re.search(r'<div class="mod_figure_detail mod_figure_detail_en cf">[\s\S]*?<div class="detail_video">',codes).group(0)
            newTags = re.search(r'<span class="mark_v">.*?alt="(.*?)"',tagsSplitCon).group(1) if re.search(r'<span class="mark_v">.+?alt="(.*?)"',tagsSplitCon) else None
        else:
            newTags = None
        log.msg("<<INFO newTags>>",level=log.INFO)

        TVDataItems["v_class"] = "电视剧"
        TVDataItems["v_name"] = response.meta["name"].strip()
        TVDataItems["v_url"] = response.meta["v_url"].strip()
        TVDataItems["v_totalPlayCount"] = response.meta["totalPlayTimes"]
        TVDataItems["v_score"] = response.meta["score"]
        TVDataItems["v_todayPlayCount"] = response.meta["todayPlayTimes"]
        TVDataItems["v_videoPlayCount"] = response.meta["normalPlayTimes"]
        TVDataItems["v_videoTodayPlayCount"] = response.meta["normalTodayPlayTimes"]
        TVDataItems["v_tags"] = newTags
        TVDataItems["v_date"] = createTime
        TVDataItems["v_infoid"] = response.meta["infoid"]

        yield TVDataItems