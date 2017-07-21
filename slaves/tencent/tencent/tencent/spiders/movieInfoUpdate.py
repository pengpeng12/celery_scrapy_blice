# -*- coding: utf-8 -*-
import scrapy,re,sys,json,time
import tencentSourceList
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

#urlLists = [i[0] for i in cursor.fetchmany(cursor.execute('select vc_url from tencent_infoMovie WHERE vc_class="电影"'))]

urlLists = []

class MovieinfoSpider(scrapy.Spider):
    name = "movieInfo"
    allowed_domains = ["qq.com"]
    start_urls = tencentSourceList.movieUrls

    def start_requests(self):
        for nameUrlList in self.start_urls.items():

            name = nameUrlList[0]
            for url in nameUrlList[1]:

                yield self.make_requests_from_url(name,url)

    def make_requests_from_url(self,name,url):
        return scrapy.Request(meta={"name":name},url=url)

    def parse(self, response):

        types = response.meta["name"]
        codes = response.body
        splitPatterns = re.findall(r'r-lazyload[\s\S]*?<div class="figure_info">',codes)
        for item in splitPatterns:
            u = re.search(r'href="(.+?)"',item).group(1) if re.search(r'href="(.+?)"',item) else ""
            urlL = "http://v.qq.com/detail/"+"".join(u.split("/")[5][0])+"/"+"".join(u.split("/")[5])
            if urlL not in urlLists:
                tagsUrl = re.search(r'class="mark_v"><img src="(.+?)"',item).group(1)\
                        if re.search(r'class="mark_v"><img src="(.+?)"',item) else ""
                tags = scrapyTencent.makeTags(tagsUrl)


                title = re.search(r'title="(.+?)"',item).group(1) if re.search(r'title="(.+?)"',item) else ""
                name = title
                imgUrl = re.search(r'r-lazyload="(.+?)"',item).group(1) if re.search(r'r-lazyload="(.+?)"',item) else ""


                yield scrapy.Request(callback=self.detailInfo,url=urlL,\
                                 meta={"types":types,"label":tags,"title":name,"imgUrl":imgUrl})
            else:
                print "old url"
                continue


    def detailInfo(self,response):

        codes = response.body
        splitCodes = re.search(r'"detail_pic"[\s\S]*?</a>',codes).group(0) \
                     if re.search(r'"detail_pic"[\s\S]*?</a>',codes) else ""
        tagsUrl = re.search(r'"mark_v"><img src="(.*?)"',splitCodes).group(1) \
                     if re.search(r'"mark_v"><img src="(.*?)"',splitCodes) else ""
        label = scrapyTencent.makeTags(tagsUrl)
        if label not in response.meta["label"]:
            newLabel = response.meta["label"]+"|"+label
        else:
            newLabel = label

        pat_on = "|".join(list(set(re.findall(r'data-name="(.+?)"',codes))))

        if re.search(r'alternateName">(.+?)</span>',codes):#译名
            alternateName = re.search(r'alternateName">(.+?)</span>',codes).group(1)
            if ">" and "<" not in alternateName:
                alternateName = alternateName
            else:
                alternateName = ""
        else:
            alternateName = ""

        if re.search(r'别　名:([\s\S]*?</div>)',codes):
            bming = scrapyTencent.rmDiv(re.search(r'别　名:([\s\S]*?</div>)',codes).group(1))
        else:
            bming = ""


        actorsSplitCon = re.search(r'"actor_list cf">([\s\S]*?)</ul>',codes).group(1) \
                 if re.search(r'"actor_list cf">([\s\S]*?)</ul>',codes) else ""
        items = re.findall(r'<li[\s\S]*?</li>',actorsSplitCon)
        ds = []
        ms = []
        for item in items:
            if 'itemprop="director"' in item:
                director = re.search(r'stat="info:actor_name">(.+?)<',item).group(1)\
                   if re.search(r'stat="info:actor_name">(.+?)<',item) else ""
                ds.append(director)
            if 'itemprop="actor"' in item:

                mainActor = re.search(r'stat="info:actor_name">(.+?)<',item).group(1)\
                    if re.search(r'stat="info:actor_name">(.+?)<',item) else ""
                ms.append(mainActor)

        directors = "|".join(ds)
        mainActors = "|".join(ms)

        if re.search(r'标　签:([\s\S]*?)</div>',codes):
            tagsSplitCon = re.search(r'标　签:([\s\S]*?)</div>',codes).group(1)
            tagsN = scrapyTencent.rmDiv("|".join(re.findall(r'(<a[\s\S]*?)</a>',tagsSplitCon)))
            tagsN = scrapyTencent.rmDiv(tagsN)
        else:
            tagsN = ""

        if re.search(r'上映时间:([\s\S]*?)</div>',codes):
            yearSplitCon = re.search(r'上映时间:([\s\S]*?)</div>',codes).group(1)
            year = scrapyTencent.rmDiv(yearSplitCon)
        else:
            year = ""

        if re.search(r'语　言:([\s\S]*?)</div>',codes):
            yearSplitCon = re.search(r'语　言:([\s\S]*?)</div>',codes).group(1)
            lag = scrapyTencent.rmDiv(yearSplitCon)
        else:
            lag = ""

        try:
            if re.search(r'地　区:([\s\S]*?)</div>',codes):
                yearSplitCon = re.search(r'地　区:([\s\S]*?)</div>',codes).group(1)
                area = scrapyTencent.rmDiv(yearSplitCon)
            else:
                area = ""

            if area == "":
                if re.search(r'国语|内地|华语',tagsN):
                    area = "内地"
                else:
                    area = "其他"
        except:
            area = ""


        if re.search(r'简.*?介：([\s\S]*?)<a',codes):
            detailSplitCon = re.search(r'简.*?介：([\s\S]*?)<a',codes).group(1)
            detail = scrapyTencent.rmDiv(detailSplitCon)
        else:
            detail = ""

        dataVid = re.search(r"id:(.+?);",codes).group(1).replace("'","").strip() if re.search(r"id:(.+?);",codes) else ""
        commentIDUrl = "http://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&low_login=1&op=3&cid="+"".join(dataVid)
        #print directors,"#",mainActors,"#",length,"#",tagsN,"#",year,"#",lag,"#",area,"#",commentIDUrl
        yield scrapy.Request(callback=self.commentID,url=commentIDUrl,meta={"types":response.meta['types'],\
                            "tags":tagsN,"title":response.meta["title"],"imgUrl":response.meta["imgUrl"],\
                            "directors":directors,"mainActors":mainActors,"release":year,"alternateName":alternateName,\
                            "lag":lag,"area":area,"detail":detail,"label":newLabel,\
                            "url":response.url,"plat_on":pat_on})

    def commentID(self,response):
        commentID = re.search(r'"comment_id":"(.+?)",',response.body).group(1) if re.search(r'"comment_id":"(.+?)",',response.body)\
                    else ""
        upDownUrl = "http://coral.qq.com/article/%s/voteinfo?logintype=0" %commentID
        yield scrapy.Request(callback=self.startEnd,url=upDownUrl,meta={"types":response.meta['types'],\
                            "tags":response.meta["tags"],"title":response.meta["title"],"imgUrl":response.meta["imgUrl"],\
                            "directors":response.meta["directors"],"mainActors":response.meta["mainActors"],\
                            "release":response.meta["release"],"label":response.meta["label"],"alternateName":response.meta["alternateName"],\
                            "lag":response.meta["lag"],"area":response.meta["area"],"detail":response.meta["detail"],\
                            "url":response.meta["url"],"pat_on":response.meta["plat_on"]})

    def startEnd(self,response):
        url = response.meta["url"]
        lenUrl = "http://v.qq.com/x/cover/"+"".join(url.split("/")[5])
        updownCodes = response.body
        try:
            startTime = json.loads(updownCodes)["data"]["starttime"]
        except:
            startTime = ""
        try:
            endTime = json.loads(updownCodes)["data"]["endtime"]
        except:
            endTime = ""

        yield scrapy.Request(callback=self.getLength,url=lenUrl,meta={"types":response.meta['types'],\
                            "tags":response.meta["tags"],"title":response.meta["title"],"imgUrl":response.meta["imgUrl"],\
                            "directors":response.meta["directors"],"mainActors":response.meta["mainActors"],\
                            "release":response.meta["release"],"label":response.meta["label"],\
                            "lag":response.meta["lag"],"area":response.meta["area"],"detail":response.meta["detail"],\
                            "url":response.meta["url"],"startTime":startTime,"endTime":endTime,\
                            "alternateName":response.meta["alternateName"],"plat_on":response.meta["pat_on"]})

    def getLength(self,response):
        self.log(response.meta["url"])
        codes = response.body
        if re.search(r'<span class="figure_info">(.+?)</span>',codes):
            length = re.search(r'<span class="figure_info">(.+?)</span>',codes).group(1)
        else:
            length = ""

        tags = response.meta["tags"]

        if "vip" in tags :
            isVip = 1
        else:
            isVip = 0
        if "独播" in tags:
            isSelf = 1
        else:
            isSelf = 0
        if "用券" in tags:
            isPay = 1
        else:
            isPay = 0
        if "预告" in tags:
            isForeshow = 1
        else:
            isForeshow = 0

        items = TencentItemMovieInfoUpdate()
        items["vc_pat"] = "tx"
        items["vc_class"] = "电影"
        items["vc_name"] = response.meta["title"]
        items["vc_url"] = response.meta["url"]
        items["infoid"] = response.meta["url"].split("/")[-1].split(".")[0].strip()
        items["vc_type"] = response.meta["types"]
        items["vc_release"] = response.meta["release"]
        items["vc_area"] = response.meta["area"]
        items["vc_directors"] = response.meta["directors"]
        items["vc_mainActors"] = response.meta["mainActors"]
        items["vc_tags"] = response.meta["tags"]
        items["vc_detail"] = response.meta["detail"]
        items["vc_startTime"] = response.meta["startTime"]
        items["vc_endTime"] = response.meta["endTime"]
        items["vc_label"] = response.meta["label"]
        items["vc_lag"] = response.meta["lag"]
        items["vc_length"] = length
        items["vc_imgUrl"] = response.meta["imgUrl"]
        items["mc_ao"] = response.meta["alternateName"]
        items["dt_date"] = createTime
        items["create_dt"] = createTime
        items["update_dt"] = updateTime
        items["plat_on"] = response.meta["plat_on"]
        items["nm_isVip"] = isVip
        items["nm_isSelf"] = isSelf
        items["nm_isPay"] = isPay
        items["nm_isForeshow"] = isForeshow
        yield items


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

    @classmethod
    def rmDiv(cls,contents):
        return re.sub(r'<.+?>',"",contents).replace("详情","").strip()


    @classmethod
    def getCreateTime(cls):
        createTime = time.strftime("%Y-%m-%d",time.localtime())
        return createTime

    @classmethod
    def getUpdateTime(cls):
        updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        return updateTime














