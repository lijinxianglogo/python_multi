#_*_ coding:utf-8 _*_
'''
关于linux下的prctl的作用：ctypes.CDLL("libc.so.6")下的prctl只在fork下有用，
在multiprocessing下时没有用的，在multiprocessing下用daemon可以做到
当子进程被杀死的时候，一定要调用wait或者join进行回收，所以对任何子进程都需要wait处理，包括kill掉的子进程都需要wait
'''
import multiprocessing
import time
import ctypes
libc = ctypes.CDLL("libc.so.6")
def run_subprocess1():
    for i in range(5):
        print "sub1"
        time.sleep(1)

def run_subprocess2():
    for i in range(5):
        print "sub2"
        time.sleep(1)

def run_subprocess3():
    for i in range(5):
        print "sub3"
        time.sleep(1)

'''
自动启动非正常死掉的进程
守护进程死掉以后主进程停止wait
'''
p1 = multiprocessing.Process(target=run_subprocess1)
p2 = multiprocessing.Process(target=run_subprocess2)
p3 = multiprocessing.Process(target=run_subprocess3)
active_p = [p1, p2, p3]
print time.time()
for p in active_p:
    p.daemon = True
    p.start()
for p in active_p:
    #如果join放在上一个for后面那么进程不会并发执行
    p.join()
print time.time()
print "主进程exit"
# import os
# import time
# import ctypes
# import signal
# libc = ctypes.CDLL("libc.so.6")
# def sig_hander(sig_num, acc_sig):
#     os.wait()
#     print "子进程退出"
# for i in range(1):
#     print i
#     pid = os.fork()
#     if pid:
#         #不关心子进程是否退出,由系统的init接管，非阻塞
#         # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
#         #创建hander函数，子啊hander函数里面调用wait，非阻塞
#         # signal.signal(signal.SIGCHLD, sig_hander)
#         #自己调用wait，阻塞
#         # os.waitpid(pid, 0)
#         print "父进程" + str(os.getpid())
#         time.sleep(1)
#         #关于waitpid函数中的opion，当opion = WNOHANG时，没有收到子程序推出信息也会立即返回，用于定时检测子程序
#         xx = os.waitpid(pid, 0)
#     else:
#         libc.prctl(1, signal.SIGINT)
#         time.sleep(0.5)
#         print "子进程" + str(os.getpid())
#         #可以通过break控制子进程是否进入循环
#         break


