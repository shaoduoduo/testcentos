import mysql.connector

global mydb
global mycursor
def connect_to_mysql():
    global mydb
    global mycursor
    try:
        mydb = mysql.connector.connect(host="localhost",user="user_server",passwd="P@ssw0rd",database="inss_mes")
    except Exception as error:
        print(error)
        return False
    print(mydb)
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
        print(err)
        return

    try:
        mycursor.execute(sql,val)
    except Exception as error:
        print(error)
        return

    mydb.commit()
    print("insert db ")