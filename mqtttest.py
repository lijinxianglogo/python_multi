#_*_ coding:utf-8 _*_
import os
import time
import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print "成功连接mqtt服务器"
    client.subscribe("chart")

def on_message(client, userdata, msg):
    print(str(msg.payload))

pid = os.fork()
#定义一个mqtt客户端的类实体
client = mqtt.Client()
#通行账户和密码
client.username_pw_set("ehigh", "123456")
#服务器ip，端口，维持心跳
client.connect("192.168.4.44", 1883, 60)
#主进程用于监听topic和显示消息
if pid:
    #定义链接mqtt的回调函数，一般要连接的topic都是在这里连接
    client.on_connect = on_connect
    #定义收到消息时的回调函数
    client.on_message = on_message
#子进程用于发送消息
else:
    time.sleep(0.1)
    print "请输入您的昵称以便双方交流："
    name = raw_input()
    client.publish("chart", str(name) + ":你好，我是" + str(name))
    while 1:
        send_info = raw_input()
        client.publish("chart", str(name) + ":" + send_info)
        time.sleep(1)
#启动函数
client.loop_forever()

