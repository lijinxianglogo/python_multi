# _*_ coding:utf-8 _*_
import multiprocessing
import os
import time
'''
进程池的使用，便于管理,启动之前要先close
'''
def pool_subprocess(i):
    print i
    print "子进程" + str(os.getpid())
    time.sleep(5)

p = multiprocessing.Pool(4)
for i in range(4):
    p.apply_async(pool_subprocess, args=(i,))
p.close()
#用deamon来让子进程自动退出
# p.deamon = True
#用join来等待子进程
p.join()
time.sleep(1)
print "EXIT"
