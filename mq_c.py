import pika
import json
import sql
import threading

class mqthread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID =threadID
        self.name = name
    def run(self):
        print("start thread:"+self.name)
        #
        



step=0

def callback(ch,method,properties,body):
    global step
    step=step + 1
    print(step)
    # print("[custmer] receive",body)
    dictdata = json.loads(body)

    # print(dictdata['location'])
    sql.inser_to_mysql(dictdata)

def mq_init():

    username = 'python_c'
    pwd = 'python_c'
    useer_pwd = pika.PlainCredentials(username,pwd)
    s_conn = pika.BlockingConnection(pika.ConnectionParameters('10.10.10.245',credentials=useer_pwd))
    chan = s_conn.channel()

    chan.queue_declare(queue='111')

    chan.basic_consume('111',callback,True)
    print("custmer wait for mes")
    chan.start_consuming()