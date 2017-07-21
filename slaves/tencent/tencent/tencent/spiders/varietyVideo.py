# -*- coding: utf-8 -*-
import scrapy,re,sys,json,time
import tencentSourceList
from tencent.items import *
import MySQLdb,socket,time
from scrapy import log
socket.setdefaulttimeout(5)
db = MySQLdb.connect("10.27.216.133","aliPa","6y3*p*o$Uj>1s$H","ysali",port=6306)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
createTime = time.strftime("%Y-%m-%d",time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

Urls = [i for i in cursor.fetchmany(cursor.execute("select vc_tags,vc_url,vc_type,vc_name, vc_infoid from tencent_infovariety"))]

class MovieinfoSpider(scrapy.Spider):
    name = "varietyVideo"
    allowed_domains = ["qq.com"]
    start_urls = Urls

    def start_requests(self):
        for tags,urlInfo,types,nameInfo, infoid in self.start_urls:
                yield self.make_requests_from_url(tags,urlInfo,types,nameInfo, infoid)

    def make_requests_from_url(self,tags,urlInfo,types,nameInfo,infoid):
        return scrapy.Request(meta={"nameInfo":nameInfo,"types":types,"tags":tags,"infoid":infoid},url=urlInfo)

    def parse(self,response):
        sourceCodes = response.body
        data_value = re.findall(r'data-value="(\d{1,5})"',sourceCodes)
        for dv in data_value:
            vid = re.search(r"id:.*?'(.*?)';",sourceCodes).group(1).strip() if re.search(r"id:.*?'(.*?)';",sourceCodes) else None
            jsHomeUrl = "http://s.video.qq.com/loadplaylist?&low_login=1&type=4" \
                        "&id=%s&plname=qq&vtype=3&video_type=10&inorder=1&otype=json&year=%s" \
                        "&callback=_jsonp_3_03f0&_t=%s"%(vid,dv,int(time.time()))
	    #print jsHomeUrl,"$$"
            yield scrapy.Request(meta={"nameInfo":response.meta["nameInfo"],"types":response.meta["types"],\
                                       "tags":response.meta["tags"],"urlInfo":response.url,"dv":dv,"infoid":response.meta["infoid"]},callback=self.parseJson,\
                                 url=jsHomeUrl,dont_filter=True)
    def parseJson(self,response):
            codes = response.body
            jsonCodes = json.loads(codes.split("_jsonp_3_03f0(")[1].strip().replace("})","}"))
            # log.msg("##########",level=log.INFO)
            # print response.url
            # print jsonCodes
            # log.msg("##########",level=log.INFO)
            splitItems = jsonCodes["video_play_list"]["playlist"][response.meta["dv"]]
            for item in splitItems:
                year = item["episode_number"]
                pic = item["pic"]
                title = item["title"]
                url = item["url"]
                vid = item["vid"]
                ids = item["id"]
                newUrl = "https://v.qq.com/x/cover/"+url.split("/")[-2]+"/"+url.split("/")[-1]

                yield  scrapy.Request(callback=self.parseHtml,url=newUrl,dont_filter=True,\
                                      meta={"year":year,"pic":pic,"name":title,"nameInfo":response.meta["nameInfo"],\
                                            "types":response.meta["types"],"tags":response.meta["tags"],\
                                            "urlInfo":response.meta["urlInfo"],"infoid":response.meta["infoid"]})

    def parseHtml(self,response):
        codes = response.body
        guests = FucTencent_video.getGuests(codes)
        length = FucTencent_video.getLength(codes)
        ids = re.search(r"id:.*?'(.*?)',",codes).group(1) if re.search(r"id:.*?'(.*?)',",codes) else ""
        if ids != "":
            homeUrl = "https://union.video.qq.com/fcgi-bin/data?tid=609&appid=10001007" \
                      "&appkey=e075742beb866145&otype=json&idlist=%s" %ids

            yield  scrapy.Request(callback=self.parsePerson,url=homeUrl,dont_filter=True,\
                                      meta={"year":response.meta["year"],"pic":response.meta["pic"],\
                                            "name":response.meta["name"],"nameInfo":response.meta["nameInfo"],\
                                            "types":response.meta["types"],"tags":response.meta["tags"],\
                                            "urlInfo":response.meta["urlInfo"],"newUrl":response.url,\
                                            "guests":guests,"length":length,"infoid":response.meta["infoid"]})

    def parsePerson(self,response):
        items = TencentItemVarietyVideo()
        jcodes = response.body
        presentercodes = json.loads(jcodes.split("QZOutputJson=")[1].replace("};","}"))
        presenters = "|".join(presentercodes["results"][0]["fields"]["presenter"])
        #infoid = response.meta["urlInfo"].split("/")[-1].split(".")[0].strip()
        videoid = response.meta["newUrl"].split("/")[-1].split(".")[0].strip()

        items["v_url"] = response.meta["newUrl"].strip()
        items["v_urlInfo"] = response.meta["urlInfo"].strip()
        items["v_name"] = response.meta["name"].strip()
        items["v_type"] = "正片"
        items["v_nameInfo"] = response.meta["nameInfo"]
        items["v_class"] = "综艺"
        items["v_tvYear"] = response.meta["year"]
        items["v_imgUrl"] = response.meta["pic"]
        items["v_presenters"] = presenters
        items["v_guests"] = response.meta["guests"]
        items["v_length"] = response.meta["length"]
        items["v_date"] = createTime
        items["v_publishTime"] = ""
        items["v_infoid"] = response.meta["infoid"]
        items["v_videoid"] = videoid

        yield items



class FucTencent_video(object):

    @staticmethod
    def getGuests(codes):
        splitCon = re.search(r'>嘉宾[\s\S]*?</div>',codes).group(0) if re.search(r'>嘉宾[\s\S]*?</div>',codes) else ""
        guests = "|".join(re.findall(r'<a[\s\S]*?>(.*?)</a>',splitCon))
        return guests

    @staticmethod
    def getLength(codes):
        length = re.search(r'duration: "(.*?)",',codes).group(1) if re.search(r'duration: "(.*?)",',codes) else ""
        return length
