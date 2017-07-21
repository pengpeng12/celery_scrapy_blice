#coding=utf-8

import logging
import os
import time
import sys

timeDay = time.strftime("%Y-%m-%d",time.localtime())

#判断平台写日志路径
if sys.platform != "win32":
    logging_path = "/opt/vdb/logs/celery/"
else:
    logging_path = "D:\celery_log"

if not os.path.exists(logging_path):
    os.mkdir(logging_path)
else:
    logging_file = logging_path+timeDay+".txt"


def log_maker(level=logging.DEBUG,filename="./maker.log",printInfo=True):
    logging.basicConfig(level=level,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='{}'.format(filename),
                    filemode='ab')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    if printInfo:
        logging.getLogger('').addHandler(console)
    return logging


if __name__ == "__main__":
    logger = log_maker(printInfo=False)
    logger.info("fasga")
