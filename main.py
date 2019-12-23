import sql
import mq_c
import time
import thread_in
import logdebug
import filewatch
import threading
import readconfig
from MtConnect.readMtThread import  *
# from concurrent.futures import ThreadPoolExecutor
#
# pool = ThreadPoolExecutor(max_workers=10)

def main():

    logdebug.configlog()
    logdebug.logdeb("start")
    try:
        filewatch.file_Watch_init()
    except Exception as err:
        logdebug.logdeb(err)
        logdebug.logdeb('filewatch fail  !!!!!!!!!!!1')


    sql.connect_to_mysql()

    mazak1050url = readconfig.readcon("MtConnect","mazak1050url")
    mazak530_0url = readconfig.readcon("MtConnect", "mazak530_0url")
    mazak530_1url = readconfig.readcon("MtConnect", "mazak530_1url")


    mq_thread=mq_c.mqthread(1,"mq-thread")
    mq_thread.setDaemon(True)

    Mazak1050 = readMtThread(2,"Mazak1050",url=mazak1050url,No=0)
    mazak530_0 = readMtThread(2,"Mazak1050",url=mazak530_0url,No=1)
    mazak530_1 = readMtThread(2,"Mazak1050",url=mazak530_1url,No=2)

    Mazak1050.setDaemon(True)
    mazak530_0.setDaemon(True)
    mazak530_1.setDaemon(True)


    Mazak1050.start()
    mq_thread.start()
    # mazak530_0.start()
    # mazak530_1.start()

    # test_thread.start()

    while True:

        # print("main loop",threading.activeCount())
        # print(threading.enumerate())
        time.sleep(10)


if __name__ == '__main__':
    main()