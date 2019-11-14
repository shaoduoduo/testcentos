import mysql.connector
import logdebug
import readconfig
global mydb
global mycursor
def connect_to_mysql():
    global mydb
    global mycursor

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

def inser_to_mysql(paralist):
#     paralist must have 6 items

    global mydb
    global mycursor
    # print(len(paralist))

    sql = "INSERT INTO TB_ELEC_copy (location,dt,tm,value,dt_tm,create_dt) VALUES(%s,%s,%s,%s,%s,%s)"

    try:
        val = (paralist["location"],paralist["dt"],paralist["tm"],paralist["value"],paralist["dt_tm"],paralist["create_dt"])
    except Exception as err:
        logdebug.logdeb(err)
        return
    print(type(val))
    try:
        mycursor.execute(sql,val)
    except Exception as error:
        logdebug.logdeb(error)
        return

    mydb.commit()
    print("insert db ")