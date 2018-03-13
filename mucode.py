# _*_ coding:utf-8 _*_
'''
从UCS-2到UTF-8的编码方式如下： UCS-2编码(16进制) UTF-8 字节流(二进制) 0000 - 007F 0xxxxxxx 0080 - 07FF 110xxxxx 10xxxxxx 0800 - FFFF 1110xxxx 10xxxxxx 10xxxxxx
例如“汉”字的Unicode编码是6C49。6C49在0800-FFFF之间，所以肯定要用3字节模板了：1110xxxx 10xxxxxx 10xxxxxx。
将6C49写成二进制是：0110 110001 001001， 用这个比特流依次代替模板中的x，得到：11100110 10110001 10001001，即E6 B1 89
UTF-16以16位为单元对UCS进行编码。对于小于0x10000的UCS码，UTF-16编码就等于UCS码对应的16位无符号整数。
对于不小于0x10000的UCS码，定义了一个算法。不过由于实际使用的UCS2，或者UCS4的BMP必然小于0x10000，所以就目前而言，可以认为UTF-16和UCS-2基本相同。
'''
'''
主要关于ord,chr,unichr,unicode,encode,decode,unpack的研究
'''
import struct

def getfiledata():
    try:
        #需要修改为本地路径
        with open("/home/ehigh/Downloads/fw_tag_v3.3.26_YS.HGbin", "r") as fp:
            return fp.read(20)
    except Exception, e:
        print e
        return False
'''
因为python的print是不能直接打印二进制的数的，如果需要看二进制的数，可以用struct.unpack来解析，因为read的都是字节流，
所以用unpack中的B来进行解析，因为这样可以得到字节的值是多少，
'''
print struct.unpack("<20B", getfiledata())
#结果(80, 0, 114, 0, 111, 0, 100, 0, 117, 0, 99, 0, 116, 0, 58, 0, 69, 0, 72, 0)
'''
如果文件编码不是ascii和utf-8的，比如是utf-16的则需要转换编码使用unicode
'''
data = getfiledata()
print data
#P r o d u c t : E H
print unicode(data, 'utf-16')
#Product:EH
'''
因为在python2.x中，ord和chr对非ascii编码不是很友善,如果要ord超过ascii的字符需要用u'xx'表示才可以转换
#u表示unicode编码，b表示字节流，
'''
print ord(u'中')
print ord('A')
print chr(65)
#用chr(20013)会报错，是否有什么方法，暂时不知道，所以用unichr
print unichr(20013)
'''
关于encode和decode
encode表示将unicode的str转换为bytes字节流，然后这样的方法就可以用ord或者unpack看见对应的编码值时多少
'''
p1 = u'中文'.encode('utf-16')
p2 = u'中文'.encode('utf-8')
print len(u'中文'), len(p1), len(p2)
p3 = p2.decode('utf-8')
print type(p3)
print struct.unpack("<6B", p1)
print struct.unpack("<6B", p2)
'''
结果为：
6 6
(255, 254, 45, 78, 135, 101)
(228, 184, 173, 230, 150, 135)
可以看出unicode的str被变为了bytes字节流
'''
'''
关于unicode编码的文件名创建会报错,因为文件名只能是str，所以需要使用encode转为字符串
'''
import os
def mknodfile(file_name):
    fpath = "/home/ehigh/Downloads/"
    fw_path = fpath + file_name
    try:
        if not os.path.exists(fpath):
            os.mkdir(fpath)
        if os.path.exists(fw_path):
            os.remove(fw_path)
        os.mknod(fw_path)
    except Exception, e:
        import traceback
        print (traceback.format_exc())
        print (e)
        return False
#mknodfile(u'中文') 这样会报错
mknodfile(p2)
print type(p2)
