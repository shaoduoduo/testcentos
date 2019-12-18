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
    logdebug.logdeb(mydb)
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
            logdebug.logdeb('insert opc  data',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        threadLock.release()

    # print("insert db ")

def insert_pc_to_mysql(paralist):#pc  input
#     paralist must have 6 items
    global threadLock
    global mydb
    global mycursor
    # print(len(paralist))

    sql = "INSERT INTO TB_PC_INPUT (location,dt_tm,value,create_dt_tm) VALUES(%s,%s,%s,CURRENT_TIMESTAMP())"

    try:
        val = (paralist["location"],paralist["dt_tm"],paralist["value"])
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


def insert_particles_to_mysql(paralist):#pc  input  every 60 times report once
#     paralist must have 6 items
    global threadLock
    global mycursor
    global part_count
    # print(len(paralist))
    if 'Q5' in paralist["location"][1]:
        part_count =part_count + 1
        if part_count %10 ==0:
            logdebug.logdeb("receive particles",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'value is --->',paralist["value"],'part_count is',part_count)

    if float(paralist["value"]) == 0:
        return

    sql = "INSERT INTO TB_PARTICLES (location,dt,tm,value,dt_tm,create_dt) VALUES(%s,%s,%s,%s,%s,%s)"

    locatlist = paralist["location"]
    list = locatlist[1:]
    list_new = [str(item) for item in list]

    lcoationstr = ','.join(str(item) for item in list)

    pass
    try:

        val = (lcoationstr,paralist["dt"],paralist["tm"],float(paralist["value"]),paralist["dt_tm"],paralist["create_dt"])
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
