# coding=utf-8
import os
import sys
from ftplib import FTP  # 引入ftp模块
# from ftplib import FTP_TLS


class MyFtp:
    ftp = FTP()

    def connect(self, host, port=21):
        self.ftp.connect(host, port)

    def login(self, username, pwd):
        self.ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
        self.ftp.login(username, pwd)
        print(self.ftp.welcome)

    def downloadFile(self, localpath, remotepath, filename):
        # print(os.path.abspath(os.path.dirname(__file__)))
        # print(sys.path[0])
        #
        # print(sys.argv[0])
        #
        # print(os.path.dirname(os.path.realpath(sys.executable)))
        #
        # print(os.path.dirname(os.path.realpath(sys.argv[0])))
        os.chdir(localpath)  # 切换工作路径到下载目录
        self.ftp.cwd(remotepath)  # 要登录的ftp目录
        self.ftp.nlst()  # 获取目录下的文件
        file_handle = open(filename, "wb").write  # 以写模式在本地打开文件
        self.ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handle, blocksize=1024)  # 下载ftp文件
        # ftp.delete（filename）  # 删除ftp服务器上的文件
        # path = os.path.dirname(os.path.realpath(sys.executable))
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            os.chdir(application_path)
        elif __file__:
            application_path = os.path.dirname(__file__)
            os.chdir(application_path)
        # os.chdir(path)
        # print(os.path.abspath(os.path.dirname(__file__)))


    def close(self):
        self.ftp.set_debuglevel(0)  # 关闭调试
        self.ftp.quit()

    def transfile(self, ip, username, password, path, filename):
        self.connect(ip)
        self.login(username, password)
        self.downloadFile(path, '', filename)
        self.close()
