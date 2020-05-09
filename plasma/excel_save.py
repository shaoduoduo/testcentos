#encoding:utf-8
import json
import datetime
import csv
from queue import Queue

global q
q = Queue()





save_dict = {'':0}
def check_repeat_data(location,timestamp):#检查重复数据，根据时间戳判断
    if location in save_dict:
        if save_dict[location] == timestamp:
            # print('数据重复，不发送',location,timestamp)
            return False

    save_dict[location] = timestamp
    print('第一次出现',location,timestamp)
    return True
#这个文件用来保存进exel
def write(paralist):

    # csvfile = open('data.csv','a',newline='')
    # content = csv.writer(csvfile,dialect='excel')
    # content.writerow(paralist)
    pass

def unpackalarm(json_str):
    # print("开始 解析 lpc数据")


    d = json.loads(json_str)
    body = d['soap:Envelope']

    body=body['soap:Body']
    body = body['ReadResponse']
    body = body['RItemList']
    body = body['Items']

    bodylen = len(body)
    bodyalarmdict= {}#保存报警项
    bodyqualitydict = {}  # 保存报警项
    bodyvaluedict = {}
    bodydttmdict = {}
    bodydict = {}

    for i in range(len(body)):

        item =body[i]

        Timestamp=item['@Timestamp']
        location = item['@ItemName']#



        Value = item['Value']
        xsitype = Value['@xsi:type']
        value = Value['#text']#
        Quality=item['Quality']#



        QualityField=Quality['@QualityField']



        # create_dt =str(datetime.date.today())
        # create_dt_tm = datetime.datetime.today().strftime("%Y-%m-%d  %H:%M:%S")

        dt,tm =Timestamp.split('T')
        dt_tm=dt+" "+tm

        bodyalarmdict[i] = location
        bodyqualitydict[i] = QualityField
        bodyvaluedict[i] = value
        bodydttmdict[i] = dt_tm


    bodydict['len'] = bodylen
    bodydict['alarm']= bodyalarmdict
    bodydict['quality'] = bodyqualitydict
    bodydict['value']= bodyvaluedict
    bodydict['dttm'] = bodydttmdict
    # print(bodydict)


    q.put(bodydict)

