# -*- coding: utf-8 -*-
import json
import random
import re
from datetime import datetime
from lxml import etree

import requests
from scrapy import Request, FormRequest, Spider

from zongheng.items import CommentItem


class CommentSpider(Spider):
    name = "comment"
    download_delay = 0.2
    allowed_domains = ["book.zongheng.com", "huayu.baidu.com"]
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
            # print GirlCategoryTypeList,GirlCategoryTypeIdList
            # 男生
            for i, categoryTypeId in enumerate(self.BoyCategoryTypeIdList):
                # if i == 0:
                genderTypeId = self.genderTypeIdList[0]
                request = Request(
                    self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=0),
                    callback=self.parse_boyTotalPage, dont_filter=True)
                request.meta['genderTypeId'] = genderTypeId
                request.meta['categoryTypeId'] = categoryTypeId
                yield request

            # 女生
            for i,categoryTypeId in enumerate(self.GirlCategoryTypeIdList):
                # if i == 0:
                genderTypeId = self.genderTypeIdList[1]
                request = Request(self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=0),
                                  callback=self.parse_girlTotalPage, dont_filter=True)
                request.meta['genderTypeId'] = genderTypeId
                request.meta['categoryTypeId'] = categoryTypeId
                yield request

    def parse_boyTotalPage(self, response):
        if response.status == 200:
            if response:
                totalPage = response.xpath('//div[@class="pagenumber pagebar"]/@count').extract_first()
                # print 'totalPage=',totalPage

                genderTypeId = response.meta['genderTypeId']
                categoryTypeId = response.meta['categoryTypeId']

                for p in range(int(totalPage)):
                    # if p == 0:
                    request = Request(self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=p + 1),
                                      callback=self.parse_boyStart, dont_filter=True)
                    yield request

    def parse_boyStart(self, response):
        if response.status == 200:
            if response:
                bookHrefList = response.xpath('//ul[@class="main_con"]/li//a[@class="fs14"]/@href').extract()
                # print('HrefList=', len(bookHrefList))
                for i, url in enumerate(bookHrefList):
                    # if i == 0:
                    request = Request(url, callback=self.parse_boyComment, dont_filter=True)
                    yield request

    # 评论页
    def parse_boyComment(self, response):
        if response.status == 200:
            if response:
                bookName = response.xpath('//div[@class="status fl"]/h1/a/text()').extract_first()
                bookURL = response.url
                bookId = response.url.replace('http://', '').replace('.html', '').split('/')[-1]
                # print('bookId=',bookId)

                # 请求评论列表
                url = 'http://book.zongheng.com/api/book/comment/getThreadL1st2.htm'
                data = {
                    'bookId': bookId,
                    'pagebar': '1',
                    'pageNum': '0',
                    'pageSize': '30'
                }
                request = FormRequest(url, callback=self.boyCommData, formdata=data, dont_filter=True)
                request.meta['bookName'] = bookName
                request.meta['bookURL'] = bookURL
                request.meta['bookId'] = bookId
                yield request

    def boyCommData(self, response):
        if response.status == 200:
            if response:
                # 获取评论总页数
                comment_totalPage = 1
                pageList = response.xpath('//div[@class="pagenumber pagebar"]/a[@class="scrollpage"]')
                if len(pageList) > 0:
                    comment_totalPage = pageList[-1].xpath('./text()').extract_first()
                # print 'boyComment_totalPage', comment_totalPage
                for page in range(int(comment_totalPage)):
                    # if page==0:
                    url = 'http://book.zongheng.com/api/book/comment/getThreadL1st2.htm'
                    data = {
                        'bookId': str(response.meta['bookId']),
                        'pagebar': '1',
                        'pageNum': str(page + 1),
                        'pageSize': '30'
                    }
                    request = FormRequest(url, formdata=data, callback=self.parse_boyMoreComment, dont_filter=True)
                    request.meta['bookName'] = response.meta['bookName']
                    request.meta['bookURL'] = response.meta['bookURL']
                    request.meta['bookId'] = response.meta['bookId']
                    yield request
        else:
            print 'get commentTotalPage-errorcode=', response.status

    def parse_boyMoreComment(self, response):
        if response.status == 200:
            if response:
                commentList = response.xpath('//div[@class="comment"]')
                if len(commentList) > 0:
                    for i, comment in enumerate(commentList):

                        username = comment.xpath('.//em[@class="z_u"]/text()').extract_first()
                        # print(username)
                        userImg = comment.xpath('.//div[@class="imgbox"]/a/img/@src').extract_first()
                        userId = comment.xpath('.//div[@class="imgbox"]/a[@class="tx"]/@href').extract_first().replace('http://', '').replace( '.html', '').split('/')[-1]
                        v_public = comment.xpath('.//span[@class="fl"]/em/text()').extract_first()
                        click = comment.xpath(
                            './/span[@class="fl click thread_click"]/em/text()').extract_first().replace('[',
                                                                                                         '').replace(
                            ']', '')
                        up = comment.xpath('.//span[@class="support thread_zc"]/text()').extract_first().replace('[',
                                                                                                                 '').replace(
                            ']', '')
                        reply = comment.xpath('.//span[@class="fl oppose replyThread"]/em/text()').extract_first()
                        if reply:
                            reply = reply.replace('[', '').replace(']', '')
                            reply = int(reply)
                        else:
                            reply = 0
                        comment = comment.xpath('.//div[@class="wz"]/p')[-2].xpath('./text()').extract_first()
                        # ro = re.compile('\[ca(.*?)\]')
                        # pResult = ro.search(comment).group(0)
                        # if len(pResult):
                        #     for str in pResult:
                        #         comment = comment.replace(str,'')
                        # print('userImg:%s---userId:%s---public:%s---click:%s---up:%s---reply:%s---comment:%s' % (userImg,userId,public,click,up,reply,comment))

                        item = CommentItem()
                        vc_name = response.meta['bookName']
                        vc_url = response.meta['bookURL']
                        vc_infoid = response.meta['bookId']

                        vc_userName = username
                        vc_userImg = userImg
                        vc_userId = userId
                        vc_public = v_public
                        nm_click = int(click)
                        nm_up = int(up)
                        nm_reply = int(reply)
                        vc_content = comment
                        dt_create = datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
                        dt_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        for field in item.fields:
                            try:
                                item[field] = eval(field)
                            except NameError:
                                # print('Field is Not Defined', field)
                                pass

                        yield item
        else:
            print 'get comment errorcode=', response.status

        ##################################

    def parse_girlTotalPage(self, response):
        if response.status == 200:
            if response:
                totalPage = response.xpath('//div[@class="pagenumber pagebar"]/@count').extract_first()
                # print 'girlTotalPage=',totalPage

                genderTypeId = response.meta['genderTypeId']
                categoryTypeId = response.meta['categoryTypeId']

                for p in range(int(totalPage)):
                    # if p == 0:
                    request = Request(self.url.format(categoryType=categoryTypeId, genderType=genderTypeId, page=p + 1),
                                      callback=self.parse_girlStart, dont_filter=True)
                    yield request

    def parse_girlStart(self, response):
        if response.status == 200:
            if response:
                bookHrefList = response.xpath('//ul[@class="main_con"]/li//a[@class="fs14"]/@href').extract()
                # print('HrefList=', len(bookHrefList))
                for i, url in enumerate(bookHrefList):
                    # if i == 0:
                    request = Request(url, callback=self.parse_girlComment, dont_filter=True)
                    yield request

    # 评论页
    def parse_girlComment(self, response):
        if response.status == 200:
            if response:
                bookURL = response.url
                # bid
                bookId = response.url.replace('http://', '').replace('.html', '').split('/')[-1]
                # bname
                bookName = response.xpath('//div[@class="lebg"]/h1/a/text()').extract_first()

                # 请求评论列表
                url = 'http://huayu.baidu.com/api/forum/getThreadList.htm'
                data = {
                    'bookId': bookId,
                    'pageNo': '0'
                }
                request = FormRequest(url, callback=self.girlCommData, formdata=data, dont_filter=True)
                request.meta['bookName'] = bookName
                request.meta['bookURL'] = bookURL
                request.meta['bookId'] = bookId
                yield request

    def girlCommData(self, response):
        if response.status == 200:
            if response:
                # 获取评论总页数
                comment_totalPage = response.xpath('//div[@class="page"]/a[@class="go_page"]')[-2].xpath(
                    './@page').extract_first()
                # print 'girlComment_totalPage=', comment_totalPage
                for page in range(int(comment_totalPage)):
                    # if page==0:
                    url = 'http://huayu.baidu.com/api/forum/getThreadList.htm'
                    data = {
                        'bookId': response.meta['bookId'],
                        'pageNo': str(page + 1),
                    }
                    request = FormRequest(url, formdata=data, callback=self.parse_girlMoreComment, dont_filter=True)
                    request.meta['bookName'] = response.meta['bookName']
                    request.meta['bookURL'] = response.meta['bookURL']
                    request.meta['bookId'] = response.meta['bookId']
                    yield request

    def parse_girlMoreComment(self, response):
        if response.status == 200:
            if response:
                commentList = response.xpath('//div[@class="comment_block"]')
                if len(commentList) > 0:
                    for i, comment in enumerate(commentList):
                        # if i==0:
                        username = comment.xpath('.//div[@class="support"]/span/a/text()').extract_first()
                        # print('name=',username)
                        userImg = comment.xpath('.//div[@class="img_box"]/a/img/@src').extract_first()
                        userId = comment.xpath('.//div[@class="img_box"]/a/@href').extract_first().replace('http://', '').replace(
                            '.html', '').split('/')[-1]
                        v_public = comment.xpath('.//div[@class="fr"]/span')[0].xpath('./text()').extract_first().encode('utf-8').replace('日期: ',
                                                                                                                        '')
                        reply = comment.xpath('.//div[@class="fr"]/span')[1].xpath('./text()').extract_first().encode('utf-8').replace('回复数:',
                                                                                                                       '')
                        click = comment.xpath('.//div[@class="fr"]/span')[2].xpath('./text()').extract_first().encode('utf-8').replace('点击数:',
                                                                                                                       '')
                        up = comment.xpath('.//div[@class="fr"]/span')[3].xpath('./text()').extract_first().encode('utf-8').replace('支持[',
                                                                                                                    '').replace(
                            ']', '')
                        comment = comment.xpath('.//div[@class="wz_box"]/p/text()').extract_first().strip()
                        ro = re.compile('\[ca(.*?)\]')
                        pResult = ro.search(comment)
                        if pResult:
                            pResult = pResult.group(0)
                            for str in pResult:
                                comment = comment.replace(str,'')
                        # print('userImg:%s---userId:%s---public:%s---click:%s---up:%s---reply:%s---comment:%s' % (userImg,userId,public,click,up,reply,comment))
                        item = CommentItem()
                        vc_name = response.meta['bookName']
                        vc_url = response.meta['bookURL']
                        vc_infoid = response.meta['bookId']
                        vc_userName = username
                        vc_userImg = userImg
                        vc_userId = userId
                        vc_public = v_public
                        nm_click = int(click)
                        nm_up = int(up)
                        nm_reply = int(reply)
                        vc_content = comment
                        dt_create = datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
                        dt_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        for field in item.fields:
                            try:
                                item[field] = eval(field)
                            except NameError:
                                # print('Field is Not Defined', field)
                                pass
                        yield item
