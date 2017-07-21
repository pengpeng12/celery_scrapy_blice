#coding=utf-8
import os

# print os.getcwd()
#print os.path.dirname(__file__)
# print __file__


class nowip(object):

    @property
    def local_ip(self):
        import socket
        try:
            localip = socket.gethostbyname(socket.gethostname())
            return localip
        except Exception,e:
            return e


if __name__ == "__main__":
    print nowip().local_ip