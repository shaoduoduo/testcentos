import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '3527058060@qq.com'
my_pass = 'brokujtptimpdbai'
# brokujtptimpdbai
# iowktlzbsksodace
# my_user = 'gyshao@insscn.com'
# my_user = '674181868@qq.com'
# my_context = 'your server programe is down'
my_title = 'from MES server'
my_chengname = 'server monitor'


def email(my_user,my_context):
    ret = 0
    try:
        msg = MIMEText(my_context, 'plain', 'utf-8')
        # msg['From'] = formataddr([my_chengname, my_sender])
        msg['From'] = my_sender
        # msg['To'] = formataddr(["ÊÕ¼þÈËêÇ³Æ", my_user])
        msg['To'] = my_user
        msg['Subject'] = my_title

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception as e:
        ret = e
    return ret

