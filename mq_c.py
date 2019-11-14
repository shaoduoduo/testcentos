import pika
import json
import sql
import threading
import logdebug
import readconfig
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
        self.mq_init()
        #
    def callback(self,ch,method,properties,body):
        # print("[custmer] receive",body)
        dictdata = json.loads(body)

        # print(dictdata['location'])
        sql.insert_to_mysql(dictdata)
        # print("thread name",self.getName())
    def mq_init(self):
        username = readconfig.readcon('rabbitmq','username')
        pwd = readconfig.readcon('rabbitmq','pwd')
        host = readconfig.readcon('rabbitmq','host')
        queue = readconfig.readcon('rabbitmq','queue')
        useer_pwd = pika.PlainCredentials(username,pwd)

        s_conn = pika.BlockingConnection(pika.ConnectionParameters(host,credentials=useer_pwd))
        chan = s_conn.channel()

        # chan.queue_declare(queue=queue)

        chan.basic_consume(queue,self.callback,True)
        logdebug.logdeb("custmer wait for mes")
        chan.start_consuming()