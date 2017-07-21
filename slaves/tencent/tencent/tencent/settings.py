# -*- coding: utf-8 -*-

# Scrapy settings for tencent project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tencent'

SPIDER_MODULES = ['tencent.spiders']
NEWSPIDER_MODULE = 'tencent.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tencent (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# MySQL数据库连接配置
MYSQL_HOST = '10.27.216.133'
MYSQL_PORT = 6306
MYSQL_DB = "ysali"
MYSQL_USR = 'aliPa'
MYSQL_PWD = '6y3*p*o$Uj>1s$H'

ITEM_PIPELINES = {
    'tencent.pipelines.TencentPipeline': 300,#保存到mysql数据库

}

# 默认Item并发数：100
CONCURRENT_ITEMS = 200

# 默认Request并发数：16
CONCURRENT_REQUESTS = 100

# 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN = 64

#设置Log的级别
LOG_LEVEL='DEBUG'
#
#Configure log file name
#LOG_FILE = "D:\linuxPro\libin\sohu\sohuVideo\sohuVideo\spiders\scrapy.log"
#COOKIES_ENABLED=False

#DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'tencent.middlewares.RotateUserAgentMiddleware' :400
    }

EXTENSIONS = {
    'tencent.task_done.Task_done': 500

}
