# -*- encoding: utf-8 -*-
"""
@File    :   DateTime.py    
@Contact :   lijinxianglogo@163.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
9/25/19 11:50 AM   lijinxiang      1.0         None
"""
import datetime
import time
from pytz import timezone

cst_tz = timezone('Asia/Shanghai')
ust_tz = timezone('UTC')
u_time = time.time()
# 时间戳转换为iso date，其中cst_tz表示这时哪个时区的时间
u_iso = datetime.datetime.fromtimestamp(u_time, cst_tz).isoformat()
print u_iso
print datetime.datetime.utcnow().replace(tzinfo=ust_tz).isoformat()
print datetime.datetime.utcnow().replace(tzinfo=ust_tz).astimezone(cst_tz).isoformat()