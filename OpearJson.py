# _*_ coding:utf-8 _*_
import json
def ReadAndChangeJsonFile():
    try:
        with open("./version.json", "r") as fileload:
            file_read = json.load(fileload)
            file_read["version"]= "jsonfiletest"
        return file_read
    except Exception, e:
        print e
        return False

strdata = ReadAndChangeJsonFile()
if strdata:
    try:
        with open("./version.json", "w") as fp:
            json.dump(strdata, fp)
    except Exception, e:
        print e

def take_dd(elem):
    return elem["dd"]
x1 = [{"ss":78, "dd":43}, {"ss":90, "dd":668}, {"ss":34, "dd":366}]
x1.sort(key=take_dd)
print x1

def takeSecond(elem):
    return elem[1]
random = [(2, 2), (3, 4), (4, 1), (1, 3)]
random.sort(key=takeSecond)
print random

import operator
x1 = [{"ss":78, "dd":43}, {"ss":90, "dd":668}, {"ss":34, "dd":366}]
x1.sort(key=operator.itemgetter("ss"))
print x1
random = [(2, 2), (3, 4), (4, 1), (1, 3)]
random.sort(key=operator.itemgetter(0))
print random

