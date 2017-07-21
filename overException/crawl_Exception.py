#coding=utf-8


class ERROR(Exception):
    '''基于celery的爬虫基本异常类'''
    pass


class TIMEOUT_EXCEPTION(ERROR):
    '''基于celery的请求网页出现超时异常'''
    pass

class URL_EXCEPTION(ERROR):
    '''基于celery的请求url出现异常'''
    pass


class DATABASE_EXCEPTION(ERROR):
    '''基于celery的数据库入库异常异常'''
    pass


class WORKER_EXCEPTION(ERROR):
    '''基于celery的worker节点出现异常'''
    pass


class TASK_EXCEPTION(ERROR):
    '''基于celery的task节点出现异常'''
    pass


class MAIL_EXCEPTION(ERROR):
    '''基于celery的邮件异常'''
    pass



