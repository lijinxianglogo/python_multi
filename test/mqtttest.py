#_*_ coding:utf-8 _*_
import os
import time
import paho.mqtt.client as mqtt
import signal


# 定义一个mqtt客户端的类实体
client = mqtt.Client()
# 通行账户和密码
client.username_pw_set("admin", "eHIGH2014")
# 服务器ip，端口，维持心跳
client.connect("127.0.0.1", 1884, 60)
# 主进程用于监听topic和显示消息
pid = os.fork()
if pid:
    # 不关心子进程是否结束，由系统init进行回收
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)


    def on_connect(client, userdata, flags, rc):
        print "成功连接mqtt服务器"
        client.subscribe("/chart")


    def on_message(client, userdata, msg):
        print('{}: {}'.format(pid, msg.payload))
    # 定义链接mqtt的回调函数，一般要连接的topic都是在这里连接
    client.on_connect = on_connect
    # 定义收到消息时的回调函数
    client.on_message = on_message
# 子进程用于发送消息
else:
    time.sleep(0.1)
    print "请输入您的昵称以便双方交流："
    name = raw_input()
    client.publish("/chart", "{}-{}:你好,我是{}".format(name, pid, name))
    while 1:
        send_info = raw_input()
        client.publish("/chart", "{}-{}: {}".format(name, pid, send_info))
        time.sleep(1)
# ？我的主进程在工作，不能一直wait，怎么办？在创建一个子进程进行消息发送,然后让主进程一直wait
# 启动函数
client.loop_forever()

