import threading
import time

class mythread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID =threadID
        self.name = name
    def run(self):
        print("start thread:"+self.name)
        while True:
            time.sleep(5)

