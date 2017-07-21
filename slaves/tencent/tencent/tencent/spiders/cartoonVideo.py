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

Urls = [i for i in
        cursor.fetchmany(cursor.execute("select vc_tags,vc_url,vc_type,vc_name,vc_infoid from tencent_infocartoon"))]


class MovieinfoSpider(scrapy.Spider):
    name = "cartoonVideo"
    allowed_domains = ["qq.com"]
    start_urls = Urls

    def start_requests(self):
        for tags, urlInfo, types, nameInfo, infoid in self.start_urls:
            yield self.make_requests_from_url(tags, urlInfo, types, nameInfo, infoid)

    def make_requests_from_url(self, tags, urlInfo, types, nameInfo, infoid):
        comment_url = "http://s.video.qq.com/get_playsource?id={}&plat=2&type=4&data_type=2&" \
                      "video_type=3&range=1-10000&plname=qq&otype=json&num_mod_cnt=20".format(infoid.strip())
        return scrapy.Request(meta={"nameInfo": nameInfo, "types": types, "tags": tags, "infoid": infoid,\
                                    "urlInfo":urlInfo}, url=comment_url)

    def parse(self, response):
        codes = response.body
        json_codes = codes.replace("QZOutputJson=","").replace("};","}")

        json_data = json.loads(json_codes)

        list_items = json_data["PlaylistItem"]["videoPlayList"]
        item_num = 0
        for item in list_items:
            item_num +=1
            videoid = item["id"]
            pic = item["pic"]
            video_url = item["playUrl"]
            if item_num<10:
                video_name = response.meta["nameInfo"]+"_0"+str(item_num)
            else:
                video_name = response.meta["nameInfo"]+"_"+str(item_num)

            yield scrapy.Request(meta={"videoid":videoid,"pic":pic,"video_url":video_url,"video_name":video_name,\
                                       "nameInfo":response.meta["nameInfo"],"types":response.meta["types"],\
                                       "tags":response.meta["tags"],"infoid":response.meta["infoid"],"urlInfo":response.meta["urlInfo"]},
                                 callback=self.parseHtml,url=video_url)

    def parseHtml(self, response):
        codes = response.body
        length = re.search(r'itemprop="duration".*?content="(\d{1,6})"',codes).group(1) \
                 if re.search(r'itemprop="duration".*?content="(\d{1,6})"',codes) else None
        publishTime = re.search(r'itemprop="datePublished".*?content="(.*?)"',codes).group(1)\
                 if re.search(r'itemprop="datePublished".*?content="(.*?)"',codes) else None

        items = TencentItemCartoonVideo()
        items["v_url"] = response.meta["video_url"].strip()
        items["v_urlInfo"] = response.meta["urlInfo"].strip()
        items["v_name"] = response.meta["video_name"].strip()
        items["v_type"] = "正片"
        items["v_nameInfo"] = response.meta["nameInfo"]
        items["v_class"] = "动漫"
        items["v_tvYear"] = None
        items["v_imgUrl"] = response.meta["pic"]
        items["v_presenters"] = None
        items["v_guests"] = None
        items["v_length"] = length
        items["v_date"] = createTime
        items["v_publishTime"] = publishTime
        items["v_infoid"] = response.meta["infoid"].strip()
        items["v_videoid"] = response.meta["videoid"].strip()

        yield items


