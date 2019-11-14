import xlrd
import logdebug
import sql
class readexcel():
    def __init__(self,path):
        self.path =path

    def init(self):
        try:
            self.workbook = xlrd.open_workbook(self.path)
        except Exception as err:
            logdebug.logdeb(err)
            return
        try:
            self.worksheet = self.workbook.sheet_by_index(0)
        except Exception as err:
            logdebug.logdeb(err)
            return
        self.nrows = self.worksheet.nrows
        # print("row is ",self.nrows)
        self.ncols = self.worksheet.ncols
        # print("col is ",self.ncols)

        for i in range(6,self.nrows-4):

            dt_tm = xlrd.xldate.xldate_as_datetime(self.worksheet.row_values(i)[0],0).__str__()
            # print(dt_tm)
            value = self.worksheet.row_values(i)[4]
            # print(type(value))
            # print("arc is ",value)
            location = "0.1um"
            paralist = {'location':location,'dt_tm':dt_tm,'value':-1.13245}
            # print(val)
            sql.insert_pc_to_mysql(paralist)


