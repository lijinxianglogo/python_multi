# _*_ coding:utf-8 _*_
import xlwt #写入数据
import xlrd #读取数据
import os
import traceback
class excel_opera(object):
    #参数:dir_path：文件夹路径,file_name：EXCEL文件名,sheet_index:EXCEL的表的索引
    def __init__(self, dir_path, file_name, sheet_index=0, sheet_name="sheet1"):
        self.sheet_index = sheet_index
        self.path = dir_path + file_name
        self.sheet_name = sheet_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(self.path):
            book = xlwt.Workbook(encoding='utf-8')
            book.add_sheet(self.sheet_name, True)
            book.save(self.path)

    def __open_excel(self, file):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception, e:
            print (traceback.format_exc())
            print (e)
            return False

    # 根据索引获取Excel表格中的数据   colnameindex：表头列名所在行的索引
    def excel_table_read(self, colnameindex=0):
        try:
            result = {}
            data = self.__open_excel(self.path)
            if data is not False:
                table = data.sheets()[self.sheet_index]
                nrows = table.nrows  # 行数
                if nrows:
                    colnames = table.row_values(colnameindex)  # 某一行数据
                    for colname in colnames:
                        result[colname] = []
                    for index in range(1, nrows):
                        row_datas = table.row_values(index)
                        if row_datas:
                            for i in range(len(row_datas)):
                                result[colnames[i]].append(row_datas[i])
            return result
        except Exception, e:
            print (traceback.format_exc())
            print (e)
            return False

    def excel_table_write(self, data):
        try:
            # 得到当前excel中的数据
            old_datas = self.excel_table_byindex()
            # 根据数据类型往里面添加数据
            data_keys = data.keys()
            for data_key in data_keys:
                if data_key in old_datas:
                    old_datas[data_key] += data[data_key]
                else:
                    old_datas[data_key] = data[data_key]
            # excel op
            file_op = xlwt.Workbook()
            sheet = file_op.add_sheet(self.sheet_name, True)
            data_keys = old_datas.keys()
            for index in range(len(data_keys)):
                sheet.write(0, index, data_keys[index])
                v = old_datas[data_keys[index]]
                for i in range(len(v)):
                    sheet.write(i + 1, index, v[i])
            file_op.save(self.path)
            return True
        except Exception, e:
            print (traceback.format_exc())
            print (e)
            return False

# test = excel_opera("/home/ehigh/ljx/test/", "test.xls")
# print test.excel_table_byindex()
# test.excel_table_write({"1253":[123,12],"tt":[883]})