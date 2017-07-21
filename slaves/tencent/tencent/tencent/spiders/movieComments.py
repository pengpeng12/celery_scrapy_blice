# -*- coding: utf-8 -*-
import scrapy,re,sys,json,time
import tencentSourceList
from scrapy import log
from tencent.items import *
import logging
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


BREAKOUT = False
PAGES = 1

urlLists = [i for i in cursor.fetchmany(cursor.execute('select vc_url,vc_name,vc_infoid from tencent_infoMovie'))]

class MovieinfoSpider(scrapy.Spider):

    name = "movieComments"
    allowed_domains = ["qq.com"]
    start_urls = urlLists

    def start_requests(self):
        for url,name,infoid in self.start_urls:
            commentIdUrl = "https://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&cid={}".format(infoid)
            yield self.make_requests_from_url(name,commentIdUrl,infoid,url)

    def make_requests_from_url(self,name,commentIdUrl,infoid,url_HOME):
        return scrapy.Request(meta={"name":name,"infoid":infoid,"url_HOME":url_HOME},url=commentIdUrl)

    def parse(self, response):
        codes = response.body
        commentid = re.search(r'"comment_id":"(\d{5,20})"',codes).group(1) if re.search(r'"comment_id":"(\d{5,20})"',codes)\
                    else None
        while True:
            global PAGES,BREAKOUT
            newUrl = "https://coral.qq.com/article/{}/comment?&reqnum=50&tag=&page={}".format(commentid,PAGES)
            if BREAKOUT == True:
                BREAKOUT = False
                print "<< -- will break  -- >>",PAGES,BREAKOUT
                break
            else:
                yield scrapy.Request(callback=self.commentParse,\
                                     meta={"name":response.meta["name"],"infoid":response.meta["infoid"],\
                                           "url_home":response.meta["url_HOME"]},url=newUrl)

    def commentParse(self,response):
        global BREAKOUT,PAGES
        items = TencentItemMovieComment()
        codes = response.body
        dictData = json.loads(codes)
        commentLen = len(dictData["data"]["commentid"])
        if commentLen > 0:
            PAGES += 1
            for content,comment_time,region in ParseMovie.learnComments(codes):
                items["content"] = content
                items["commentDate"] = comment_time
                items["region"] = region
                items["url"] = response.meta["url_home"]
                items["infoid"] = response.meta["infoid"]
                items["name"] = response.meta["name"]

                yield items
        else:

            PAGES = 1
            BREAKOUT = True


class ParseMovie(object):

    @classmethod
    def learnComments(cls,jsonComments):
        dictData = json.loads(jsonComments)
        for item in dictData["data"]["commentid"]:
            comment_time = item["time"]
            content = item["content"].strip()
            nick = item["userinfo"]["nick"].strip()
            gender = item["userinfo"]["gender"]
            region = item["userinfo"]["region"] if item["userinfo"]["region"] != "::" else None
            yield content,comment_time,region


