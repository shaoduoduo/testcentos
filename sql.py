# import mysql.connector
import mysql.connector
import logdebug
import datetime
import readconfig
import threading
import time
global mydb
global mycursor
global threadLock
part_count = 0


def connect_to_mysql():
    global mydb
    global mycursor
    global threadLock
    threadLock = threading.Lock()

    host = readconfig.readcon('mysql','host')
    user = readconfig.readcon('mysql','user')
    passwd = readconfig.readcon('mysql','passwd')
    database = readconfig.readcon('mysql','database')

    try:
        mydb = mysql.connector.connect(host=host,user=user,passwd=passwd,database=database)
    except Exception as error:
        logdebug.logdeb(error)
        return False
    # logdebug.logdeb(mydb)
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        print(x)

def insert_to_mysql(paralist):  #rabbitmq  opc data
#     paralist must have 6 items
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))
    if float(paralist["value"])==0:
        return

    sql = "INSERT INTO TB_ELEC (location,dt,tm,value,dt_tm,create_dt) VALUES(%s,%s,%s,%s,%s,%s)"

    try:
        val = (paralist["location"],paralist["dt"],paralist["tm"],float(paralist["value"]),paralist["dt_tm"],paralist["create_dt"])
    except Exception as err:
        logdebug.logdeb(err)

        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
        # mycursor.execute("CALL sp_tb_elec_update_inc_val()")#
    except Exception as error:
        logdebug.logdeb(error)
        print(float(paralist["value"]))
    finally:
        threadLock.release()

    # print('insert successfully')
    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        if(paralist["location"] == 'PW400030'):
            str = 'insert opc  data'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logdebug.logdeb(str)
        threadLock.release()



    # print("insert db ")

def insert_pc_manual_to_mysql(paralist):#pc  input


#general data collect from pc input 2020/4/15
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))"sp_tb_elec_update_inc_val()"

    # print(paralist["index"],paralist["time"],paralist["date"],paralist["add1"],paralist["add2"],paralist["add3"],paralist["add4"],paralist["data0"],paralist["data1"],paralist["data2"],
    #            paralist["data3"],paralist["data4"],paralist["data5"],paralist["data6"],paralist["data7"],paralist["data8"],paralist["data9"],paralist["data10"])
    # return
    sql = "INSERT INTO TB_PC_INPUT_MANUAL (`index`,`time`,`date`,add1,add2,add3,add4,data0,data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,create_dt_tm)" \
          " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"

    try:
        val = (paralist["index"],paralist["time"],paralist["date"],paralist["add1"],paralist["add2"],paralist["add3"],paralist["add4"],paralist["data0"],paralist["data1"],paralist["data2"],
               paralist["data3"],paralist["data4"],paralist["data5"],paralist["data6"],paralist["data7"],paralist["data8"],paralist["data9"],paralist["data10"])


    # sql = "INSERT INTO TB_PC_INPUT_MANUAL (`index`,`time`,`date`,create_dt_tm)  VALUES(%s,%s,%s,CURRENT_TIMESTAMP())"
    #
    # try:
    #     val = (2,'7:50:00','2020/1/12')

    except Exception as err:
        logdebug.logdeb(err)
        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()



def insert_pc_to_mysql(paralist):#pc  input
#     paralist must have 6 items
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))"sp_tb_elec_update_inc_val()"


    if  paralist['date1'] ==0 or paralist['date2']==0:
        return


    sql = "INSERT INTO TB_PC_INPUT (location,chemical1_result1,chemical2_result1,date1," \
          "chemical1_result2,chemical2_result2,date2,create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"

    try:
        val = (paralist["location"],paralist["Chem1_result1"],paralist["Chem2_result1"],paralist["date1"],
               paralist["Chem1_result2"],paralist["Chem2_result2"],paralist["date2"])
    except Exception as err:
        logdebug.logdeb(err)
        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()

def insert_Mtconnect_to_mysql(paralist):  #mtconnect
# {'itemid': 'tmp', 'timestamp': '2019-12-13 16:11:10', 'value': None, 'machine_num': 0,'currenttime': '2019-12-23 14:13:12'}
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))
    if (paralist["value"])==None:
        return

    sql = "INSERT INTO TB_PM_MACHINE (location,dt,tm,value,dt_tm,machine,machine_dt_tm,create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"

    try:
        val = (paralist["itemid"],paralist["dt"],paralist["tm"],str(paralist["value"]),\
               paralist["dt_tm"],paralist["machine_num"],paralist["machine_dt_tm"])
    except Exception as err:
        logdebug.logdeb(err)

        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
        # mycursor.execute("CALL sp_tb_elec_update_inc_val()")#
    except Exception as error:
        logdebug.logdeb(error)
        print((paralist["value"]))
    finally:
        threadLock.release()

    # print('insert successfully')
    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:

        threadLock.release()



    # print("insert db ")

def insert_particles_to_mysql(paralist):#pc  input  every 60 times report once
#     paralist must have 6 items
    global threadLock
    global mycursor
    global part_count
    # print(len(paralist))
    if 'Q5' in paralist["location"][1]:
        part_count =part_count + 1
        if part_count %10 ==0:
            print("receive particles",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'value is --->',str(paralist["value"]),part_count)

    if float(paralist["value"]) == 0:
        return

    sql = "INSERT INTO TB_PARTICLES (location,dt,tm,value,dt_tm,create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s)"

    locatlist = paralist["location"]
    list = locatlist[1:]
    list_new = [str(item) for item in list]

    lcoationstr = ','.join(str(item) for item in list)

    pass
    try:

        val = (lcoationstr,paralist["dt"],paralist["tm"],float(paralist["value"]),paralist["dt_tm"],paralist["create_dt_tm"])
    except Exception as err:
        logdebug.logdeb(err)
        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()
        if(paralist["location"] == 'TS2_2'):
            print('insert PARTICLES',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def insert_lpc_to_mysql(paralist):#pc  input  every 60 times report once
#     paralist must have 6 items
    global threadLock
    global mycursor
    global part_count
    # print(len(paralist))

    if float(paralist["value"]) == 0:
        return

    sql = "INSERT INTO TB_PARTICLES (location,dt,tm,value,dt_tm,create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s)"

    lcoationstr= paralist["location"]

    if ( '7017C' in  lcoationstr )and ('0.3um' in lcoationstr):
        lcoationstr= paralist["location"] = '0.3um/LPC'
    elif ( '7017C' in  lcoationstr )and ('0.1um' in lcoationstr):
        lcoationstr = paralist["location"] = '0.1um/LPC'
    else:
        return
    # lcoation='lpc/0.'+lcoationstr
    try:

        val = (lcoationstr,paralist["dt"],paralist["tm"],float(paralist["value"]),paralist["dt_tm"],paralist["create_dt_tm"])
    except Exception as err:
        logdebug.logdeb(err)
        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()
        if(paralist["location"] == 'TS2_2'):
            print('insert PARTICLES',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def insert_qa_to_mysql(paralist):#pc  input
#     paralist must have 6 items
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))"sp_tb_elec_update_inc_val()"



    sql = "INSERT INTO TB_QA_INCOMMING (part_no,sequence,client,material,part_name,production_order,indate," \
          "filepath,value_50um,value_200um,create_dt_tm) " \
          "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"

    try:
        val = (paralist["part_no"],paralist["sequence"],paralist["client"],paralist["material"],paralist["part_name"],paralist["production_order"],
               paralist["indate"],paralist["filepath"],paralist["value_50um"],paralist["value_200um"])
    except Exception as err:
        logdebug.logdeb(err)
        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


def select_elec_from_mysql():
    #     paralist must have 6 items
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))"sp_tb_elec_update_inc_val()"

    sql = "SELECT DISTINCT	location,dt_tm,value  FROM  TB_ELEC	WHERE location REGEXP '[1-9][YW]G$' AND  HOUR(tm) =8 AND dt = CURRENT_DATE() AND MINUTE (tm) > 30 ORDER BY  location DESC;"
    #sql = "SELECT 	*  FROM  TB_ELEC	WHERE  dt = CURRENT_DATE();"

    # mycursor.execute(sql)


    # print(type(val))

    try:
        threadLock.acquire()
        mycursor.execute(sql)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()

    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()

    myresult = mycursor.fetchall()
    returnstr = ""

    for x in myresult:
        # returnstr =returnstr +''.join(list(x))

        # print((x))
        x1= x[0]
        y1 = x[1]
        # y = time.strftime("%Y-%m-%d %H:%M:%S",x[1])

        z1 = x[2]
        returnstr = returnstr+x1+","+str(y1)+","+str(z1)+"\n"
        # print(type(x1),type(y1),type(z1))
    return  (returnstr)

def insert_arc_to_mysql(paralist):#pc  input  every 60 times report once
#     paralist must have 6 items
    global threadLock
    global mycursor
    global part_count
    # print(len(paralist))


    sql = "INSERT INTO TB_ST_ARC (device,data_date,data_time,data0,data1,data2,data3,data4,data5,create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"

    # print(paralist["1"])
    # lcoation='lpc/0.'+lcoationstr
    try:
        val = (paralist["device"],paralist["date"],paralist["time"],paralist["0"],paralist["1"],float(paralist["2"]),paralist["3"],paralist["4"],paralist["5"])
    except Exception as err:
        logdebug.logdeb(err)
        return
    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()

def insert_anodize_to_mysql(paralist):#pc  input  every 60 times report once
#     paralist must have 6 items
    global threadLock
    global mycursor
    global part_count
    # print(len(paralist))
    # anodize_index = 0
    if 'PRO_INDEX_ANODIZE' in paralist:
        anodize_index = paralist["PRO_INDEX_ANODIZE"]
        if anodize_index < 0 and anodize_index > 6:
            logdebug.logdeb('recieve wrong anodize -->>', anodize_index, paralist)
            return
    else:
        logdebug.logdeb('recieve wrong anodize -->>', paralist)
        return

    if anodize_index == 0:#alarm
        sql = "INSERT INTO TB_ST_ANODIZE (data_index,data_date,data_time,add1,add2, create_dt_tm) VALUES(%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"
        try:
            val = (
            anodize_index, paralist["data"]["date"], paralist["data"]["time"], paralist["data"]["status"], paralist["data"]["msg"])
        except Exception as err:
            logdebug.logdeb(err)
            return

# cpv vpv csv vsv
    elif anodize_index == 1 or anodize_index == 2 or anodize_index == 3:
        sql = "INSERT INTO TB_ST_ANODIZE (data_index,data_date,data_time,value0,value1,value2,value3, create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"
        try:
            val = (
            anodize_index, paralist["data"]["date"], paralist["data"]["time"], float(paralist["data"]["cpv"]), float(paralist["data"]["vpv"]), float(paralist["data"]["csv"]), float(paralist["data"]["vsv"]))
        except Exception as err:
            logdebug.logdeb(err)
            return

    elif anodize_index == 4 or anodize_index == 5 :
        sql = "INSERT INTO TB_ST_ANODIZE (data_index,data_date,data_time,add1,add2,add3,add4, create_dt_tm) VALUES(%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"
        try:
            val = (
            anodize_index, paralist["data"]["date"], paralist["data"]["time"], (paralist["data"]["num"]), (paralist["data"]["code"]), (paralist["data"]["position"]), (paralist["data"]["action"]))
        except Exception as err:
            logdebug.logdeb(err)
            return
    elif anodize_index == 6:
        sql = "INSERT INTO TB_ST_ANODIZE (data_index,data_date,data_time,value0,value1,value2,value3,value4,value5,value6,value7,value8,value9,value10,value11,value12,value13,value14, create_dt_tm) " \
              "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())"
        try:
            val = (
            anodize_index, paralist["data"]["date"], paralist["data"]["time"],float(paralist["data"]["A1"]),float(paralist["data"]["A3"]),float(paralist["data"]["A5"]),float(paralist["data"]["A7"]),
            float(paralist["data"]["A9"]),float(paralist["data"]["A11"]),float(paralist["data"]["A13"]),float(paralist["data"]["D1"]),float(paralist["data"]["D3"]),float(paralist["data"]["A16"]),
            float(paralist["data"]["A18"]),float(paralist["data"]["A20"]),float(paralist["data"]["S1"]),float(paralist["data"]["S2"]),float(paralist["data"]["S3"]))
        except Exception as err:
            logdebug.logdeb(err)
            return
    else:
        return

    # print(type(val))
    try:
        threadLock.acquire()
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()


    try:
        threadLock.acquire()
        mydb.commit()
    except Exception as error:
        logdebug.logdeb(error)
    finally:
        threadLock.release()
