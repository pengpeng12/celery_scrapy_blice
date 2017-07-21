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
createTime = time.strftime("%Y-%m-%d %H", time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


sql = '''SELECT b.vc_url,b.vc_type,b.vc_name,b.vc_videoid
                FROM hot_level_data  a
                JOIN tencent_video b ON a.vc_videoid = b.vc_videoid
                WHERE a.vc_class="动漫" and a.vc_plat="tencent" limit 100
                '''

Urls = [i for i in cursor.fetchmany(cursor.execute(sql))]

print len(Urls),"is loaded in memory, will loop ..."

class VdeodataC(scrapy.Spider):
    name = "cartoonVideoData"
    allowed_domains = ["qq.com"]
    start_urls = Urls
    print "start_urls >> ",len(start_urls)

    def start_requests(self):
        print "in start_requests"
        for  url, types, name, videoid in self.start_urls:
            print url,"loading ..."
            yield self.make_requests_from_url( url, types, name, videoid)

    def make_requests_from_url(self,  url, types, name, videoid):
        videoData_url = "https://union.video.qq.com/fcgi-bin/data?tid=376&&appid=20001212&" \
                        "appkey=b4789ed0ec69d23a&otype=json&idlist={}".format(videoid.strip())
        return scrapy.Request(meta={"name": name, "types": types,  "videoid": videoid.strip(), \
                                    "url": url}, url=videoData_url)

    def parse(self, response):
        json_codes = response.body
        json_data = json.loads(json_codes.replace("QZOutputJson=","").replace("};","}"))
        data_item = json_data["results"][0]["fields"]
        videoData = data_item["view_all_count"]
        codes_url = response.meta["url"]
        yield scrapy.Request(url = codes_url,callback=self.VipCodes,\
                             meta={"name":response.meta["name"],"videoid":response.meta["videoid"],"videoData":videoData})

    def VipCodes(self,response):
        items = TencentItemCartoonVideoData()
        codes = response.body
        reMark = response.meta["videoid"]+".html"
        isvip_words = re.search(r'<a.*?%s[\s\S]*?</a>'%reMark,codes).group(0)\
                     if re.search(r'<a.*?%s[\s\S]*?</a>'%reMark,codes) else None
        if "付费" in isvip_words:
            isvip = 1
        else:
            isvip = None

        if '预告' in isvip_words:
            types = "预告"
        else:
            types = "正片"

        items["v_date"] = createTime
        items["v_class"] = "动漫"
        items["v_name"] = response.meta["name"]
        items["v_url"] = response.url
        items["v_types"] = types
        items["v_playCount"] = response.meta["videoData"]
        items["v_likeCount"] = None
        items["v_unlikeCount"] = None
        items["v_scoreQQ"] = None
        items["v_scoreDB"] = None
        items["v_isVip"] = isvip
        items["v_isSelf"] = None
        items["v_isPay"] = None
        items["v_videoid"] = response.meta["videoid"]

        yield items




























