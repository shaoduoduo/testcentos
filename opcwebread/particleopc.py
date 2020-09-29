import requests
import readconfig
import json
import simplejson
import xmltodict
import ast
import threading
import logdebug
import time
import sql
import re
import datetime

def xmltojson(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = simplejson.dumps(xmlparse)
    return jsonstr
#读取本地数据用于测试
def readjson():
    with open('js.json', 'a') as f:
        data = json.load(f)
    return data  # json 格式
save_dict = {'':0}
def check_repeat_data(location,timestamp):#检查重复数据，根据时间戳判断
    if location in save_dict:
        if save_dict[location] == timestamp:
            # print('数据重复，不发送',location,timestamp)
            return False

    save_dict[location] = timestamp
    # print('第一次出现',location,timestamp)
    return True

def wsdl(url, headers, xmlstr):
    headers = ast.literal_eval(headers)  # 转为dict格式

    data = xmlstr

    try:
        rep = requests.post(url, data=data, headers=headers)
        # rep = requests.post(url, data=data)
    except Exception as error:
        # main.logdebug(error)
        return None
    rep = rep.text

    json_str = xmltojson(rep)
    return json_str
#ss= 'LMS/Inputs/Location 112/1.0/Aggregates/Cumulative Counts/Data'
# ['112/1.0']
#TS1_2,2
def reg_location(loc):
#'ITTest.PW400030'
    rr  = 'ITTest.(.*)'
    # rr = 'ion (.*)/Ag'
    res = re.findall(rr, loc)
    if res == [] :
        return

    location = res[0]
    # res = res[0].split('/')
    # location = res
    return location
#test . location and Quality is demo
def unpackxml(json_str):
    # print("开始 解析 lpc数据")

    patt = re.compile(r'"@ItemName": "ITTest.TS1_W", "Value": {"@xsi:type": "xsd:float", "#text": "\d+.000000"}, "Quality": {"@QualityField": "[a-z]+"}')
    # patt = re.compile(restr)
    ret = re.findall(patt,json_str)

    TS1_W_locat = 0
    TS1_WQuality = 'bad'
    if (ret):
        # print(ret)
        patts = re.compile(r'\d+.000000')
        rets = re.findall(patts,ret[0])
        if (rets):
            # print(rets)
            TS1_W = float(rets[0])
            TS1_W_locat= int(TS1_W)
        else:
            print("CDAN2 数据无法解析")
            return None


        if 'good'  in ret[0]:
            TS1_WQuality = 'good'


    d = json.loads(json_str)
    body = d['soap:Envelope']

    body=body['soap:Body']
    body = body['ReadResponse']
    body = body['RItemList']
    body = body['Items']


    for i in range(len(body)):

        item =body[i]

        Timestamp=item['@Timestamp']
        #
        # Timestamp = '2020-1-1T10:1:1'


        location = item['@ItemName']#
        location = reg_location(location)
        if location=='TS1_W':  #这条目不做处理
            continue
        if 'TS1_' in location:
            if TS1_WQuality == 'bad': #bad data
                continue
            location = location+','+str(TS1_W_locat)

        Value = item['Value']
        # xsitype = Value['@xsi:type']
        value = Value['#text']#
        Quality=item['Quality']#



        QualityField=Quality['@QualityField']



        # create_dt =str(datetime.date.today())
        # create_dt_tm = datetime.datetime.today().strftime("%Y-%m-%d  %H:%M:%S")

        dt,tm =Timestamp.split('T')
        dt_tm=dt+" "+tm

        if QualityField != 'good':
            continue
        # if float(value) == 0:
        #     continue
        bodydict = {
            'value':float(value),
            'location':location,
            'dt_tm' :dt_tm,
            'dt':dt,
            'tm':tm,
            'create_dt':str(datetime.datetime.now().date())
            # 'device' :device,
        }
        if check_repeat_data(bodydict['location'],bodydict['dt_tm']):
            sql.insert_pc_particles_to_mysql(bodydict)
    # bodydict['len'] = bodylen
    # bodydict['alarm']= bodyalarmdict
    # bodydict['quality'] = bodyqualitydict
    # bodydict['value']= bodyvaluedict
    # bodydict['dttm'] = bodydttmdict
    # print(bodydict)


    # return bodydict

class particleopc(threading.Thread):
    def __init__(self,threadID,name,location):#location meaning whitch mq is chossed eg. PC_LPC
        threading.Thread.__init__(self)
        self.threadID =threadID
        self.name = name
        self.location = location
        self.url = readconfig.readcon(self.location,'url')
        self.headers = readconfig.readcon(self.location, 'headers')
        self.wsdl_xml = readconfig.readcon(self.location, 'wsdl_xml')
    def run(self):
        logdebug.logdeb("start thread:"+self.name)
        while True:
            try:
                self.unpack(self.location)
            except Exception as err:
                print('particleopc lpc   err :',err,self.name)
                time.sleep(60*5)
            finally:
                time.sleep(60)
    def unpack(self,device):

        res = wsdl(self.url,self.headers,self.wsdl_xml)
        if res == None:
            return res
        if (type(res)!= type('str')):
            res = json.dumps(res)

        unpackxml(res)
        # print(res)
        # print(res)

    # def callback(self,ch,method,properties,body):
    #     try:
    #         dictdata = json.loads(body)
    #     except Exception as er:
    #         logdebug.logdeb('recieve illegal arc2 data ')
    #         return
    #         # print(dictdata['location'])
    #     # if self.location == 'rabbitmq_LPC':
    #     dictdata['device'] = 2
    #     sql.insert_arc_to_mysql(dictdata)
        # sql.insert_lpc_to_mysql(dictdata)
            # print(dictdata)

        # print("thread name",self.getName())
    # def mq_init(self):
    #     username = readconfig.readcon(self.location,'username')
    #     pwd = readconfig.readcon(self.location,'pwd')
    #     host = readconfig.readcon(self.location,'host')
    #     virtual_host = readconfig.readcon(self.location,'virtual_host')
    #     queue = readconfig.readcon(self.location,'queue')
    #
    #     useer_pwd = pika.PlainCredentials(username,pwd)
    #
    #     s_conn = pika.BlockingConnection(pika.ConnectionParameters(virtual_host=virtual_host, host = host,credentials=useer_pwd))
    #
    #     chan = s_conn.channel()
    #
    #     # chan.queue_declare(queue=queue)
    #
    #
    #     chan.basic_consume(queue,self.callback,True)
    #     # chan.basic_consume(queue_mt,self.callback_mt,True)
    #     # chan.basic_consume(queue_particles,self.callback_particles,True)
    #
    #
    #     logdebug.logdeb("custmer wait for mes---->>>"+self.location)
    #     chan.start_consuming()

if __name__ == '__main__':
        # pc_particle = pc_particle_thread(1,'','pc_particle')
        # pc_particle.start()
        # url = readconfig.readcon('plasma3', 'url')
        # headers = readconfig.readcon('plasma3', 'headers')
        # wsdl_xml = readconfig.readcon('plasma3', 'wsdl_xml')

        res = reg_location('LMS/Inputs/Location 102/0.1/Aggregates/Cumulative Counts/Data')
        print(res)