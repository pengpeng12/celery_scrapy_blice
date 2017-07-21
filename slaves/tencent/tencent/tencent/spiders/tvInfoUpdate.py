# -*- coding: utf-8 -*-
import scrapy,re,sys,json,time
import tencentSourceList
from tencent.items import *

import MySQLdb,socket,time
socket.setdefaulttimeout(5)
db = MySQLdb.connect("59.110.17.233","aliPa","6y3*p*o$Uj>1s$H","ysali",port=6306)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
from makeUrlList import TVUrlListSpider
from scrapy import log

urlLists = []


class tvInfoSpider(scrapy.Spider):

    name = "tvInfo"
    allowed_domains = ["qq.com"]
    start_urls = TVUrlListSpider().TVUrlList


    def start_requests(self):
        for items in self.start_urls:
            types = items.keys()[0]
            for url in items.values()[0]:
                yield self.make_requests_from_url(url,types)


    def make_requests_from_url(self,urlItem,types):
        return scrapy.Request(meta={"types":types},url=urlItem)

    def parse(self, response):
        codes = response.body
        for tags,urlL,name,imgUrl in tencentInfoTv.splitContent(codes):
            print response.meta["types"],tags,urlL,name,imgUrl
            if urlL not in urlLists:
                newUrl = "http://v.qq.com/x/cover/"+urlL.split("/")[-1]
                yield scrapy.Request(url=newUrl,callback=self.detailInfoUrl,meta={"types":response.meta["types"],\
                                     "tags":tags,"name":name,"imgUrl":imgUrl},dont_filter=True)

    def detailInfoUrl(self,response):
        sourceCodes = response.body
        detailUrl,directors,mainActors = tencentInfoTv.detailUrl(sourceCodes)
        if detailUrl not in urlLists:
            log.msg("newUrl:{}".format(detailUrl),level=log.INFO)
            yield scrapy.Request(url=detailUrl,callback=self.getDetailInfo,meta={"types":response.meta["types"],\
                                "tags":response.meta["tags"],"name":response.meta["name"],"imgUrl":response.meta["imgUrl"],\
                                "directors":directors,"mainActors":mainActors},dont_filter=True)
        else:

            print u'old url:',detailUrl


    def getDetailInfo(self,response):
        print response.url,"responde url ..."
        item = TencentItemTvInfoUpdate()
        codes = response.body
        tag = response.meta["tags"]

        lenNum = re.findall(ur'episodeNumber">(\d{1,4})</span>',codes)

        if len(lenNum) > 0:
            is_nearby = 2
        else:
            is_nearby = 1

        tagList = []
        if re.search(r'<div class="mod_figure_detail mod_figure_detail_en cf">[\s\S]*?<div class="detail_video">',codes):
            tagsSplitCon = re.search(r'<div class="mod_figure_detail mod_figure_detail_en cf">[\s\S]*?<div class="detail_video">',codes).group(0)
            newTags = re.search(r'<span class="mark_v">.+?alt="(.+?)"',tagsSplitCon).group(1)\
                      if re.search(r'<span class="mark_v">.+?alt="(.+?)"',tagsSplitCon) else ""
        else:
            newTags = ""

        if "会员" in tag:
            tagList.append("会员")
            isVip = 1
        else:
            isVip = 0
        if "独播" in tag:
            tagList.append("独播")
            isSelf = 1
        else:
            isSelf = 0
        if "腾讯" in tag:
            tagList.append("腾讯")
            isTencent = 1
        else:
            isTencent = 0
        if "付费" in tag:
            tagList.append("付费")
            isPay =1
        else:
            isPay = 0

        strTags = "|".join(tagList)
        if newTags != "" and strTags != "":
            newTags = newTags+"|"+strTags
        if newTags != "" and strTags == "":
            newTags = newTags
        if newTags == "" and strTags != "":
            newTags = strTags

        if re.search(r'别　名:([\s\S]*?)</div>',codes):
            directorSplitCon = re.search(r'别　名:([\s\S]*?)</div>',codes).group(1)
            bieName = tencentInfoTv.rmDiv(directorSplitCon).strip()
        else:
            bieName = ""


        if re.search(r'地　区:([\s\S]*?)</div>',codes):
            directorSplitCon = re.search(r'地　区:([\s\S]*?)</div>',codes).group(1)
            area = tencentInfoTv.rmDiv(directorSplitCon).strip()
        else:
            area = ""

        if re.search(r'语　言:([\s\S]*?)</div>',codes):
            directorSplitCon = re.search(r'语　言:([\s\S]*?)</div>',codes).group(1)
            lag = tencentInfoTv.rmDiv(directorSplitCon).strip()
        else:
            lag = ""

        if re.search(r'出品时间:([\s\S]*?)</div>',codes):
            directorSplitCon = re.search(r'出品时间:([\s\S]*?)</div>',codes).group(1)
            year = tencentInfoTv.rmDiv(directorSplitCon).strip()
        else:
            year = ""

        if re.search(r'总集数:([\s\S]*?)</div>',codes):
            directorSplitCon = re.search(r'总集数:([\s\S]*?)</div>',codes).group(1)
            zjs = tencentInfoTv.rmDiv(directorSplitCon).strip()
        else:
            zjs = ""

        ##标签##
        if re.search(r'标　签:([\s\S]*?)</div>',codes):
            directorSplitCon = re.search(r'标　签:([\s\S]*?)</div>',codes).group(1)
            tags = tencentInfoTv.rmDiv("|".join(re.findall(r'<a[\s\S]*?>(.+?)</a>',directorSplitCon)))
        else:
            tags = ""

        ##简介##
        if re.search(r'class="intro_full">([\s\S]*?)</p>',codes):
            detailSplitCon = re.search(r'class="intro_full">([\s\S]*?)</p>',codes).group(1)
            detail = tencentInfoTv.rmDiv(detailSplitCon)
        elif re.search(r'itemprop="description">([\s\S]*?)</span>',codes):
            detailSplitCon = re.search(r'itemprop="description">([\s\S]*?)</span>',codes).group(1)
            detail = tencentInfoTv.rmDiv(detailSplitCon)
        else:
            detail = ""

        item["name"] = response.meta["name"]
        item["url"] = response.url
        item["infoid"] = response.url.split("/")[-1].split(".")[0].strip()
        item["imgUrl"] = response.meta["imgUrl"]
        item["totalType"] = response.meta["types"]
        item["year"] = year
        item["area"] = area
        item["lag"] = lag
        item["directors"] = response.meta["directors"]
        item["mainActors"] = response.meta["mainActors"]
        item["tags"] = tags
        item["zjs"] = zjs
        item["detail"] = detail
        item["isVip"] = isVip
        item["isSelf"] = isSelf
        item["isPay"] = isPay
        item["isTencent"] = isTencent
        item["newTags"] = newTags
        item["bieName"] = bieName
        item["isNearby"] = is_nearby
        print newTags,bieName,zjs
        yield item



class tencentInfoTv(object):

    @staticmethod
    def rmDiv(contents):
        return re.sub(r'<.+?>',"",contents).strip()

    @classmethod
    def makeTags(cls,tag):
        tags = []
        keyWords = ["会员免费","会员用券","独播","单片付费","会员独家","预告片"]
        for key in keyWords :
            if key in tag :
                tags.append(key)
        return "|".join(tags)

    @classmethod
    def splitContent(cls,codes):
        if re.search(r'<ul class="figures_list">[\s\S]*?</ul>',codes):
            print "get codes from login demo ..."
            splitCon = re.search(r'<ul class="figures_list">[\s\S]*?</ul>',codes).group(0)
        else:
            print "can not get splitCon !"
            splitCon = codes
        splitPatterns = re.findall(r'<li class="list_item">[\s\S]*?<div class="figure_count">',splitCon)
        for item in splitPatterns:
            u = re.search(r'href="(.+?)"',item).group(1) if re.search(r'href="(.+?)"',item) else ""
            urlL = "http://v.qq.com/detail/"+"".join(u.split("/")[5][0])+"/"+"".join(u.split("/")[5])
            tagsUrl = re.search(r'class="mark_v"><img src="(.+?)"',item).group(1)\
                    if re.search(r'class="mark_v"><img src="(.+?)"',item) else ""
            tags = scrapyTencent.makeTags(tagsUrl)
            title = re.search(r'title="(.+?)"',item).group(1) if re.search(r'title="(.+?)"',item) else ""
            name = title
            imgUrl = re.search(r'r-lazyload="(.+?)"',item).group(1) if re.search(r'r-lazyload="(.+?)"',item) else ""
            yield tags,urlL,name,imgUrl


    @classmethod
    def detailUrl(cls,sourceCodes):
        ##导演##
        if re.search(r"导演：([\s\S]*?)</a></span>",sourceCodes):
            directorSplitCon = re.search(r'导演：([\s\S]*?</a></span>)',sourceCodes).group(1)
            directors = cls.rmDiv("|".join(re.findall(r'<a[\s\S]*?>(.+?)</a>',directorSplitCon)))
        else:
            directors = ""

        ##主演##
        if re.search(r"主演：([\s\S]*?</div>)",sourceCodes):
            directorSplitCon = re.search(r'主演：([\s\S]*?</div>)',sourceCodes).group(1)
            mainActors = cls.rmDiv("|".join(re.findall(r'<a[\s\S]*?>(.+?)</a>',directorSplitCon)))
        else:
            mainActors = ""
        if  re.search(r'"album_pic"[\s\S]*?href="(.+?)"',sourceCodes):
            detailUrl = re.search(r'"album_pic"[\s\S]*?href="(.+?)"',sourceCodes).group(1)
            return detailUrl,directors,mainActors
        else:
            print "can't find detail url in sourceCode ！！"
            detailUrl = ""

            return detailUrl,directors,mainActors

class scrapyTencent(object):

    @classmethod
    def makeTags(cls,tag):
        keyImgs = {"VIP":"mark_5",
                   "预告":"mark_2",
                   "独播":"mark_1",
                   "用券":"mark_6"
                   }
        tags = []
        for va in keyImgs.items() :
            if va[1] in tag:
                tags.append(va[0])
        return "|".join(tags)
