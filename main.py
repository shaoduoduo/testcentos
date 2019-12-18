import sql
import mq_c
import time
import thread_in
import logdebug
import filewatch
import threading
import os
# from concurrent.futures import ThreadPoolExecutor
#
# pool = ThreadPoolExecutor(max_workers=10)

def main():

    logdebug.configlog()
    logdebug.logdeb("start")

    filewatch.file_Watch_init()
    sql.connect_to_mysql()

    mq_thread=mq_c.mqthread(1,"mq-thread")
    # test_thread = thread.mythread(2,"my-thread")
    mq_thread.setDaemon(True)

    mq_thread.start()

    # test_thread.start()

    while True:

        # print("main loop",threading.activeCount())
        # print(threading.enumerate())
        time.sleep(10)


if __name__ == '__main__':
    main()