from datetime import datetime


import logging

import threading
def configlog():
    current = datetime.now()
    time_str = datetime.strftime(current,"%Y-%m-%d")
    time_str = time_str+'.log'
    logging.basicConfig(filename=time_str,level=logging.WARNING,format='%(asctime)s:%(levelname)s:%(message)s')

def logdeb(msg,*args,**kwargs):
    logging.warning(msg,*args,**kwargs)

    print(msg,">>>>>>thread name is ",threading.currentThread().getName())

