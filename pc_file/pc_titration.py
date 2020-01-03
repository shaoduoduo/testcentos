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

    linelist = []
    for x in range(3,19):
        # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
        linedict = {}
        linedict['location'] = df.loc[x].values[0]
        linedict['Chem1_result1'] = df.loc[x].values[7]
        linedict['Chem2_result1'] = df.loc[x].values[8]
        linedict['date1'] = df.loc[x].values[9]
        linedict['Chem1_result2']    = df.loc[x].values[10]
        linedict['Chem2_result2'] = df.loc[x].values[11]
        linedict['date2'] = df.loc[x].values[12]

        linelist.append(linedict)
        # linedata = df.loc[x].values
        # print(type(linedata))
    for x in range(22,26):
        # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
        linedict = {}
        linedict['location'] = df.loc[x].values[0]
        linedict['Chem1_result1'] = df.loc[x].values[7]
        linedict['Chem2_result1'] = df.loc[x].values[8]
        linedict['date1'] = df.loc[x].values[9]
        linedict['Chem1_result2']    = df.loc[x].values[10]
        linedict['Chem2_result2'] = df.loc[x].values[11]
        linedict['date2'] = df.loc[x].values[12]

        linelist.append(linedict)

    for x in range(29,45):
        # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
        linedict = {}
        linedict['location'] = df.loc[x].values[0]
        linedict['Chem1_result1'] = df.loc[x].values[7]
        linedict['Chem2_result1'] = df.loc[x].values[8]
        linedict['date1'] = df.loc[x].values[9]
        linedict['Chem1_result2']    = df.loc[x].values[10]
        linedict['Chem2_result2'] = df.loc[x].values[11]
        linedict['date2'] = df.loc[x].values[12]

        linelist.append(linedict)
    for x in range(48,52):
        # linedata = df.ix[x,['location','ch1_LCL','ch1_UCL','ch2_LCL','ch2_UCL','ch1_name','ch2_name','ch1_result1','ch2_result1','ch1_result2','ch2_result1','date']].to_dict()
        linedict = {}

        linedict['location'] = df.loc[x].values[0]
        linedict['Chem1_result1'] = df.loc[x].values[7]
        linedict['Chem2_result1'] = df.loc[x].values[8]
        linedict['date1'] = df.loc[x].values[9]
        linedict['Chem1_result2']    = df.loc[x].values[10]
        linedict['Chem2_result2'] = df.loc[x].values[11]
        linedict['date2'] = df.loc[x].values[12]

        linelist.append(linedict)
    # print(linelist)

    for x in  linelist:
        for i in x:
            # print(x[i])

            # if numpy.isnan(a):
            #     print('is nan')
            # numpy.isnan()
            if pandas.isna(x[i]):
                x[i] = 0


    return linelist

def deal_pc_Titration():
    pass

# res = read_pc_Titration('/mnt/share/Titration MES_12_30.xlsx')

# try:
#     res = read_pc_Titration('/mnt/share/111.xlsx')
#     print(res[0])
#     if res[0]['location'] != 'NC-DEP1-HKOH-1':
#         print('not right file')
# except Exception as  e:
#     print(e)
#     print('not right file')


    # sql.insert_pc_to_mysql(res)

