import requests
import re
import readconfig
import json
import simplejson
import xmltodict
import ast
import main

def xmltojson(xmlstr):
    xmlparse = xmltodict.parse(xmlstr)
    jsonstr = simplejson.dumps(xmlparse)
    return jsonstr
#读取本地数据用于测试
def readjson():
    with open('js.json', 'a') as f:
        data = json.load(f)
    return data  # json 格式

def wsdl(url,headers,xmlstr):

    headers = ast.literal_eval(headers)#转为dict格式

    data = xmlstr

    try:
        rep = requests.post(url, data=data, headers=headers)
    except Exception as error:
        main.logdebug(error)
        return None
    rep = rep.text

    json_str = xmltojson(rep)
    return json_str


