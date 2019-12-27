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
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID =threadID
        self.name = name
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
        # sql.insert_to_mysql(dictdata)
        # print("thread name",self.getName())
    def callback_opc(self,ch,method,properties,body):
        # print("[custmer] receive",body)
        dictdata = json.loads(body)
        sql.insert_to_mysql(dictdata)

        pass

    def callback_mt(self,ch,method,properties,body):
        # print("[custmer] receive",body)
        dictdata = json.loads(body)
        sql.insert_to_mysql(dictdata)

    def callback_particles(self,ch,method,properties,body):
        # print("[custmer] receive",body)
        dictdata = json.loads(body)
        sql.insert_particles_to_mysql(dictdata)
        pass
    def mq_init(self):
        username = readconfig.readcon('rabbitmq','username')
        pwd = readconfig.readcon('rabbitmq','pwd')
        host = readconfig.readcon('rabbitmq','host')
        virtual_host = readconfig.readcon('rabbitmq','virtual_host')
        queue_opc = readconfig.readcon('rabbitmq','queue_opc')
        queue_mt = readconfig.readcon('rabbitmq','queue_mt')
        queue_particles = readconfig.readcon('rabbitmq','queue_particles')

        useer_pwd = pika.PlainCredentials(username,pwd)

        s_conn = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=virtual_host, host = host,credentials=useer_pwd))

        chan = s_conn.channel()

        # chan.queue_declare(queue=queue)


        chan.basic_consume(queue_opc,self.callback_opc,True)
        # chan.basic_consume(queue_mt,self.callback_mt,True)
        chan.basic_consume(queue_particles,self.callback_particles,True)


        logdebug.logdeb("custmer wait for mes"+'---->>opc')
        chan.start_consuming()