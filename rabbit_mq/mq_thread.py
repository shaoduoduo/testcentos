import pika
import json
import sql
import threading
import logdebug
import readconfig
import time
#
# []
# host= 10.10.10.245
# username = python_c
# pwd = python_c
# queue = 111


class mqthread(threading.Thread):
    def __init__(self,threadID,name,location):#location meaning whitch mq is chossed eg. PC_LPC
        threading.Thread.__init__(self)
        self.threadID =threadID
        self.name = name
        self.location = location
    def run(self):
        logdebug.logdeb("start thread:"+self.name)
        while True:
            try:
                self.mq_init()
                break
            except Exception as err:
                print('mq_init err :',err)
            time.sleep(5)

    def callback(self,ch,method,properties,body):
        # print("[custmer] receive",body)
        dictdata = json.loads(body)

        # print(dictdata['location'])
        if self.location == 'PC_LPC':
            # sql.insert_to_mysql(dictdata)
            print(dictdata)

        # print("thread name",self.getName())
    def mq_init(self):
        username = readconfig.readcon(self.location,'username')
        pwd = readconfig.readcon(self.location,'pwd')
        host = readconfig.readcon(self.location,'host')
        virtual_host = readconfig.readcon(self.location,'virtual_host')
        queue = readconfig.readcon(self.location,'queue_opc')

        useer_pwd = pika.PlainCredentials(username,pwd)

        s_conn = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=virtual_host, host = host,credentials=useer_pwd))

        chan = s_conn.channel()

        # chan.queue_declare(queue=queue)


        chan.basic_consume(queue,self.callback,True)
        # chan.basic_consume(queue_mt,self.callback_mt,True)
        # chan.basic_consume(queue_particles,self.callback_particles,True)


        logdebug.logdeb("custmer wait for mes---->>>",self.location)
        chan.start_consuming()