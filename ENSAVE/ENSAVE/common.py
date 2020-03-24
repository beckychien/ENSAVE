# -*- coding: UTF-8 -*-
import pymssql
# import pymysql
import time
import datetime
import os
import traceback
import sys
from ENSAVE.myLog import MyLog
from decimal import *
from django.db import connection

mylog = MyLog('COMMON')


sqlhost = "134.175.55.99"
sqlport = 1433
sqluser = "psk"
sqlpwd = "123456"

class Common(object):
    def GetData(strsql):
        conn = pymssql.connect(host=sqlhost, user=sqluser, password=sqlpwd, port=sqlport,
                               database='eis_bak', charset="utf8")

        cursor = conn.cursor()
        # 執行sql查詢語句
        try:
            cursor.execute(strsql)

            # 取得查詢結果
            ret = cursor.fetchall()
            cursor.close()
            conn.close()
            return ret


        except Exception as inst:
            mylog.logger.error(strsql)
            mylog.logger.error(inst)
            cursor.close()
            conn.close()
            print(inst)
            raise

    # def WriteToDb(sqllist):
    #     conn = pymssql.connect(host=sqlhost, user=sqluser, password=sqlpwd, port=sqlport,
    #                            database='eis_bak', charset="utf8")
    #     cursor = conn.cursor()
    #     try:
    #         sql = ''
    #         for item in sqllist:
    #             sql = item
    #             cursor.execute(item)
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #     except Exception as inst:
    #         mylog.logger.error(sql)
    #         mylog.logger.error(inst)
    #         conn.rollback()
    #         cursor.close()
    #         conn.close()
    #         raise

    def CombineSqlStr(row):
        sql = ''
        for item in row:
            if str(item) == "None":
                sql = sql + 'null' + ','
            else:
                sql = sql + '"' + str(item) + '"' + ','

        sql = sql.strip(',')
        sql += ')'

        return sql
