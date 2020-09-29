import pandas
import pandas as pd
import numpy
import time
from datetime import datetime
#  2020年1月8日  读取文件，并返回字典
#'/mnt/share/qa/控制图数据库 - 副本.xlsx'
def read_qa_incomming(fdir):
        # df = pandas.read_excel(fdir,sheet_name='incomming',header=None)
    df = pandas.read_excel(fdir, None)
    print((df.keys()))

    res_list_roughness = []
    res_list_thickness = []
    if '粗糙度' in df.keys():
        # rough = df['粗糙度']
        df1 = pandas.read_excel(fdir, sheet_name='粗糙度')
        # res = df1.sample(2).values
        res = df1.values
        for i in res:
            data_dict = {
                'part_id': i[2],
                'data_value': i[3],
                # 'occur_dt':datetime.strftime(i[4],'%Y-%m-%d %H:%M:%S'),
                'occur_dt': datetime.strftime(i[4], '%Y-%m-%d'),
                'line': i[6]
            }

            # print(data_dict)
            res_list_roughness.append(data_dict)
    # if '厚度' in xl:

    if '厚度' in df.keys():
        # rough = df['粗糙度']
        df1 = pandas.read_excel(fdir, sheet_name='厚度')
        # res = df1.sample(2).values
        res = df1.values
        for i in res:
            data_dict = {
                'part_id': i[2],
                'data_value': i[3],
                # 'occur_dt':datetime.strftime(i[4],'%Y-%m-%d %H:%M:%S'),
                'occur_dt': datetime.strftime(i[4], '%Y-%m-%d'),
                'line': i[6]
            }
            res_list_thickness.append(data_dict)
            # print(data_dict)
        # print(type(res))
        # print(res_list_thickness)
    return {'roughness':res_list_roughness,'thickness':res_list_thickness}

if __name__ == '__main__':
    # '/mnt/share/qa/控制图数据库 - 副本.xlsx'
    read_qa_incomming('/mnt/share/qa/控制图数据库 - 副本.xlsx')