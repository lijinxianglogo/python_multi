#_*_ coding:utf-8 _*_
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/EH100602/sys/LCTTestTool/SendDisplayData/BsCommSucRateTest")

def on_message(client, userdata, msg):
    print("title:" + msg.topic + " mess:" + str(msg.payload))

#定义一个mqtt客户端的类实体
client = mqtt.Client()
#定义链接mqtt的回调函数
client.on_connect = on_connect
#定义收到消息时的回调函数
client.on_message = on_message

client.username_pw_set("ehigh", "123456")

client.connect("192.168.4.44", 1883, 60)

#启动函数
client.loop_forever()

