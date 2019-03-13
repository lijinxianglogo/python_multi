# -*- coding: utf-8 -*-
import httplib2
http = httplib2.Http('cache')
response, content = http.request("http://192.168.4.44")
xx =None
if type(xx) is str and "jj" in xx:
    print 56
