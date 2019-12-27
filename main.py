import sql
import rabbit_mq.mq_c
import rabbit_mq.mq_thread
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
    print("start")
    try:
        filewatch.file_Watch_init()
    except Exception as err:
        logdebug.logdeb(err)
        logdebug.logdeb('filewatch fail  !!!!!!!!!!!1')


    sql.connect_to_mysql()

    mazak1050url = readconfig.readcon("MtConnect","mazak1050url")
    mazak530_0url = readconfig.readcon("MtConnect", "mazak530_0url")
    mazak530_1url = readconfig.readcon("MtConnect", "mazak530_1url")


    mq_thread=rabbit_mq.mq_c.mqthread(1,"mq-thread")
    mq_thread.setDaemon(True)
    mq_pc_lpc =rabbit_mq.mq_thread.mqthread(5,'pc_lpc','rabbitmq_LPC')    #start pc_lpc data sollect
    mq_pc_lpc.setDaemon(True)


    Mazak1050 = readMtThread(2,"Mazak1050",url=mazak1050url,No=0)
    mazak530_0 = readMtThread(3,"mazak530_0",url=mazak530_0url,No=1)
    mazak530_1 = readMtThread(4,"mazak530_1",url=mazak530_1url,No=2)

    Mazak1050.setDaemon(True)
    mazak530_0.setDaemon(True)
    mazak530_1.setDaemon(True)



    Mazak1050.start()
    mq_thread.start()
    mazak530_0.start()
    mazak530_1.start()
    mq_pc_lpc.start()


    # test_thread.start()

    while True:

        print("main loop",threading.activeCount())
        # print(threading.enumerate())
        time.sleep(60)


if __name__ == '__main__':
    main()