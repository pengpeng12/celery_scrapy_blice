#coding=utf-8

from task_logging.task_logging import log_maker
from check_ips.spider_ip import nowip
from check_ips.useips import spider_ips
from overException.crawl_Exception import *

logger = log_maker(printInfo=False)

#函数执行时间
def time_run(usetime):
    import time
    timeNow = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    def fuc(*args,**kwargs):
        logger.info("{}:{}".format(timeNow,usetime.__name__))
        return usetime(*args,**kwargs)
    return fuc


#函数运行开始、结束状态写入数据库
def load_sign2mysql(usetime):
    import time
    timeNow = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    def fuc(*args,**kwargs):
        logger.info("{}:{}".format(timeNow,usetime.__name__))
        return usetime(*args,**kwargs)
    return fuc


#计数发生的异常
def Exception_counter(fuc):
    def ex_c(*args,**kwargs):
        pass
        return fuc(*args,**kwargs)
    return ex_c


#监控过滤采集ip
def check_ip(fuc):
    def cm(*args,**kwargs):
        spider_ip = nowip().local_ip
        if spider_ip in spider_ips.values():
            return fuc(*args,**kwargs)
        else:
            raise WORKER_EXCEPTION
            return
    return cm


if __name__ == "__main__":
    pass