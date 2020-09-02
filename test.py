#-*-coding:utf-8-*-

import readconfig
import re
ss= 'LMS/Inputs/Location 112/1.0/Aggregates/Cumulative Counts/Data'
# wsdl_xml = readconfig.readcon('plasma3', 'wsdl_xml')
# res = re.search('[\d+]',ss)
rr = 'ion (.*)/Ag'
res = re.findall(rr,ss)
# print(res.group())
print(res)