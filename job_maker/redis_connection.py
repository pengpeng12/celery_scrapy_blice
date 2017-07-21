#coding=utf-8

import redis

from settings import reids_setting
from task_logging import task_logging

class Redis_blice:

    '''获取配置文件'''
    setting_dict = reids_setting.ali_redis
    pool = redis.ConnectionPool(host=setting_dict["IP"],password=setting_dict["PASSWORD"],\
                                port=setting_dict["PORT"],db=0)

    def __str__(self):
        return 'Redis_blice'

    @classmethod
    def connection_pool(cls):
        r = redis.Redis(connection_pool=cls.pool)
        return r

    @classmethod
    def table_info_hash(cls,tableName):

        ''' get info by tablename '''

        if isinstance(tableName,str):
            r = cls.connection_pool()
            return r.hgetall(tableName)
        else:
            return None

    @classmethod
    def push_list(cls,listname,name):
        cls.connection_pool().lpush(listname,name)


if __name__ == "__main__":
    print Redis_blice.table_info_hash("tencent")