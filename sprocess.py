# _*_ coding:utf-8 _*_
import os
import subprocess
#subprocess 用来系统交互
# /subprocess.call(["python", "mprocess.py"])

p = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
out, err = p.communicate()
print out
#可以用subprocess来进行系统调用，替代之前的很多系统函数
print os.getcwd()


