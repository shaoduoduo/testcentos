import watchdog
import logdebug
import readconfig
import readxls
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCH_PATH = readconfig.readcon("pc_mount","path") # 监控目录


class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(FileMonitorHandler, self).__init__(**kwargs)
        # 监控目录 目录下面以device_id为目录存放各自的图片
        self._watch_path = WATCH_PATH

    # 重写文件改变函数，文件改变都会触发文件夹变化
    def on_modified(self, event):
        if not event.is_directory:  # 文件改变都会触发文件夹变化
            file_path = event.src_path
            print("文件改变: %s " % file_path)
            readexcel = readxls.readexcel(file_path)
            readexcel.init()

    # def on_created(self, event):
    #     print('创建了文件夹', event.src_path)


    # def on_moved(self, event):
    #     print("移动了文件", event.src_path)

    def on_deleted(self, event):
        print("删除了文件", event.src_path)

    # def on_any_event(self, event):
    #     print("都会触发")
    #

def file_Watch_init():
    event_handler = FileMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_PATH, recursive=True)  # recursive递归的
    observer.start()
    # observer.join()