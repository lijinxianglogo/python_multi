# # -*- encoding: utf-8 -*-
import math


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
        # 纬度每变化一度的实际距离,单位米
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
        print(l_and_l_dis - uwb_dis)
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
xx = UwbCoordToGps(p0, p1)
p0 = {'longitude': 107.010915, 'latitude': 41.057112, 'x': -16.13, 'y': -160.25}

p1 = {'longitude': 107.005207, 'latitude': 41.056227, 'x': -656.59, 'y': -156.94}
p2 = {'longitude': 107.01013, 'latitude': 41.060109, 'x': -9.92, 'y': 294.92}
xx = UwbCoordToGps(p0, p1)
# print xx.calc_uwb_to_lon_lat(65.23, 12.56)
# print xx.calc_uwb_to_lon_lat(198.96, 14.44)
# print xx.calc_lon_lat_to_uwb(p2['longitude'], p2['latitude'])
# print xx.calc_lon_lat_to_uwb(p3['longitude'], p3['latitude'])
#
#
#
#
#
#
#
# import struct
# # import pymysql
# # connection = pymysql.connect(host='localhost',
# #                              port=3306,
# #                              user='root',
# #                              password='eHIGH2014',
# #                              db='country_info',
# #                              charset='utf8',
# #                              use_unicode=True,
# #                              # binary_prefix=True,
# #                              cursorclass=pymysql.cursors.DictCursor)
#
# # with connection.cursor() as cursor:
# #     sql = "insert into test (pwd) values (%s)"
# #     for i in range(10):
# #         dd = struct.pack('<H10s', i, 'sss')
# #         args = (bytearray(dd))
# #         cursor.execute(sql, args)
# #     connection.commit()
#     # sql = "create table tb_house(pk_house_id int(4) not null, \
#     #                              house_name varchar(64) not null default '-', \
#     #                              house_zone int(11) not null)\
#     #        engine=innodb charset=utf8 partition by range(house_zone)(\
#     #            partition p0 values less than (20),\
#     #            partition p1 values less than (40),\
#     #            partition p2 values less than (60),\
#     #            partition p3 values less than maxvalue\
#     #        );"
#     # cursor.execute(sql)
#     # connection.commit()
#
# # import os, sys
# # import time
# # import signal
# # import ctypes
# # libc = ctypes.CDLL('libc.so.6')
# # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
# # 后台运行
#
# # def daemon():
# #     global num
# #     # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
# #     pid = os.fork()
# #     if pid:
# #         sys.exit(0)
# #     else:
# #         # # 子进程默认继承父进程的umask（文件权限掩码），重设为0（完全控制），以免影响程序读写文件
# #         os.umask(0)
# #         # # 让子进程成为新的会话组长和进程组长
# #         os.setsid()
# #         # # 刷新缓冲区先，小心使得万年船
# #         sys.stdout.flush()
# #         sys.stderr.flush()
# #         # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
# #         with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
# #             os.dup2(read_null.fileno(), sys.stdin.fileno())
# #             os.dup2(write_null.fileno(), sys.stdout.fileno())
# #             os.dup2(write_null.fileno(), sys.stderr.fileno())
#
#
#
#
#
#
#
#
#
#

print(ord('e'))

