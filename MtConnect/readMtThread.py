import threading
import queue
import time
import requests
import re
import bs4
from datetime import datetime,timedelta
import sql

language = {'servo': ''}



# 一共75项
def setlanguage():
#   Description
    language['avail'] = ''
    language['functionalmode']=''
    language['d1_asset_chg'] = '资源变更'
    language['d1_asset_rem'] = ''

#    Axes
    language['servo'] = ''
    language['spndl'] = ''

    language['xpm'] = 'X轴机械位置'
    language['xpw'] = 'X轴当前位置'
    language['xt'] = 'X轴行程'
    language['xl'] = 'X轴负载'
    language['xf']='X轴进给速度'
    language['xaxisstate'] = 'X轴状态'

    language['ypm'] = 'Y轴机械位置'
    language['ypw'] = 'Y轴当前位置'
    language['yt'] = 'Y轴行程'
    language['yl'] = 'Y轴负载'
    language['yf']='Y轴进给速度'
    language['yaxisstate'] = 'Y轴状态'

    language['zpm'] = 'Z轴机械位置'
    language['zpw'] = 'Z轴当前位置'
    language['zt'] = 'Z轴行程'
    language['zl'] = 'Z轴负载'
    language['zf']='Z轴进给速度'
    language['zaxisstate'] = 'Z轴状态'

    language['cl'] = 'C轴负载'
    language['sl']='S轴负载'
    language['ct'] = 'C轴角速度'
    language['cf'] = 'C轴进给速度'
    language['cs'] = 'C轴旋转速度'
    language['ctemp'] = 'C轴温度'
    language['cposm']='C轴绝对坐标'
    language['cposw'] = 'C轴坐标'
    language['rf'] = 'C轴旋转模式'

    language['spc'] = ''
    language['tmp'] = ''
    language['caxisstate']='C轴状态'
    #报警信息
    language['ccond'] = '运行状态信息'
    language['logic'] = '运行状态提醒'
    language['system'] = '运行状态信息'
#Controller
    language['estop'] = '急停开关状态'
    language['atime']='自动运转时间'
    language['yltime'] = '总时间'
    language['ctime'] = '加工时间'
    language['tcltime'] = '自动加工时间'
    language['pltnum'] = '托盘ID'
#   Path
    language['peditmode']=''
    language['peditname'] = ''
    language['hd1chuckstate'] = ''
    language['pfr'] = '设定快速进给'
    language['pfo'] = '设定保持进给'
    language['Sovr']='主轴设定转速'
    language['pgm'] = '程序号'
    language['spgm'] = '子程序号'
    language['ln'] = '线速度'
    language['unit'] = '单元号'
    language['seq']='顺序号'
    language['pc'] = '工件计数'
    language['pf'] = '实际保持进给'
    language['tid'] = '刀具号'
    language['tid2'] = '刀具组'
    language['tid3']='刀具后缀'
    language['exec'] = '运转状态'
    language['mode'] = '控制模式'
    language['pcmt'] = '程序备注'
    language['spcmt'] = '子程序备注'
    language['motion']='错误码'
    language['path_system'] = ''

#   Door
    language['door'] = '门状态'

#Systems
    language['electric'] = ''
    language['hydhealth'] = '液压'

    language['coolhealth'] = '冷却液'
    language['cooltemp']='冷却液温度'
    language['concentration'] = '冷却液浓度'


    language['pneucond'] = '气压'
    language['lube'] = '润滑'




class readMtThread(threading.Thread):
    def __init__(self,threadID,name,url,No):
        threading.Thread.__init__(self)
        self.ThreadID = threadID
        self.name = name
        self.url = url
        self.No = No
        self.cnt = 0
        self.dataitemidlist = ['servo', 'spndl', 'atime', 'ctime', 'tcltime', 'yltime', 'estop', 'pltnum', 'ccond', 'logic',
                          'system', 'concentration', 'cooltemp', 'coolhealth', 'avail', 'd1_asset_chg', 'd1_asset_rem',
                          'functionalmode', 'door', 'electric', 'hydhealth', 'lube', 'pf', 'Sovr', 'exec',
                          'hd1chuckstate', 'ln', 'mode', 'pc', 'pcmt', 'peditmode', 'peditname', 'pfo', 'pfr', 'pgm',
                          'seq', 'spcmt', 'spgm', 'tid', 'tid2', 'tid3', 'unit', 'motion', 'path_system', 'pneucond',
                          'xf', 'xl', 'xpm', 'xpw', 'xaxisstate', 'xt', 'yf', 'yl', 'ypm', 'ypw', 'yaxisstate', 'yt',
                          'zf', 'zl', 'zpm', 'zpw', 'zaxisstate', 'zt', 'cf', 'cl', 'cposm', 'cposw', 'cs', 'ctemp',
                          'sl', 'caxisstate', 'rf', 'ct', 'spc', 'tmp']
        self.save_dict = {'':0}
    def Mtconnect_init(self):

        pass
    def check_repeat_data(self,location,sequence):
        if location in self.save_dict:
            if self.save_dict[location] == sequence:
                return False
        self.save_dict[location]=sequence
        # print('first time happen ',location,sequence,self.name)
        return True

    def run(self):
        while True:
            try:
                self.getMtconnect()
                self.cnt +=1
                if self.cnt % 10 == 0:
                    # print(self.name,"getMtconnect -----> ", self.cnt)
                    pass
            except Exception as err:
                # print(err)
                # print(self.name,'--->关机状态，无法创建连接',datetime.now())
                time.sleep(60*10)
            finally:
                time.sleep(60)

    def getMtconnect(self):
        rec = requests.get(self.url)
        soup = bs4.BeautifulSoup(rec.text, "lxml")


        # creationtime = "2020-01-08T07:10:45Z"


        # 拿到当前时间
        ss = bs4.BeautifulSoup.find_all(soup, firstsequence="1")

        # Header creationTime = "2020-01-08T07:09:41Z"
        regexp = r'creationtime="(.*?)Z"'
        # timelist = re.findall(regexp, str(ss[0]))
        timelist = re.findall(regexp, str(soup.contents))
        timestamp = soup.contents[1].contents[0].contents[0].contents[1].attrs['creationtime']
        # print(timelist)
        stime = timestamp.replace("T", " ")
        stime = stime.replace("Z", "")
        # print('stime ->>',stime)
        # currenttime = stime
        currenttime = self.changTimeFormat(stime)
        # print(gloltime)
        # res=soup.prettify() #处理好缩进，结构化显示

        tag = soup.body  # 查找body标签内的所有内容
        # print(tag)
        # print(soup.position)
        # ss = bs4.BeautifulSoup.find_all(soup,name="axisstate")

        for i in range(len(self.dataitemidlist)):
            # print(i, dataitemidlist[i])
            ss = bs4.BeautifulSoup.find_all(soup, dataitemid=self.dataitemidlist[i])

            # for x in dataitemidlist:
            #     ss = bs4.BeautifulSoup.find_all(soup, dataitemid=x)
            # ss = bs4.BeautifulSoup.find_all(soup,dataitemid="yaxisstate")
            #

            regexp = r'timestamp="(.*?)Z"'
            timestr = re.findall(regexp, str(ss[0]))
            # print(timestr)

            regexp = r'(.*?)T(.*?)\.'
            stime = re.findall(regexp, str(timestr[0]))

            timestamp = ' '.join(stime[0])
            timestamp_8 = self.changTimeFormat(timestamp)
            dt = timestamp_8.split(' ')[0]
            tm = timestamp_8.split(' ')[1]

            #get sequeue
            regexp = r'sequence="(\d+)"'
            sequence = re.findall(regexp, str(ss[0]))
            if sequence.__len__()==0:
                continue
            sequence = int(sequence[0])

            regexp = r'nativecode="\d+"'
            nativeCode = re.findall(regexp, str(ss[0]))
            if nativeCode.__len__()==0:
                nativeCode = 0


            regexp = r'nativeseverity="\d+"'
            nativeSeverity = re.findall(regexp, str(ss[0]))
            if nativeSeverity.__len__()==0:
                nativeSeverity = 0


            # if nativeCode.__len__() != 0:


            dict = {}

            # dict['chinese'] = language[self.dataitemidlist[i]]  # 添加信息
            dict['itemid'] = self.dataitemidlist[i]  # 更新

            dict['value'] = (ss[0].string ) # 更新
            # if dict['value']==None:
            #     dict['value'] =0
            dict['machine_num'] = self.No #mazak1050
            dict['dt'] =dt
            dict['tm'] =tm
            dict['dt_tm']= timestamp_8
            # dict['create_dt_tm'] =currenttime
            dict['machine_dt_tm']=  currenttime

            dict['sequence']=sequence
            dict['nativeCode']=nativeCode
            dict['nativeSeverity']=nativeSeverity
            # print(dict)
            if self.check_repeat_data(dict['itemid'],dict['sequence']):
                sql.insert_Mtconnect_to_mysql(dict)

    def changTimeFormat(self,timeStr):

        try:
            res = datetime.strptime(timeStr,'%Y-%m-%d %H:%M:%S')+timedelta(hours=8)
            # res = datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S')
            # '2020-01-09 00:01:27'
            # res = timeStr+ timedelta(hours=8)
        except Exception as err:
            return None

        timestring = res.strftime('%Y-%m-%d %H:%M:%S')

        return timestring



