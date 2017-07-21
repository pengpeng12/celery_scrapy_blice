#coding=utf-8

from settings import mysql_setting
from task_logging import task_logging
import time
import MySQLdb
import socket


IP = mysql_setting.ali_mysql["IP"]
UserName = mysql_setting.ali_mysql["UserName"]
PassWord = mysql_setting.ali_mysql["PassWord"]
DataBase = mysql_setting.ali_mysql["DataBase"]
Port = mysql_setting.ali_mysql["PORT"]


db = MySQLdb.connect(IP,UserName,PassWord,DataBase,port=Port)
db.set_character_set('utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
createTime = time.strftime("%Y-%m-%d",time.localtime())
updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())



logging = task_logging.log_maker(printInfo=False)

DabaseError = "DabaseError"

class weboDataBase:

    def __init__(self):
        self.db = db
        self.cursor = cursor

    def getInfoFromDatabase(self,sql,type=1,byip=True):
        '''
        执行传入的sql，默认数据库是ysali
        '''

        if not byip:

            pass

        else:
            if type == 1:
                try:
                    return [i for i in cursor.fetchmany(cursor.execute(sql))]
                except Exception,e:
                    logging.error(msg="{}:{},{}".format(DabaseError,e,sql))
                    return list()
            else:
                try:
                    return [i[0] for i in cursor.fetchmany(cursor.execute(sql))]
                except Exception,e:
                    logging.error(msg="{}:{},{}".format(DabaseError,e,sql))
                    return list()


    def setInfoToDataBase_sql_insert(self,sql,args):
        '''
        insert数据
        '''
        self.cursor.execute(sql,args)
        self.db.commit()

    def setInfoToDataBase_sql_update(self,sql):

        '''
        updata更新数据
        '''
        self.cursor.execute(sql)
        self.db.commit()


    def setInfoToDataBase_proc(self,proc_name,args):
        '''
        默认执行存储过程入库,传入存储过程的名称，参数
        '''
        try:
            self.cursor.callproc(proc_name,args)
            self.db.commit()
            logging.info(msg="{}--task done !".format(proc_name))
        except Exception,r:
            logging.error(msg="{}:{},{}".format(DabaseError,r,proc_name))


    def closeDataBase(self):
        '''
        关闭指针，关闭数据库
        '''
        logging.info('database close :{}'.format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())))
        self.cursor.close()
        self.db.close()



