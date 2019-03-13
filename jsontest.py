# -*- coding: utf-8 -*-
"""
   Copyright (c) 2017, Everhigh Tech. Ltd. Co.
      		  All rights reserved

Created on Mon Nov 13 15:51:31 2017

@author: luochao
@brief : back call by the SDK
"""
import os
import json
def writeJsonFile(jsondata):
    if type(jsondata) is dict:
        try:
            with open("./ALLVersion.json", "w") as fp:
                json.dump(jsondata, fp)
            return True
        except Exception, e:
            import traceback
            print (traceback.format_exc())
            print (e)
            return False
    else:
        print ("param need sict")
        return False

def ReadAndChangeJsonFile(proj, version):
    if (type(proj) is str) and (type(version) is str):
        try:
            if not os.path.exists("./ALLVersion.json"):
                os.mknod("./ALLVersion.json")
            if os.path.getsize("./ALLVersion.json"):
                with open("./ALLVersion.json", "r") as fp:
                    file_read = json.load(fp)
                    file_read[proj] = version
            else:
                print ("file is temp----ALLVersion.json")
                file_read = {}
                file_read[proj] = version
            return file_read
        except Exception, e:
            import traceback
            print (traceback.format_exc())
            print (e)
            return False
    else:
        print ("param need str")
        return False
# data = ReadAndChangeJsonFile("ttt", "1.2.3.4")
# data = {"error":"1.2.45.567"}
writeJsonFile(data)