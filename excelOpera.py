# _*_ coding:utf-8 _*_
import xlwt
import xlrd
import os
import math
import traceback


class ExcelOpera(object):
    # 参数:dir_path：文件夹路径,file_name：EXCEL文件名,sheet_index:EXCEL的表的索引
    def __init__(self, dir_path, file_name, sheet_index=0, sheet_name="sheet2"):
        self.sheet_index = sheet_index
        self.path = dir_path + file_name
        self.sheet_name = sheet_name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(self.path):
            book = xlwt.Workbook(encoding='utf-8')
            book.add_sheet(self.sheet_name, True)
            book.save(self.path)

    @staticmethod
    def __open_excel(file_name):
        try:
            data = xlrd.open_workbook(file_name)
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
            old_datas = self.excel_table_read()
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


class UwbCoordToGps(object):
    def __init__(self, point_0, point_1):
        """
        创建自定义直角坐标系temp_x_y，该直角坐标系以
        平行x=point_0[latitude]为y轴，以平行y=point_0[longitude]为x轴，以x=point_0[latitude]和y=point_0[longitude]的交点为原点
        :param point_0:{longitude: float(经度),
                        latitude: float(纬度),
                        x: float(x坐标),
                        y: float(y坐标)}
        :param point_1:{longitude: float(经度),
                        latitude: float(纬度),
                        x: float(x坐标),
                        y: float(y坐标)}
        """
        # 纬度每变化一度的实际距离,单位米0
        self.latitude_per = 110880
        # 经度每变化一度的实际距离,单位米
        self.longitude_per = 110880 * math.cos(point_0['latitude'] * math.pi / 180)
        # 微调直角坐标系的坐标
        self.__x_y_fine_adjust(point_0, point_1)
        # 定义原点
        self.ori_longitude = point_0['longitude']
        self.ori_latitude = point_0['latitude']
        self.point_0 = point_0
        # 得到point_1在temp_x_y下的坐标
        tp_1 = self.__lon_lat_to_x_y(point_1['longitude'], point_1['latitude'])
        # 得到得到temp_x_y原点坐标在uwb坐标系下的坐标形成偏移向量
        point_1_len = (point_1['x'] - self.point_0['x']) ** 2 + (point_1['y'] - self.point_0['y']) ** 2
        self.coso = ((point_1['x'] - self.point_0['x']) * tp_1['x'] +
                     (point_1['y'] - self.point_0['y']) * tp_1['y']) / point_1_len
        self.sino = ((point_1['y'] - self.point_0['y']) * tp_1['x'] -
                     (point_1['x'] - self.point_0['x']) * tp_1['y']) / point_1_len

    def __x_y_fine_adjust(self, point_0, point_1):
        """
        对传入的点的坐标进行微调
        :return:
        """
        # 经纬度距离
        l_and_l_dis = math.sqrt(((point_1['longitude'] - point_0['longitude']) * self.longitude_per) ** 2 +
                                ((point_1['latitude'] - point_0['latitude']) * self.latitude_per) ** 2)
        # UWB距离
        uwb_dis = math.sqrt((point_1['x'] - point_0['x']) ** 2 + (point_1['y'] - point_0['y']) ** 2)
        # 两个点同时进行微调
        print l_and_l_dis - uwb_dis
        adjust_value = (l_and_l_dis - uwb_dis) / 2.0
        if point_1['x'] == point_0['x']:
            # 对y坐标微调
            if point_1['y'] <= point_0['y']:
                point_1['y'] -= adjust_value
                point_0['y'] += adjust_value
            else:
                point_1['y'] += adjust_value
                point_0['y'] -= adjust_value
        elif point_1['y'] == point_0['y']:
            # 对x坐标微调
            if point_1['x'] <= point_0['x']:
                point_1['x'] -= adjust_value
                point_0['x'] += adjust_value
            else:
                point_1['x'] += adjust_value
                point_0['x'] -= adjust_value
        else:
            # 斜率微调
            dx = adjust_value * abs(point_1['x'] - point_0['x']) / uwb_dis
            dy = adjust_value * abs(point_1['y'] - point_0['y']) / uwb_dis
            if point_1['x'] > point_0['x']:
                # 斜率大于0
                if point_1['y'] > point_0['y']:
                    point_0['x'] -= dx
                    point_1['x'] += dx
                    point_0['y'] -= dy
                    point_1['y'] += dy
                else:
                    # 斜率小于0
                    point_0['x'] -= dx
                    point_1['x'] += dx
                    point_0['y'] += dy
                    point_1['y'] -= dy
            else:
                # 斜率小于0
                if point_1['y'] > point_0['y']:
                    point_0['x'] += dx
                    point_1['x'] -= dx
                    point_0['y'] -= dy
                    point_1['y'] += dy
                else:
                    # 斜率大于0
                    point_0['x'] += dx
                    point_1['x'] -= dx
                    point_0['y'] += dy
                    point_1['y'] -= dy
                    # UWB距离
        return True

    def __lon_lat_to_x_y(self, longitude, latitude):
        """
        将经纬度坐标转换为自定义直角坐标系temp_x_y下的坐标
        :param longitude: 经度
        :param latitude: 纬度
        :return:
        """
        result = dict()
        result['x'] = (longitude - self.ori_longitude) * self.longitude_per
        result['y'] = (latitude - self.ori_latitude) * self.latitude_per
        return result

    def __x_y_to_lon_lat(self, x, y):
        """
        将自定义直角坐标系temp_x_y下的坐标转换为经纬度坐标
        :param x:自定义直角坐标系temp_x_y下的x坐标
        :param y:自定义直角坐标系temp_x_y下的y坐标
        :return:
        """
        result = dict()
        result['latitude'] = y / self.latitude_per + self.ori_latitude
        result['longitude'] = x / self.longitude_per + self.ori_longitude
        return result

    def calc_uwb_to_lon_lat(self, x, y):
        """
        得到uwb坐标的经纬度
        :param x: float(uwb的x坐标)
        :param y:float(uwb的y坐标)
        :return:{longitude: float(经度坐标)
                 latitude： float(纬度坐标)}
        """
        tp_x = self.coso * (x - self.point_0['x']) + self.sino * (y - self.point_0['y'])
        tp_y = self.coso * (y - self.point_0['y']) - self.sino * (x - self.point_0['x'])
        return self.__x_y_to_lon_lat(tp_x, tp_y)

    def calc_lon_lat_to_uwb(self, lon, lat):
        """
        计算经纬度的uwb坐标
        :param lon:经度
        :param lat:纬度
        :return:字典
        """
        tp_x_y = self.__lon_lat_to_x_y(lon, lat)
        result = dict()
        result['x'] = self.coso*tp_x_y['x'] - self.sino*tp_x_y['y'] + self.point_0['x']
        result['y'] = self.sino*tp_x_y['x'] + self.coso*tp_x_y['y'] + self.point_0['y']
        return result


p0 = {'longitude': 104.135872972222, 'latitude': 30.3178330555556, 'x': 0, 'y': 0}
p1 = {'longitude': 104.1357671864, 'latitude': 30.3177029120, 'x': -17.715, 'y': -0.056}
coord_change = UwbCoordToGps(p0, p1)
excel_op = ExcelOpera('./', 'test_result.xlsx')
excel_data = excel_op.excel_table_read()
result = {'pos_x': [], 'pos_y': []}
for index in range(len(excel_data['GpsLongitude'])):
    uwb_data = coord_change.calc_lon_lat_to_uwb(excel_data['GpsLongitude'][index], excel_data['GpsLatitude'][index])
    result['pos_x'].append(uwb_data['x'])
    result['pos_y'].append(uwb_data['y'])
print result
# excel_op.excel_table_write(result)