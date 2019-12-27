
import logging

import threading
def configlog():
    logging.basicConfig(filename='logging.log',level=logging.WARNING,format='%(asctime)s:%(levelname)s:%(message)s')

def logdeb(msg,*args,**kwargs):
    logging.warning(msg,*args,**kwargs)

    print(msg,">>>>>>thread name is ",threading.currentThread().getName())

