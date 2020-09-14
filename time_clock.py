#-*-coding:utf-8-*-
#
import datetime
def clock_loop(hour_in,min_in):
    current = datetime.datetime.now()
    # print(type(current.hour))
    if(current.hour==hour_in and current.minute==min_in):
        return True
    return False

if __name__ == '__main__':
    print(clock_loop(14,20))