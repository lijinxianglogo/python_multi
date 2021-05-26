# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
# 定义一个mqtt客户端的类实体
client = mqtt.Client()
# 通行账户和密码
client.username_pw_set('ehigh', 'Abc123')
# 连接回调函数


def connect_callback(client, userdata, flags, rc):
    # print client, userdata, flags, rc
    client.subscribe('/EH100602/tx/#')


def message_callback(client, userdata, message):
    print client, userdata, message
    print message.payload


client.on_connect = connect_callback
client.on_message = message_callback
# 服务器ip，端口，维持心跳
client.connect("192.168.4.44", 1883, 3600)
client.loop_forever()