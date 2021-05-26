# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler
import colorlog
import os
class CSLog(object):
    def __init__(self, project_name, log_path):
        assert (project_name != None)
        assert (log_path != None)
        if (os.path.exists(os.path.split(log_path)[0])):
            pass
        else:
            os.mkdir(os.path.split(log_path)[0])
        self.logger = logging.getLogger(project_name)
        self.logger.setLevel(logging.DEBUG)
        Colorformatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(name)s-%(levelname)s(file: %(filename)s, func: %(funcName)s, line: %(lineno)d, pid: %(process)d): %(message)s")
        formatter = logging.Formatter(
            "%(asctime)s %(name)s-%(levelname)s(file: %(filename)s, func: %(funcName)s, line: %(lineno)d, pid: %(process)d): %(message)s")
        #文件配置
        fileHander = TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=7)
        fileHander.setLevel(logging.INFO)
        fileHander.setFormatter(formatter)
        #屏幕输出
        streamHander = logging.StreamHandler()
        streamHander.setLevel(logging.INFO)
        streamHander.setFormatter(Colorformatter)
        #加入logger
        self.logger.addHandler(fileHander)
        self.logger.addHandler(streamHander)

    def getlogger(self):
        return self.logger