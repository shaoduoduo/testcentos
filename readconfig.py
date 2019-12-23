import configparser
import logdebug

def readcon(section,key):
    cf = configparser.ConfigParser()
    try:
        cf.read("config.ini")
        try:
            key = cf.get(section,key)
            return key
        except Exception as err:
            logdebug.logdeb(err)
            return None
    except  Exception as err:
        logdebug.logdeb(err)
        return None
