import pandas
import numpy
import sql


def read_pc_Titration(fdir):

    try:
        df = pandas.read_excel(fdir,sheet_name='IT MES',header=None)
    except Exception as e:
        print(e)
        return None
        # print(err)
    # data = df.loc[1].values
    # data=df.loc[0].values        #0表示第一行 这里读取数据并不包含表头，要注意哦！
    # print("读取指定行的数据：\n{0}".format(data))
    # print(df)
    #
    linelist = []
    for x in range(df.shape[0]):
        if pandas.isna(df.loc[x].values[0]):
            continue
        # if '-' in str(df.loc[x].values[0]):
        if  str(df.loc[x].values[0]).count('-')==3:
            linedict = {}
            linedict['location'] = df.loc[x].values[0]
            linedict['Chem1_result1'] = df.loc[x].values[7]
            linedict['Chem2_result1'] = df.loc[x].values[8]
            linedict['date1'] = df.loc[x].values[9]
            linedict['Chem1_result2'] = df.loc[x].values[10]
            linedict['Chem2_result2'] = df.loc[x].values[11]
            linedict['date2'] = df.loc[x].values[12]
            linelist.append(linedict)
    for x in  linelist:
        for i in x:
            if pandas.isna(x[i]):
                x[i] = 0
    return linelist
    #
    # for x in range(3,20):
    #     # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
    #     linedict = {}
    #     linedict['location'] = df.loc[x].values[0]
    #     linedict['Chem1_result1'] = df.loc[x].values[7]
    #     linedict['Chem2_result1'] = df.loc[x].values[8]
    #     linedict['date1'] = df.loc[x].values[9]
    #     linedict['Chem1_result2']    = df.loc[x].values[10]
    #     linedict['Chem2_result2'] = df.loc[x].values[11]
    #     linedict['date2'] = df.loc[x].values[12]
    #
    #     linelist.append(linedict)
    #     # linedata = df.loc[x].values
    #     # print(type(linedata))
    # for x in range(23,27):
    #     # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
    #     linedict = {}
    #     linedict['location'] = df.loc[x].values[0]
    #     linedict['Chem1_result1'] = df.loc[x].values[7]
    #     linedict['Chem2_result1'] = df.loc[x].values[8]
    #     linedict['date1'] = df.loc[x].values[9]
    #     linedict['Chem1_result2']    = df.loc[x].values[10]
    #     linedict['Chem2_result2'] = df.loc[x].values[11]
    #     linedict['date2'] = df.loc[x].values[12]
    #
    #     linelist.append(linedict)
    #
    # for x in range(29,45):
    #     # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
    #     linedict = {}
    #     linedict['location'] = df.loc[x].values[0]
    #     linedict['Chem1_result1'] = df.loc[x].values[7]
    #     linedict['Chem2_result1'] = df.loc[x].values[8]
    #     linedict['date1'] = df.loc[x].values[9]
    #     linedict['Chem1_result2']    = df.loc[x].values[10]
    #     linedict['Chem2_result2'] = df.loc[x].values[11]
    #     linedict['date2'] = df.loc[x].values[12]
    #
    #     linelist.append(linedict)
    # for x in range(48,52):
    #     # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
    #     linedict = {}
    #
    #     linedict['location'] = df.loc[x].values[0]
    #     linedict['Chem1_result1'] = df.loc[x].values[7]
    #     linedict['Chem2_result1'] = df.loc[x].values[8]
    #     linedict['date1'] = df.loc[x].values[9]
    #     linedict['Chem1_result2']    = df.loc[x].values[10]
    #     linedict['Chem2_result2'] = df.loc[x].values[11]
    #     linedict['date2'] = df.loc[x].values[12]
    #
    #     linelist.append(linedict)
    # # print(linelist)
    #
    # for x in  linelist:
    #     for i in x:
    #         if pandas.isna(x[i]):
    #             x[i] = 0
    # return linelist

def read_pc_manual_input(fdir):

    try:
        df = pandas.read_excel(fdir,header=None)
    except Exception as e:
        print(e)
        return None
        # print(err)
    # data = df.loc[1].values
    data = df.shape[0]
    # data=df.loc[1].values        #0表示第一行 这里读取数据并不包含表头，要注意哦！
    # print("读取指定行的数据：\n{0}".format(data))
    # print(df)
    #
    linelist = []
    for x in range(1,df.shape[0]):
        # if pandas.isna(df.loc[x].values[0]):
        #     continue
        # if '-' in str(df.loc[x].values[0]):
#读取到 22行：data10
        linedict = []
        for j in range(22):
            linedict.append(df.loc[x].values[j])
        linelist.append(linedict)

    for w in  linelist:
        for y in range(w.__len__()):
            if pandas.isna(w[y]):
                w[y] = 0
    # print(linelist)
    return linelist



if __name__  == "__main__":
    # sql.connect_to_mysql()
    res = read_pc_manual_input('/mnt/share/3.xlsx')
    for x in res:
        # sql.insert_pc_manual_to_mysql(x)
        print(x)
    print(res)
# try:
#     res = read_pc_Titration('/mnt/share/111.xlsx')
#     print(res[0])
#     if res[0]['location'] != 'NC-DEP1-HKOH-1':
#         print('not right file')
# except Exception as  e:
#     print(e)
#     print('not right file')


    # sql.insert_pc_to_mysql(res)

