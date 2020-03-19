import  readconfig
import  sql
from f_email.sendemail import *

EMAILADDR = readconfig.readcon("fc_manual","emailaddr") #
def elec_mail():


    res = email(EMAILADDR,sql.select_elec_from_mysql())
    print(EMAILADDR,"send ok",res)