# -*- coding: utf-8 -*-
import socket
import select
import os
def TCPClient():
    #TCP:基于连接的通讯
    #创建以恶搞套接字
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #连接某个服务器
    sk_address = ('127.0.0.1', 9566)
    sk.connect(sk_address)
    # sk.settimeout(5)
    # 设置select的监听列表
    rlist = [sk]
    while True:
        sk.sendall(str(os.getpid()))
        c_rlist, c_wlist, c_xlist = select.select(rlist, [], [], 1)
        for c_read in c_rlist:
            if c_read == sk:
                data = sk.recv(1024)
                if len(data):
                    print(len(data))
                else:
                    print(len(data))
                    exit(1)

import time
def UDPClient():
    # UDP: 基于非连接的通讯
    #recvfrom和sendto
    # 创建UDP套接字
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置非阻塞模式
    sk.setblocking(0)
    #服务器地址
    sk_address = ('127.0.0.1', 9566)
    sk.sendto(b'', sk_address)
    while True:
        # 调用select监听
        rlist = [sk]
        c_rlist, c_wlist, c_xlist = select.select(rlist, [], [],1)
        for c_read in c_rlist:
            if c_read == sk:
                data, address = sk.recvfrom(1024)
                print( address, data.decode())
        sk.recvfrom(1024)
        print(121212)

# UDPClient()
