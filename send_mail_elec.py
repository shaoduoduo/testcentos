import  readconfig
import  sql
from f_email.sendemail import *
import logdebug
EMAILADDR = readconfig.readcon("fc_manual","emailaddr") #
def elec_mail():

    try :
        res = email(EMAILADDR,sql.select_elec_from_mysql())
    except Exception as  err:
        logdebug.logdeb(err)
        return
    print(EMAILADDR,"send ok",res)