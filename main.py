import os
par_dir = os.path.dirname(os.path.abspath(__file__))
print(par_dir)
os.chdir(par_dir)
import sql
import rabbit_mq.mq_c
import rabbit_mq.mq_thread
import rabbit_mq.mq_arc1
import rabbit_mq.mq_arc2
import time
import thread_in
import logdebug
import datetime
import filewatch
import threading
import readconfig
import pc_file.pc_filewatcher as pc_f
import qa_file.qa_filewatcher as qa_f
from MtConnect.readMtThread import  *
from send_mail_elec import *
import rabbit_mq.mq_anodize
from time_clock import *
from plasma import lpcopcread
from pc_particle import web_pc
from pc_particle import web_pc_lpc
from opcwebread import fcopc,particleopc
# from concurrent.futures import ThreadPoolExecutor
#
# pool = ThreadPoolExecutor(max_workers=10)

def main():

    # return

    sql.connect_to_mysql()
    logdebug.configlog()
    print("start")

    # try:
    #     pc_f.file_Watch_init()
    # except Exception as err:
    #     logdebug.logdeb(err)
    #     logdebug.logdeb('pc  filewatch fail  !!!!!!!!!!!1')


    # try:
    #     qa_f.file_Watch_init()
    # except Exception as err:
    #     logdebug.logdeb(err)
    #     logdebug.logdeb('qa  filewatch fail  !!!!!!!!!!!1')
    #

    mazak1050url = readconfig.readcon("MtConnect","mazak1050url")
    mazak530_0url = readconfig.readcon("MtConnect", "mazak530_0url")
    mazak530_1url = readconfig.readcon("MtConnect", "mazak530_1url")


    #
    # mq_thread=rabbit_mq.mq_c.mqthread(1,"mq-thread")
    # mq_thread.setDaemon(True)
    # mq_pc_lpc =rabbit_mq.mq_thread.mqthread(5,'pc_lpc','rabbitmq_LPC')    #start pc_lpc data sollect
    # mq_pc_lpc.setDaemon(True)



    Mazak1050 = readMtThread(2,"Mazak1050",url=mazak1050url,No=0)
    mazak530_0 = readMtThread(3,"mazak530_0",url=mazak530_0url,No=1)
    mazak530_1 = readMtThread(4,"mazak530_1",url=mazak530_1url,No=2)

    Mazak1050.setDaemon(True)
    mazak530_0.setDaemon(True)
    mazak530_1.setDaemon(True)

    mq_arc1 = rabbit_mq.mq_arc1.mqthread(5,'st_arc1','rabbitmq_ARC1')
    mq_arc1.setDaemon(True)
    mq_arc2 = rabbit_mq.mq_arc2.mqthread(6,'st_arc2','rabbitmq_ARC2')
    mq_arc2.setDaemon(True)

    mq_anodize = rabbit_mq.mq_anodize.mqthread(7,'anodize','rabbitmq_anodize')
    mq_anodize.setDaemon(True)

    threadplasma1 = lpcopcread.opcwbthread(8,'plasma1','plasma1')
    threadplasma1.setDaemon(True)

    threadplasma2 = lpcopcread.opcwbthread(9, 'plasma2', 'plasma2')
    threadplasma2.setDaemon(True)

    thread_pc_particle = web_pc.pc_particle_thread(10,'pc_particle','pc_particle')
    thread_pc_particle.setDaemon(True)


    thread_pc_lpc = web_pc_lpc.pc_lpc_thread(11,'pc_lpc','pc_lpc')
    thread_pc_lpc.setDaemon(True)


    thread_fc_opc= fcopc.fc_opc_thread(12,'fc_opc','fc_opc')
    thread_fc_opc.setDaemon(True)

    thread_particle_opc= particleopc.particleopc(13,'particle_opc','particle_opc')
    thread_particle_opc.setDaemon(True)
    # threadplasma1.start()
    # threadplasma2.start()


    # Mazak1050.start()
    # mq_thread.start()#opc
    # mazak530_0.start()
    # mazak530_1.start()
    # mq_pc_lpc.start()#lpc

    mq_arc1.start()
    mq_arc2.start()
    # mq_anodize.start()

    # thread_pc_particle.start()
    # thread_pc_lpc.start()
    # thread_fc_opc.start()
    thread_particle_opc.start()
    static_cnt = 0
    while True:

        #print("main loop",threading.activeCount(),datetime.now())
        # print(threading.enumerate())
        time.sleep(60)
        #send mail to fc
        static_cnt +=1

        # if static_cnt % (12*24) == 0:#24h
        #     sql.close_to_mysql()
        #     sql.connect_to_mysql()
        if True == clock_loop(17,1):
            try :
                # elec_mail()
                pass
            except Exception as err:
                logdebug.logdeb('send mail error',err)



if __name__ == '__main__':
    main()