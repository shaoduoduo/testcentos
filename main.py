import sql
import mq_c

def main():
    sql.connect_to_mysql()
    mq_c.mq_init()
    print ("end")


if __name__ == '__main__':
    main()