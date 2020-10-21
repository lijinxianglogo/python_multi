# _*_ coding:utf-8 _*_

#python本身是不支持二进制的，打印的时候默认是unicode的UTF-8编码,所以需要用unpack来解包

from Crypto.Cipher import AES
class prpcrypt(object):
    def __init__(self, key, IV):
        #这里的密匙和IV默认为16字节128位的
        self.key = key
        self.IV = IV
        self.mode = AES.MODE_CBC
        #AES加密的块长度是16字节
        self.length = 16

    def encrypt(self, bdata):
        try:
            # 由于加密的字符串必须是16的倍数，所以对于字符串需要进行补齐操作
            cryptor = AES.new(self.key, self.mode, self.IV)
            add = 0
            if len(bdata) % self.length:
                add = self.length - (len(bdata) % self.length)
            # 将需要补齐的个数转换为对应ascii字符进行补齐
            bdata = bdata + (chr(add) * add)
            return cryptor.encrypt(bdata)
        except Exception, e:
            print e
            return False

    def decrypt(self, bdata):
        try:
            #由于系统的原因这里可以全部加FF，常规是需要去除掉添加的字符的
            cryptor = AES.new(self.key, self.mode, self.IV)
            de_data = cryptor.decrypt(bdata)
            #对解密过后的数据进行处理并返回
            return self.__GetDecryptData(de_data)
        except Exception, e:
            return False

    def __GetDecryptData(self, de_data):
        try:
            '''
            1.判断数据是否添加字符,如果没有添加则直接返回参数
            2.如果添加了,则对数据进行截取
            '''
            add_str = de_data[-1]
            if ord(add_str) >= 0xF:
                return de_data
            for c in de_data[-ord(add_str):]:
                if c != add_str:
                    return de_data
            return de_data[:len(de_data)-ord(add_str)]
        except Exception, e:
            return False


# data = {1:{'test1':9},2:{'test2':8}}
# data1 = {3:{'test1':9},2:{'test2':66}}
#
# print dict(data.items()+ data1.items())
data = [u'我', u'白', u'啊', u'中']
print sorted(data)
print '三十三'