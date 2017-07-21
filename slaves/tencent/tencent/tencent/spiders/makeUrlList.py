# -*- coding: utf-8 -*-
import re
import requests

login_url = "http://v.qq.com/x/list/movie?offset=0"#电影
login_url2 = "http://v.qq.com/x/list/tv"#电视剧
login_url3 = "http://v.qq.com/x/list/variety"#综艺
login_url4 = "http://v.qq.com/x/list/cartoon"#动漫
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'}

##电影##
class MovieUrlListSpider(object):

    @property
    def MovieUrlList(self):
        session = requests.get(login_url,headers=header)
        if session.status_code is 200:
            codes = session.content
            items = re.findall(r'<a href="(.*?)"[\s\S]*?class="item"[\s\S]*?>(.*?)</a>',codes)
            for item_url,item_types in items:
                item_url =  Rmtags.rmAmp(info=item_url)
                url = Rmtags.joinUrl(seurl=item_url,types="movie")
                pageCodes = requests.get(url,headers=header).content
                pageNumList = re.findall(r'pages_index:paging_page_(.*?)"',pageCodes)
                if pageNumList != []:
                    pageNum = max(pageNumList)
                    if item_url.startswith("?offset") and not item_url.endswith("theatre=1"):
                        urlList = [url.replace("offset=0&","")+"&offset={}".format(i) for i in range(0,int(pageNum)*30+1,30)]
                        yield {item_types:urlList}
                else:
                    print "ERROR-01-Movie",url


##电视剧##
class TVUrlListSpider(object):

    @property
    def TVUrlList(self):
        codes = requests.get(login_url2,headers=header).content
        items = re.findall(r'<a href="(.*?)"[\s\S]*?class="item"[\s\S]*?>(.*?)</a>',codes)
        for item_url,item_types in items:
            item_url =  Rmtags.rmAmp(info=item_url)
            url = Rmtags.joinUrl(seurl=item_url,types="tv")
            pageCodes = requests.get(url,headers=header).content
            pageNumList = re.findall(r'pages_index:paging_page_(.*?)"',pageCodes)
            if pageNumList != []:
                pageNum = max(pageNumList)
                if item_url.startswith("?offset") and not item_url.endswith("theatre=1"):
                    urlList = [url.replace("offset=0&","")+"&offset={}".format(i) for i in range(0,int(pageNum)*30+1,30)]
                    yield {item_types:urlList}
            else:
                    print "ERROR-01-TV",url

##综艺##
class VarietyUrlListSpider(object):

    @property
    def VarietyUrlList(self):
        codes = requests.get(login_url3,headers=header).content
        items = re.findall(r'<a href="(.*?)"[\s\S]*?class="item"[\s\S]*?>(.*?)</a>',codes)
        for item_url,item_types in items:
            item_url =  Rmtags.rmAmp(info=item_url)
            url = Rmtags.joinUrl(seurl=item_url,types="variety")
            pageCodes = requests.get(url,headers=header).content
            pageNumList = re.findall(r'pages_index:paging_page_(.*?)"',pageCodes)
            if pageNumList != []:
                pageNum = max(pageNumList)
                if item_url.startswith("?offset") and not item_url.endswith("theatre=1"):
                    urlList = [url.replace("offset=0&","")+"&offset={}".format(i) for i in range(0,int(pageNum)*30+1,30)]
                    yield {item_types:urlList}
            else:
                    print "ERROR-01-Variety",url

##动漫##
class CartoonUrlListSpider(object):

    @property
    def CartoonUrlList(self):
        codes = requests.get(login_url4,headers=header).content
        items = re.findall(r'<a href="(.*?)"[\s\S]*?class="item"[\s\S]*?>(.*?)</a>',codes)
        for item_url,item_types in items:
            item_url =  Rmtags.rmAmp(info=item_url)
            url = Rmtags.joinUrl(seurl=item_url,types="cartoon")
            pageCodes = requests.get(url,headers=header).content
            pageNumList = re.findall(r'pages_index:paging_page_(.*?)"',pageCodes)
            if pageNumList != []:
                pageNum = max(pageNumList)
                if item_url.startswith("?offset") and not item_url.endswith("theatre=1"):
                    urlList = [url.replace("offset=0&","")+"&offset={}".format(i) for i in range(0,int(pageNum)*30+1,30)]
                    yield {item_types:urlList}

            else:
                    print "ERROR-01-Cartoon",url

class Rmtags(object):

    @staticmethod
    def rmAmp(tags="&amp;",info=""):
        if info == "":
            return None
        else:
            return re.sub(tags,"&",info).strip()

    @staticmethod
    def joinUrl(seurl="",types=""):
        if seurl !="" and types != "":
            return "http://v.qq.com/x/list/{}".format(types)+seurl
        else:
            return None


if __name__ == "__main__" :
    for i in CartoonUrlListSpider().CartoonUrlList:
        print i
        print "###############"


