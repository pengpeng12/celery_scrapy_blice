# -*- coding: utf-8 -*-
import scrapy, re, sys, json, time
from scrapy import log
from tencent.items import *
import MySQLdb, socket, time

from slaves.tencent.tencent.tencent.items import TencentItemCartoonData

socket.setdefaulttimeout(5)
db = MySQLdb.connect("10.27.216.133", "aliPa", "6y3*p*o$Uj>1s$H", "ysali", port=6306)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
createTime = time.strftime("%Y-%m-%d", time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

urlListC = []
# urlLists = [i for i in
#             cursor.fetchmany(cursor.execute('select vc_url,vc_name,vc_tags,vc_fews,vc_infoid from tencent_infoCartoon'))]


class MovieinfoSpider(scrapy.Spider):
    name = "cartoonData"
    allowed_domains = ["qq.com"]

    def __init__(self, category=None, *args, **kwargs):
        import base64
        super(MovieinfoSpider, self).__init__(*args, **kwargs)
        category = json.loads(base64.b64decode(category)).values()[0]
        self.start_urls = category


    def start_requests(self):
        for vc_url, vc_name, vc_tags, vc_fews,vc_infoid in self.start_urls:
            yield self.make_requests_from_url(vc_url, vc_name, vc_tags, vc_fews,vc_infoid)

    def make_requests_from_url(self, vc_url, vc_name, vc_tags, vc_fews,vc_infoid):
        return scrapy.Request(meta={"name": vc_name, "tags": vc_tags, "fews": vc_fews,"vc_infoid":vc_infoid}, url=vc_url)

    def parse(self, response):
        log.msg("load url >>%s" % response.url, level=log.INFO)
        splitUrl = response.meta["vc_infoid"]
        countUrl = "http://data.video.qq.com/fcgi-bin/data?tid=70&&appid=10001007&appkey=e075742beb866145&low_login=1&idlist=" + splitUrl
        yield scrapy.Request(url=countUrl, callback=self.countParse, \
                             meta={"name": response.meta["name"], "tags": response.meta["tags"],
                                   "fews": response.meta["fews"], \
                                   "infoid": splitUrl,"url":response.url})

    def countParse(self, response):
        codesOfCount = response.body
        totalPlayCount = re.search(r'<allnumc>(.+?)</allnumc>', codesOfCount).group(1) if re.search(
                r'<allnumc>(.+?)</allnumc>', codesOfCount) else None
        videoTotalPlayCount = re.search(r'<allnumc_m>(.+?)</allnumc_m>', codesOfCount).group(1) if re.search(
                r'<allnumc_m>(.+?)</allnumc_m>', codesOfCount) else None
        todayTotalPlayCount = re.search(r'<tdnumc>(.+?)</tdnumc>', codesOfCount).group(1) if re.search(
                r'<tdnumc>(.+?)</tdnumc>', codesOfCount) else None
        todayVideoTotalPlayCount = re.search(r'<tdnumc_m>(.+?)</tdnumc_m>', codesOfCount).group(1) if re.search(
                r'<tdnumc_m>(.+?)</tdnumc_m>', codesOfCount) else None
        infoid = response.meta["infoid"]
        scoreUrl = "http://data.video.qq.com/fcgi-bin/data?tid=128&appid=10001007&appkey=e075742beb866145&low_login=1&idlist=" + infoid
        yield scrapy.Request(url=scoreUrl, callback=self.scoreParse, \
                             meta={"name": response.meta["name"], "tags": response.meta["tags"],
                                   "fews": response.meta["fews"], \
                                   "infoid": response.meta["infoid"], "totalPlayCount": totalPlayCount, \
                                   "videoTotalPlayCount": videoTotalPlayCount,
                                   "todayTotalPlayCount": todayTotalPlayCount, \
                                   "todayVideoTotalPlayCount": todayVideoTotalPlayCount,"url":response.meta["url"]})

    def scoreParse(self, response):
        items = TencentItemCartoonData()
        codesOfScore = response.body
        splitScore = re.search(r'<score>([\s\S]*)</score>', codesOfScore).group(1) if re.search(
            r'<score>([\s\S]*)</score>', codesOfScore) else ""
        score = re.search(r'<score>(.+?)</score>', splitScore).group(1) if re.search(r'<score>(.+?)</score>',
                                                                                     splitScore) else None

        items["vc_class"] = "动漫"
        items["vc_name"] = response.meta["name"]
        items["totalPlayCount"] = response.meta["totalPlayCount"]
        items["score"] = score
        items["todayTotalPlayCount"] = response.meta["todayTotalPlayCount"]
        items["videoTotalPlayCount"] = response.meta["videoTotalPlayCount"]
        items["todayVideoTotalPlayCount"] = response.meta["todayVideoTotalPlayCount"]
        items["tag"] = response.meta["tags"]
        items["createTime"] = createTime
        items["infoid"] = response.meta["infoid"].strip()
        items["vc_url"] = response.meta["url"]

        yield items
