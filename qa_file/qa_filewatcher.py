import watchdog
import logdebug
import readconfig
from f_email.sendemail import *
from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer
from qa_file.qa_incoming import *


from watchdog.observers.polling import PollingObserver
# from watchdog.events import LoggingEventHandler

import time
from pc_file.pc_titration import *
import sql

WATCH_PATH = readconfig.readcon("qa_manual","path") # 监控目录
HISTORY_FILE = readconfig.readcon("qa_manual","filelog") # 监控目录
EMAILADDR = readconfig.readcon("qa_manual","emailaddr") #

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

# class LoggingEventHandler(FileSystemEventHandler):
#     def __init__(self, **kwargs):
#         super(LoggingEventHandler, self).__init__(**kwargs)
#         # 监控目录 目录下面以device_id为目录存放各自的图片
#         self._watch_path = WATCH_PATH
#
#     # 重写文件改变函数，文件改变都会触发文件夹变化
#     def on_modified(self, event):
#         if(".tmp" in event.src_path) or '~$' in event.src_path or ".TMP" in event.src_path:
#             return
#
#         if not event.is_directory:  # 文件改变都会触发文件夹变化
#             file_path = event.src_path
#             print("文件改变: %s " % file_path)
#
#         # if(".xlsx" in event.src_path ):
#         #     print("is an xlsx file")
#         #     filescan = FileScan(HISTORY_FILE)
#         #     if filescan.scanfile(event.src_path) == False:  # did not have save this file before
#         #
#         #         res = read_pc_Titration(event.src_path)
#         #         for x in res:
#         #             sql.insert_pc_to_mysql(x)
#         #
#         #         filescan.recordfile(event.src_path)
#         #     filescan.__del__()
#
#
#
#     def on_created(self, event):
#         if(".tmp" in event.src_path) or '~$' in event.src_path or ".TMP" in event.src_path:
#             return
#         print('创建了文件', event.src_path)
#
#         if(".xlsx" in event.src_path ):
#             print("is an xlsx file")
#             filescan = FileScan(HISTORY_FILE)
#             if filescan.scanfile(event.src_path) == False:  # did not have save this file before
#
#                 # res = read_pc_Titration(event.src_path)
#                 time.sleep(1)
#
#                 try:
#                     res = read_pc_Titration(event.src_path)
#                     # print(res[0])
#                     if (res.__len__() != 42):  # last judge  and check
#                         print('lines is wrong',res.__len__())
#                         # print(res)
#                         return
#
#                     if res[0]['location'] != 'NC-DEP1-HKOH-1':
#                         print('not right file ,location is wrong',event.src_path,res[0]['location'])
#                         return
#                 except Exception as  e:
#                     # print(e)
#                     print('not right file  Exception',event.src_path,e)
#                     return
#
#
#                 for x in res:
#                     sql.insert_pc_to_mysql(x)
#                 print('record file ',event.src_path)
#                 res = email(EMAILADDR,event.src_path+'    is recording')
#                 if res!=0:
#                     print(res)
#                 filescan.recordfile(event.src_path)
#             filescan.__del__()
#
#
#     # def on_moved(self, event):
#     #     print("移动了文件", event.src_path)
#     #
#     # def on_deleted(self, event):
#     #     print("删除了文件", event.src_path)
#
#     # def on_any_event(self, event):
#     #     if(event.src_path != self._watch_path):
#     #         print("都会触发", event.src_path)

class LoggingEventHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(LoggingEventHandler, self).__init__(**kwargs)
        # 监控目录 目录下面以device_id为目录存放各自的图片
        self._watch_path = WATCH_PATH

    # 重写文件改变函数，文件改变都会触发文件夹变化
    def on_modified(self, event):
        if(".tmp" in event.src_path) or '~$' in event.src_path or ".TMP" in event.src_path:
            return

        if not event.is_directory:  # 文件改变都会触发文件夹变化
            file_path = event.src_path
            print("文件改变: %s " % file_path)

        # if(".xlsx" in event.src_path ):
        #     print("is an xlsx file")
        #     filescan = FileScan(HISTORY_FILE)
        #     if filescan.scanfile(event.src_path) == False:  # did not have save this file before
        #
        #         res = read_pc_Titration(event.src_path)
        #         for x in res:
        #             sql.insert_pc_to_mysql(x)
        #
        #         filescan.recordfile(event.src_path)
        #     filescan.__del__()



    def on_created(self, event):
        if(".tmp" in event.src_path) or '~$' in event.src_path or ".TMP" in event.src_path:
            return
        print('创建了文件', event.src_path)

        if(".xlsx" in event.src_path ):
            print("is an xlsx file")
            filescan = FileScan(HISTORY_FILE)
            if filescan.scanfile(event.src_path) == False:  # did not have save this file before

                # res = read_pc_Titration(event.src_path)
                time.sleep(1)

                try:
                    res = read_qa_incomming(event.src_path)
                    # print(res[0])
                    # if (res.__len__() != 42):  # last judge  and check
                    #     print('lines is wrong',res.__len__())
                    #     # print(res)
                    #     return
                    res_thckness = res['thickness']
                    res_roughness = res['roughness']
                    # if res[0]['location'] != 'NC-DEP1-HKOH-1':
                    #     print('not right file ,location is wrong',event.src_path,res[0]['location'])
                    #     return
                except Exception as  e:
                    # print(e)
                    print('not right file  Exception',event.src_path,e)
                    return


                for x in res_thckness:
                    sql.insert_qa_spc_thickness_to_mysql(x)
                for x in res_roughness:
                    sql.insert_qa_spc_roughness_to_mysql(x)

                print('record file ',event.src_path)
                # res = email(EMAILADDR,event.src_path+'    is recording')
                # if res!=0:
                #     print(res)
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