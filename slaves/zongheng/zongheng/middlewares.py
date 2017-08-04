# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random
import requests
# from scrapy import signals
#
#
class ZonghengSpiderMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.ipList = ["122.114.82.64", "120.24.216.121", "123.206.121.190", "139.199.160.49", "120.26.167.145",
        #            "115.28.141.184", "115.28.141.184", "122.114.167.92", "115.159.147.178",
        #            "112.74.198.237", "123.206.197.28"
        #            ]
        result = requests.get('http://dev.kuaidaili.com/api/getproxy?orderid=949187989849476&num=100&kps=1')
        if result.status_code == 200:
            self.ipList = result.text.split('\n')
            # print self.ipList

    def get_rand_ip(self):
        # 代理ip
        rand = random.randint(0, len(self.ipList) - 1)
        dlIp = self.ipList[rand]
        self.logger.debug('Using ip------' + dlIp)
        return "http://" + dlIp

    def process_request(self, request, spider):
        request.meta['proxy'] = self.get_rand_ip()