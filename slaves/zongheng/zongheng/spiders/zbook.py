# -*- coding: utf-8 -*-
import json
from time import strftime,gmtime
import random

from datetime import datetime
from lxml import etree

import requests
from scrapy import Request,FormRequest,Spider

from zongheng.items import BookItem


class ZbookSpider(Spider):
    name = "zbook"
    allowed_domains = ["book.zongheng.com",'huayu.baidu.com']
    start_url = 'http://book.zongheng.com/store/c0/c0/b9/u0/p1/v9/s9/t0/ALL.html'
    url = 'http://book.zongheng.com/store/c{categoryType}/c0/b{genderType}/u0/p{page}/v9/s9/t0/ALL.html'

    def start_requests(self):
        yield Request(self.start_url, callback=self.parse_index)

    def parse_index(self, response):
        if response.status == 200:
            # html = response.text
            # os = open('page0.html','w+')
            # os.write(html)
            # os.close()
            # print(html)
            # data = json.loads(html)
            # typeList = data['14_0_0_1_10']
            # print(typeList)
            self.genderTypeList = response.xpath('//div[@class="select_con"]/div[@class="kind"]')[0].xpath(
                './/div[@class="nr"]/a[@class="store"]/text()').extract()
            self.genderTypeIdList = response.xpath('//div[@class="select_con"]/div[@class="kind"]')[0].xpath(
                './/a[@class="store"]/@booktype').extract()
            # print(genderTypeList,genderTypeIdList)
            # 男生站category
            self.BoyCategoryTypeList = response.xpath('//div[@class="nr br sub"]/a[@class="store"]/text()').extract()
            self.BoyCategoryTypeIdList = response.xpath(
                '//div[@class="nr br sub"]/a[@class="store"]/@categoryid').extract()
            # 女生站category
            codes = requests.get('http://book.zongheng.com/store/c0/c0/b1/u0/p1/v9/s9/t0/ALL.html').text
            codesHtml = etree.HTML(codes)
            self.GirlCategoryTypeList = codesHtml.xpath('//div[@class="nr br sub"]/a[@class="store"]/text()')
            self.GirlCategoryTypeIdList = codesHtml.xpath('//div[@class="nr br sub"]/a[@class="store"]/@categoryid')
            # print(GirlCategoryTypeList,GirlCategoryTypeIdList)
            # 男生
            for i, categoryTypeId in enumerate(self.BoyCategoryTypeIdList):
                # if i == 0:
                genderTypeId = self.genderTypeIdList[0]
                request = Request(
                    self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=0),
                    callback=self.parse_boyTotalPage, dont_filter=True)
                request.meta['genderType'] = self.genderTypeList[0]
                request.meta['genderTypeId'] = genderTypeId
                request.meta['categoryTypeId'] = categoryTypeId
                request.meta['categoryType'] = self.BoyCategoryTypeList[i]
                yield request

            #女生
            for i, categoryTypeId in enumerate(self.GirlCategoryTypeIdList):
                # if i == 0:
                genderTypeId = self.genderTypeIdList[1]
                request = Request(self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=0),
                                  callback=self.parse_girlTotalPage, dont_filter=True)
                request.meta['genderType'] = self.genderTypeList[1]
                request.meta['genderTypeId'] = genderTypeId
                request.meta['categoryTypeId'] = categoryTypeId
                request.meta['categoryType'] = self.GirlCategoryTypeList[i]
                yield request

    def parse_boyTotalPage(self, response):
        if response.status == 200:
            if response:
                totalPage = response.xpath('//div[@class="pagenumber pagebar"]/@count').extract_first()
                # print 'totalPage=',totalPage

                genderTypeId = response.meta['genderTypeId']
                genderType = response.meta['genderType']
                categoryTypeId = response.meta['categoryTypeId']
                categoryType = response.meta['categoryType']

                for p in range(int(totalPage)):
                    # if p <= 3:
                    request = Request(self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=p + 1),
                                      callback=self.parse_boyStart, dont_filter=True)
                    request.meta['genderType'] = genderType
                    request.meta['genderTypeId'] = genderTypeId
                    request.meta['categoryType'] = categoryType
                    request.meta['categoryTypeId'] = categoryTypeId
                    yield request

    def parse_boyStart(self, response):
        if response.status == 200:
            if response:
                bookHrefList = response.xpath('//ul[@class="main_con"]/li//a[@class="fs14"]/@href').extract()
                # print('HrefList=', len(bookHrefList))
                for i, url in enumerate(bookHrefList):
                    # if i == 0:
                    item = BookItem()
                    genderType = response.meta['genderType']
                    genderTypeId = response.meta['genderTypeId']
                    categoryType = response.meta['categoryType']
                    categoryTypeId = response.meta['categoryTypeId']
                    for field in item.fields:
                        try:
                            item[field] = eval(field)
                        except NameError:
                            # print('Field is Not Defined', field)
                            pass
                    request = Request(url, callback=self.parse_boyDetail, dont_filter=True)
                    request.meta['item'] = item
                    yield request

    # 详情页
    def parse_boyDetail(self, response):
        if response.status == 200:
            if response:
                item = response.meta['item']
                # # 是否连载中 0连载中 1 已完结
                # serialSta serial连载中 end已完结
                serialSta = response.xpath('//div[@class="book_cover fl"]/span/@class').extract_first()
                if serialSta=='serial':
                    serialSta = '连载'
                else:
                    serialSta = '完结'
                # print('serialStatus=', serialSta)
                bookURL = response.url
                # bid
                bookId = response.url.replace('http://', '').replace('.html', '').split('/')[-1]
                # print('bookId=',bookId)
                # bname
                bookName = response.xpath('//div[@class="status fl"]/h1/a/text()').extract_first()
                # bookIcon
                bIcon = response.xpath('//div[@class="book_cover fl"]/p/a/img/@src').extract_first()
                # author
                bookAuthor = response.xpath('//div[@class="booksub"]/a[@target="_blank"]/text()').extract_first()
                # tags
                bookTags = response.xpath('//div[@class="keyword"]/a/text()').extract()
                if len(bookTags) > 1:
                    bookTags = "|".join(bookTags)
                else:
                    bookTags = bookTags[0]
                # stringNumber
                totalStringCount = response.xpath('//div[@class="booksub"]/span/text()').extract_first()
                # bookIntro
                bIntro = response.xpath('//div[@class="info_con"]/p/text()').extract_first().strip().encode('utf-8')
                # print(bookName)
                # print(bIcon)
                # print(bookAuthor)
                # print(bookTags)
                # print(totalStringCount)
                # print(bIntro)
                pList = response.xpath('//div[@class="vote_info"]/p')
                # 月推荐monthRecommend
                monthReco = pList[0].xpath('./text()').extract_first()
                # 月点击monthTouch
                monthTou = pList[1].xpath('./text()').extract_first()
                # 总点击totalTouch
                totalTou = pList[2].xpath('./text()').extract_first()
                # 总收藏totalCollection
                totalColle = pList[3].xpath('./text()').extract_first()
                # 总推荐totalRecommend
                totalReco = pList[4].xpath('./text()').extract_first()
                # 评论数discussCount
                discussCo = pList[5].xpath('./text()').extract_first()
                # print('monthReco=%s,monthTou=%s,totalTou=%s,totalColle=%s,totalReco=%s,discussCo=%s' % (monthReco,monthTou,totalTou,totalColle,totalReco,discussCo))

                vc_tags = serialSta
                bid = bookId
                bname = bookName
                bookIcon = bIcon
                author = bookAuthor
                vc_label = bookTags
                vc_url = bookURL
                stringNumber = int(totalStringCount)
                bookIntro = bIntro
                monthRecommend = int(monthReco)
                monthTouch = int(monthTou)
                totalTouch = int(totalTou)
                totalCollection = int(totalColle)
                totalRecommend = int(totalReco)
                discussCount = int(discussCo)
                # dt_create = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                dt_create = datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
                dt_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                for field in item.fields:
                    try:
                        item[field] = eval(field)
                    except NameError:
                        # print('Field is Not Defined', field)
                        pass

                yield item
    #####################
    def parse_girlTotalPage(self, response):
       if response.status == 200:
            if response:
                totalPage = response.xpath('//div[@class="pagenumber pagebar"]/@count').extract_first()
                # print 'totalPage=',totalPage
                genderTypeId = response.meta['genderTypeId']
                genderType = response.meta['genderType']
                categoryTypeId = response.meta['categoryTypeId']
                categoryType = response.meta['categoryType']

                for p in range(int(totalPage)):
                    # if p <= 3:
                    request = Request(self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=p + 1),
                                      callback=self.parse_girlStart, dont_filter=True)
                    request.meta['genderType'] = genderType
                    request.meta['genderTypeId'] = genderTypeId
                    request.meta['categoryType'] = categoryType
                    request.meta['categoryTypeId'] = categoryTypeId
                    yield request

    def parse_girlStart(self, response):
        if response.status == 200:
            if response:
                bookHrefList = response.xpath('//ul[@class="main_con"]/li//a[@class="fs14"]/@href').extract()
                # print('HrefList=', len(bookHrefList))
                for i, url in enumerate(bookHrefList):
                    # if i == 0:
                    item = BookItem()
                    genderType = response.meta['genderType']
                    genderTypeId = response.meta['genderTypeId']
                    categoryType = response.meta['categoryType']
                    categoryTypeId = response.meta['categoryTypeId']
                    for field in item.fields:
                        try:
                            item[field] = eval(field)
                        except NameError:
                            # print('Field is Not Defined', field)
                            pass
                    request = Request(url, callback=self.parse_girlDetail, dont_filter=True)
                    request.meta['item'] = item
                    yield request

    # 女生详情页
    def parse_girlDetail(self, response):
        if response.status == 200:
            if response:
                item = response.meta['item']
                # # 是否连载中 0连载中 1 已完结
                # serialSta serial连载中 end已完结
                serialSta = response.xpath('//div[@class="booktitle"]/div')[1].xpath('./@class').extract_first()
                if serialSta=='lzz':
                    serialSta = '连载'
                else:
                    serialSta = '完结'
                # print('serialStatus=', serialSta)

                bookURL = response.url
                # bid
                bookId = response.url.replace('http://', '').replace('.html', '').split('/')[-1]
                # bname
                bookName = response.xpath('//div[@class="lebg"]/h1/a/text()').extract_first()
                # bookIcon
                bIcon = response.xpath('//div[@class="img"]/a/img/@src').extract_first()
                # author
                bookAuthor = response.xpath('//div[@class="lebg"]/h1/span/a/text()').extract_first()
                # tags
                bookTags = response.xpath('//div[@class="wz"]/p')[1].xpath('./a/text()').extract()
                if len(bookTags) > 1:
                    bookTags = "|".join(bookTags)
                else:
                    bookTags = bookTags[0]
                totalTou = response.xpath('//div[@class="booknumber"]/text()').extract()[1].strip()
                #stringNumber
                totalStringCount = response.xpath('//div[@class="booknumber"]/text()').extract()[2].strip()
                # bookIntro
                bIntro = response.xpath('//p[@class="jj"]/text()').extract_first().strip().encode('utf-8')

                # print('bookId=', bookId)
                # print(bookName)
                # print(bIcon)
                # print(bookAuthor)
                # print(bookTags)
                # print(bIntro)
                # print(response.xpath('//div[@class="booknumber"]/text()').extract())
                # print('%s-%s-%s' % (totalTou,totalStringCount,bookName))

                # 评论数discussCount
                discussCo = response.xpath('//div[@class="pl"]/span/text()').extract_first()

                vc_tags = serialSta
                bid = bookId
                bname = bookName
                bookIcon = bIcon
                author = bookAuthor
                vc_label = bookTags
                vc_url = bookURL
                stringNumber = int(totalStringCount)
                bookIntro = bIntro
                totalTouch = int(totalTou)
                discussCount = int(discussCo)

                # dt_create = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                dt_create = datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
                dt_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                for field in item.fields:
                    try:
                        item[field] = eval(field)
                    except NameError:
                        # print('Field is Not Defined', field)
                        pass

                yield item
