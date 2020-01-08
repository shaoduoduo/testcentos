import pandas
import numpy
import time

#  2020年1月8日  读取文件，并返回字典

def read_qa_incomming(fdir):


        # df = pandas.read_excel(fdir,sheet_name='incomming',header=None)
    df = pandas.read_excel(fdir, header=None)

        # print(err)

    lines = 2# 38 71

    linedict = {}
    linedict['part_no'] = df.loc[lines].values[1]  #零件号
    linedict['sequence'] = df.loc[lines].values[5]  #序列号
    linedict['client'] = df.loc[lines].values[9]  #客户
    linedict['material'] = df.loc[lines].values[12]  #材质

    linedict['part_name'] = df.loc[lines+1].values[1]  #名称
    linedict['production_order'] = df.loc[lines+1].values[6]  #工单号
    date = df.loc[lines + 1].values[9]  # 入厂日期
    # datearr = time.localtime(date)
    # linedict['indate'] = time.strftime("%Y-%m-%d",date)  #
    linedict['indate'] = str(date)
    # print(linedict['indate'] )
    linedict['filepath'] = fdir
    linedict['value_50um'] = df[1].loc[lines + 16]  #value_50um
    linedict['value_200um'] =  df[2].loc[lines + 16]  #value_200um



    for x in linedict:
        if pandas.isna(linedict[x]):
            linedict[x] = 0
    return  linedict


