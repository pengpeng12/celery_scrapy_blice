#coding=utf-8
import os
import sys
import time
import datetime
import json


class LoadJson(object):

    def loadJsonToFile(self,plat,vclass,items):
        ''' /opt/vdb/comments/tencent/movie/time.time().txt  时间取整数'''
        tample = time.strftime("%Y%m%d%H",time.localtime())
        filePath = "/opt/vdb/comments/{}/{}".format(plat,vclass)
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            learnPath = filePath+"/"+str(int(tample))+".txt"
            self.writeJson(items,learnPath)
        else:
            learnPath = filePath+"/"+str(int(tample))+".txt"
            self.writeJson(items,learnPath)


    def writeJson(self,items,learnPath):
        with open(learnPath,"a+") as files:
            try:
                if isinstance(items,dict):
                    jsonItem = json.dumps(items)
                    files.write(jsonItem+"\r\n")
                else:
                    jsonItem = json.dumps(dict(items))
                    files.write(jsonItem+"\r\n")

            except Exception,r:
                print r,time.time()


