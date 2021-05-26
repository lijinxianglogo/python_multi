# _*_ coding:utf-8 _*_
import pymysql
import traceback
import datetime
import time
import os
from CSLog import CSLog
CSLogger = CSLog("CSSQL", "./Log/CSSQL.log").getlogger()
db_config_default = {
    'user': 'root',
    'password': 'eHIGH2014',
    'host': '192.168.4.44',
    'port': 3306,
    'database': 'lct_net_manager',
    'charset': 'utf8',
    'use_unicode': True,
    'throw_alarm': True
}


class CSSQL(object):
    __instance = None
    @classmethod
    def getInstance(cls, db_config):
        if cls.__instance is None:
            cls.__instance = CSSQL(db_config)
        return cls.__instance

    def __init__(self, db_config):
        #检查参数
        try:
            self.host = db_config['host']
            self.user = db_config['user']
            self.password = db_config['password']
            self.database = db_config['database']
            self.port = db_config['port']
            self.charset = db_config['charset']
            self.use_unicode = db_config["use_unicode"]
            self.connection = None
            self.connectSQL()
        except Exception, e:
            CSLogger.error(e)
            CSLogger.error(traceback.format_exc())
            raise e

    def reconnectSQL(self):
        #所有的数据库操作都需要连接判断
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
            #连接数据库
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset,
                use_unicode=self.use_unicode,
                cursorclass=pymysql.cursors.DictCursor
            )
            return True
        except Exception, e:
            CSLogger.error(e)
            CSLogger.error(traceback.format_exc())
            return False

    def connectSQL(self, stime=5):
        while True:
            if self.reconnectSQL():
                return True
            else:
                time.sleep(stime)

    def executecSQL(self, sql, data_param=None, commit=True, recursor = False):
        try:
            # 判定是否连接被重置
            if self.connection is None:
                self.connectSQL()
            # 执行sql语句
            cursor = self.connection.cursor()
            #对于某些操作会有参数形式
            if data_param:
                result = cursor.execute(sql, data_param)
            else:
                result = cursor.execute(sql)
            #是否commit
            if commit:
                self.connection.commit()
            #对于增加数据而言返回主键ID
            if recursor:
                return cursor
            else:
                return result
        except Exception, e:
            CSLogger.error(e)
            CSLogger.error(traceback.format_exc())
            #对于某些错误进行重连，其余错误抛出，不重连
            if e[0] in [2000, 2003, 2006, 2013, 2014, 2015]:
                #重连
                self.connectSQL()
                # 执行sql语句
                cursor = self.connection.cursor()
                # 对于某些操作会有参数形式
                if data_param:
                    result = cursor.execute(sql % data_param)
                else:
                    result = cursor.execute(sql)
                # 是否commit
                if commit:
                    self.connection.commit()
                # 对于增加数据而言返回主键ID
                if recursor:
                    return cursor
                else:
                    return result
            else:
                raise e

    def insert(self, table, data, commit=True):
        sql = "INSERT INTO {table} SET {param}".format(table=table, param=self.join_field_value(data))
        cursor = self.executecSQL(sql=sql, data_param=tuple(data.values()), commit=commit, recursor=True)
        if cursor:
            return cursor.lastrowid
        else:
            return None

    def delete(self, table, condition=None, limit=None, order=None, desc=False, commit=True):
        # type: (object, object, object, object, object, object) -> object
        """

        :rtype: 
        """
        condition = self.condition(condition)
        limits = "LIMIT {limit}".format(limit=limit) if limit else ""
        if desc:
            orders = "ORDER by {order} DESC".format(order=order) if order else ""
        else:
            orders = "ORDER by {order}".format(order=order) if order else ""
        sql = "DELETE FROM {table} WHERE {condition} {orders} {limits}".format(table=table, condition=condition,
                                                                                   orders=orders, limits=limits)
        return self.executecSQL(sql=sql, commit=commit)

    def update(self, table, data, condition=None, limit=None, order=None, desc=False, commit=True):
        condition = self.condition(condition)
        limits = "LIMIT {limit}".format(limit=limit) if limit else ""
        if desc:
            orders = "ORDER by {order} DESC".format(order=order) if order else ""
        else:
            orders = "ORDER by {order}".format(order=order) if order else ""
        sql = "UPDATE {table} SET {param} WHERE {condition} {orders} {limits}".format(table=table,
            param=self.join_field_value(data), condition=condition, orders=orders, limits=limits)
        return self.executecSQL(sql=sql, data_param=data.values(), commit=commit)

    def find(self, table, fields=None, condition=None, limit=None, order=None, desc=False, fetchone=False, commit=True):
        #域处理
        if fields:
            if isinstance(fields, tuple) or isinstance(fields, list):
                fields = '`, `'.join(fields)
                fields = '`{fields}`'.format(fields=fields)
        else:
            fields = "*"
        #查询条件处理
        condition = self.condition(condition)
        #限制处理
        limits = "LIMIT {limit}".format(limit=limit) if limit else ""
        #排序处理
        if desc:
            orders = "ORDER by {order} DESC".format(order=order) if order else ""
        else:
            orders = "ORDER by {order}".format(order=order) if order else ""

        sql = "SELECT {fields} FROM {table} WHERE {condition} {orders} {limits}".format(fields=fields, table=table,
                condition=condition, orders=orders, limits=limits)
        cursor = self.executecSQL(sql=sql, recursor=True, commit=commit)
        if cursor:
            return self.fethandle(cursor, fetchone)
        else:
            return None

    def fethandle(self, cursor, fetchone=False):
        if fetchone:
            result = cursor.fetchone()
            if result:
                for key in result:
                    if isinstance(result[key], type(datetime.datetime(2016, 5, 9, 20, 57, 10))):
                        result[key] = str(result[key])
        else:
            result = cursor.fetchall()
            if result:
                for i in range(0, len(result)):
                    for key in result[i]:
                        if isinstance(result[i][key], type(datetime.datetime(2016, 5, 9, 20, 57, 10))):
                            result[i][key] = str(result[i][key])
        return result

    def join_field_value(self, data, glue=', '):
        sql = comma = ''
        for key in data.keys():
            sql += "{}`{}` = %s".format(comma, key)
            comma = glue
        return sql

    def condition(self, condition):
        if not condition:
            sql = '1'
        elif isinstance(condition, dict):
            sql = ''
            i = 0
            c_len = len(condition)
            for key,val in condition.items():
                i += 1
                if isinstance(val, list):
                    if isinstance(val[0], list):
                        j = 0
                        j_len = len(val)
                        for inner_val in val:
                            j += 1
                            if isinstance(inner_val[1], str):
                                sql += " " + key + " " + inner_val[0] + " " + " '" + inner_val[1] + "' "
                            else:
                                sql += " " + key + " " + inner_val[0] + " " + " " + str(inner_val[1]) + " "
                            if j < j_len:
                                sql += ' AND '
                    else:
                        if isinstance(val[1], str):
                            sql += " " + key + " " + val[0] + " " + " '" + val[1] + "' "
                        else:
                            sql += " " + key + " " + val[0] + " " + " " + str(val[1]) + " "
                elif isinstance(val, str):
                    sql += " " + key + " =" + " '" + val + "' "
                else:
                    sql += " " + key + " =" + " " + str(val) + " "
                if i < c_len:
                    sql += ' AND '
        else:
            sql = condition

        return sql
