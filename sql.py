# import mysql.connector
import mysql.connector
import logdebug
import datetime
import readconfig
import threading

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

    if( lcoationstr != '0.1um/LPC' )and (lcoationstr != '0.3um/LPC'):
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

