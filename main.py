import sql
import mq_c
import time
import thread
import threading
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=10)


def main():
    sql.connect_to_mysql()
    # mq_c.mq_init()
    mq_thread=mq_c.mqthread(1,"mq-thread")
    test_thread = thread.mythread(2,"my-thread")
    mq_thread.start()
    # test_thread.start()
    while True:
        time.sleep(5)
        # print("main loop",threading.activeCount())
        # print(threading.enumerate())


if __name__ == '__main__':
    main()