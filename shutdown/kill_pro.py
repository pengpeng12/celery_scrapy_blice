#coding=utf-8

import sys,os
pathjoin = os.path.dirname(__file__)
if sys.platform != "win32":
    sys.path.append("/".join(os.getcwd().split("/")[:-1]))

sys.path.append("/opt/vdb/libin/celery_blice")


from job_maker.mysql_connection import weboDataBase
import time,socket,re
localip = socket.gethostbyname(socket.gethostname())

def kill_process_by_name(name):
    process_list = []
    cmd = "ps -ef | grep %s|grep -v grep|grep -v kill_pro" % name
    f = os.popen(cmd)
    txt = f.readlines()
    if len(txt) == 0:
        print "no process \"%s\"!!" % name
        return
    else:
        for line in txt:
            colum = line.split()
            pid = colum[1]
            if ":" not in colum[4]:
                cmd = "kill -9 %d" % int(pid)
                print cmd
                os.system(cmd)
            else:
                if re.search('\/(.*?\.((py)|(sh)))',line):
                    name_pid = re.search('\/(.*?\.((py)|(sh)))',line).group(1).split("/")[-1]
                else:
                    name_pid = line
                process_list.append((name_pid,pid))


    #监控进程数，发现是否启动采集程序，将结果写到数据库
    for (vname,pid) in process_list:
        create = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #count_process = list(set(process_list)).__len__()
        sql = "INSERT INTO linux_pid (dt_create,vc_pid,vc_name,vc_ip,vc_class)  VALUES (%s,%s,%s,%s,%s)"
        agrs = (create,pid,str(vname),localip,name)
        weboDataBase().setInfoToDataBase_sql_insert(sql,agrs)


if __name__ == "__main__":
    namelist = ["iqiyi","tencent","youku","sohu","le","weibo","weixin","news","drama"]
    for name in namelist:
        print name,"process looping ..."
        kill_process_by_name(name)