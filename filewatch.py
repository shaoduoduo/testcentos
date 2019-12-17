import watchdog
import logdebug
import readconfig
import readxls
from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer

from watchdog.observers.polling import PollingObserver
from watchdog.events import LoggingEventHandler

import time
WATCH_PATH = readconfig.readcon("pc_mount","path") # 监控目录
HISTORY_FILE = readconfig.readcon("pc_mount","filelog") # 监控目录
class FileScan():
    def __init__(self,history):
        self.history = history
        self.fp = open(self.history,"a+")
        self.fp.seek(0,0)

    def recordfile(self,filename):
        #record the file
        self.fp.write(filename+time.strftime(" ---->>>>%Y-%m-%d %H:%M:%S \n",time.localtime()))

    def scanfile(self,filename):
        line = True
        res = False


        while line:
            line =self.fp.readline()
            # print("read line", line)

            isExist = filename in line

            # print(isExist)
            if isExist==True:
                logdebug.logdeb(filename+"has been read at"+line)
                res = True
                break
        self.fp.seek(0,0)#return to the first line
        # if res == False:
            # self.recordfile(filename)
            # print("record this file ")
        return res


    def __del__(self):
        self.fp.close()
#
# class FileMonitorHandler(FileSystemEventHandler):
#     def __init__(self, **kwargs):
#         super(FileMonitorHandler, self).__init__(**kwargs)
#         # 监控目录 目录下面以device_id为目录存放各自的图片
#         self._watch_path = WATCH_PATH
#
#     # 重写文件改变函数，文件改变都会触发文件夹变化
#     def on_modified(self, event):
#         if not event.is_directory:  # 文件改变都会触发文件夹变化
#             file_path = event.src_path
#             print("文件改变: %s " % file_path)
#
#             filescan = FileScan(HISTORY_FILE)
#             if filescan.scanfile(file_path) == False:#do not have save this file
#                 readexcel = readxls.readexcel(file_path)
#                 readexcel.init()#read and save file (insert into mysql)
#                 filescan.recordfile(file_path)
#             filescan.__del__()
#
#     # def on_created(self, event):
#     #     print('创建了文件夹', event.src_path)
#
#
#     # def on_moved(self, event):
#     #     print("移动了文件", event.src_path)
#
#     def on_deleted(self, event):
#         print("删除了文件", event.src_path)
#
#     def on_any_event(self, event):
#         print("都会触发")


class LoggingEventHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(LoggingEventHandler, self).__init__(**kwargs)
        # 监控目录 目录下面以device_id为目录存放各自的图片
        self._watch_path = WATCH_PATH

    # 重写文件改变函数，文件改变都会触发文件夹变化
    def on_modified(self, event):
        if not event.is_directory:  # 文件改变都会触发文件夹变化
            file_path = event.src_path
            print("文件改变: %s " % file_path)

            # filescan = FileScan(HISTORY_FILE)
            # if filescan.scanfile(file_path) == False:#do not have save this file
            #     readexcel = readxls.readexcel(file_path)
            #     readexcel.init()#read and save file (insert into mysql)
            #     filescan.recordfile(file_path)
            # filescan.__del__()

    def on_created(self, event):
        print('创建了文件夹', event.src_path)
        if(".tmp" in event.src_path):
            return
        if(".xls" in event.src_path ):
            print("is an excel file")
            filescan = FileScan(HISTORY_FILE)
            if filescan.scanfile(event.src_path) == False:  # do not have save this file
                readexcel = readxls.readexcel(event.src_path)
                readexcel.init()  # read and save file (insert into mysql)
                filescan.recordfile(event.src_path)
            filescan.__del__()

    # def on_moved(self, event):
    #     print("移动了文件", event.src_path)
    #
    # def on_deleted(self, event):
    #     print("删除了文件", event.src_path)

    # def on_any_event(self, event):
    #     if(event.src_path != self._watch_path):
    #         print("都会触发", event.src_path)


def file_Watch_init():
    # event_handler = FileMonitorHandler()
    # observer = Observer()
    # observer.schedule(event_handler, path=WATCH_PATH, recursive=True)  # recursive递归的
    # observer.start()

    event_handler = LoggingEventHandler()
    observer = PollingObserver()
    observer.schedule(event_handler,path=WATCH_PATH,recursive=True)
    observer.start()