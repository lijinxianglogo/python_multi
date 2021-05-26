# -*- coding: utf-8 -*-
import select
import socket
import os
import errno
import sys
import multiprocessing
import threading
import signal
import ctypes
libc = ctypes.CDLL('libc.so.6')
sys.path.append("..")
import logging
cslog = logging
TIMEOUT = 5


class TCPServer(object):
    def __init__(self, sk_address=('127.0.0.1', 9566)):
        global libc
        # TCP:基于连接的通讯
        # 创建TCP套接字
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口可以立即使用
        self.sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 将套接字绑定到某个地址
        self.sk.bind(sk_address)
        # 设置最大监听个数
        self.sk.listen(5)
        # select监听tcp母套接字
        self.f_rlist = [self.sk]

    def fork_run(self):
        # 子进程列表
        child_pid_list = []
        while True:
            # ********************回收子进程****************************
            for child_pid in child_pid_list:
                try:
                    p, status = os.waitpid(child_pid, os.WNOHANG | os.WUNTRACED | os.WCONTINUED)
                    if p == -1:
                        if status == errno.EINTR:
                            child_pid_list.remove(child_pid)
                            cslog.info("被信号中断")
                        elif status == errno.ECHILD:
                            cslog.info("该pid不可等待")
                    elif p > 0:
                        if os.WIFSTOPPED(status):
                            cslog.info('子进程并没有退出,只是停止工作')
                        elif os.WIFCONTINUED(status):
                            cslog.info('子进程恢复了运行')
                        else:
                            child_pid_list.remove(child_pid)
                            cslog.info('子进程结束了')
                except Exception as e:
                    print(e)
            # ********************回收子进程end****************************
            # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            fc_rlist, fc_wlist, fc_xlist = select.select(self.f_rlist, [], [], 0.1)
            for fc_read in fc_rlist:
                if fc_read == self.sk:
                    # 等待接收连接请求，并为新的连接分配新的套接字
                    conn, address = self.sk.accept()
                    pid = os.fork()
                    if pid:
                        child_pid_list.append(pid)
                        conn.close()
                    else:
                        self.__tcp_server_child(conn)
                        exit(1)

    def multiprocess_run(self):
        # 子进程列表
        child_pid_list = []
        while True:
            # ********************回收子进程****************************
            for cp in child_pid_list:
                cp.join(0.01)
            # ********************回收子进程end****************************
            # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            fc_rlist, fc_wlist, fc_xlist = select.select(self.f_rlist, [], [], 0.1)
            for fc_read in fc_rlist:
                if fc_read == self.sk:
                    # 等待接收连接请求，并为新的连接分配新的套接字
                    conn, address = self.sk.accept()
                    cslog.info("新的tcp客户端连接:{address}".format(address=address))
                    cp = multiprocessing.Process(target=self.__tcp_server_child, args=(conn,))
                    cp.start()
                    child_pid_list.append(cp)
                    conn.close()

    def thread_run(self):
        # 子线程程列表
        while True:
            # ********************回收子进程end****************************
            # signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            fc_rlist, fc_wlist, fc_xlist = select.select(self.f_rlist, [], [], 0.1)
            for fc_read in fc_rlist:
                if fc_read == self.sk:
                    # 等待接收连接请求，并为新的连接分配新的套接字
                    conn, address = self.sk.accept()
                    cslog.info("新的tcp客户端连接:{address}".format(address=address))
                    loop = threading.Thread(target=self.__tcp_server_child, args=(conn,))
                    # loop.setDaemon(True)
                    loop.start()

    @staticmethod
    def __tcp_server_child(conn):
        global TIMEOUT
        #主进程退出，子进程自动退出
        libc.prctl(1, 15)
        # 设置新套接字的超时时间为5s
        timeout = 0
        rlist = [conn]
        while True:
            if timeout < TIMEOUT:
                connect = False
                c_rlist, c_wlist, c_xlist = select.select(rlist, [], [], 1)
                for c_read in c_rlist:
                    if c_read == conn:
                        # 利用新的套接字与客户端进行通信
                        # conn.sendall('你好我是TCP服务器，你现在可以向我发送信息了！！！')
                        # 利用新的套接字，等待接收客户端的信息，超时则继续等待接收
                        data = conn.recv(1024)
                        if len(data):
                            timeout = 0
                            connect = True
                            cslog.info(data)
                if not connect:
                    timeout += 1
            else:
                break
        conn.close()
        return True

    def list_run(self):
        global TIMEOUT
        conn_list = []
        conn_timeout_list = []
        while True:
            pop_index = []
            #记录超时的客户端
            for i in range(len(conn_timeout_list)):
                if conn_timeout_list[i] >= TIMEOUT:
                    pop_index.append(i)
                else:
                    conn_timeout_list[i] += 1
            # 将超时的客户端断开连接，并移除
            j = 0
            for i in pop_index:
                conn_list[i-j].close()
                conn_list.pop(i-j)
                conn_timeout_list.pop(i-j)
                j += 1
            # 获取新的tcp客户端连接
            fc_rlist, fc_wlist, fc_xlist = select.select(self.f_rlist, [], [], 1)
            for fc_read in fc_rlist:
                if fc_read == self.sk:
                    conn, address = self.sk.accept()
                    if conn in conn_list:
                        conn_index = conn_list.index(conn)
                        conn_timeout_list[conn_index] = 0
                    else:
                        conn_list.append(conn)
                        conn_timeout_list.append(0)
                        cslog.info("新的tcp客户端连接:{address}".format(address=address))
            # 轮询客户端连接列表
            conn_rlist, conn_wlist, conn_xlist = select.select(conn_list, [], [], 1)
            for conn_read in conn_rlist:
                if conn_read in conn_list:
                    data = conn_read.recv(1024)
                    if len(data):
                        print(data)
                        index = conn_list.index(conn_read)
                        conn_timeout_list[index] = 0

class UDPServer(object):
    def __init__(self, sk_address=('127.0.0.1', 50000)):
        # UDP: 基于非连接的通讯
        # 创建UDP套接字
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 设置端口可以立即使用
        self.sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设置非阻塞
        self.sk.setblocking(0)
        # 将套接字绑定到某个地址
        self.sk.bind(sk_address)
        # 设置select的监听列表
        self.rlist = [self.sk]

    def start_server(self):
        client_list = []
        i = 1
        while True:
            i += 1
            # #调用select监听
            c_rlist, c_wlist, c_xlist = select.select(self.rlist, [], [], 0.1)
            for c_read in c_rlist:
                if c_read == self.sk:
                    data, address = self.sk.recvfrom(1024)
                    client_list.append(address)
                    print(data)
            # for client in client_list:
            #     self.sk.sendto('你好，UDP服务器已经收到了你的消息：{infomation}'.format(infomation=i).encode(), client)



# tcp_server = TCPServer()
# tcp_server.thread_run()
udp = UDPServer()
udp.start_server()









