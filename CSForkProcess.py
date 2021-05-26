# -*- coding: utf-8 -*-
import os
import ctypes
libc = ctypes.CDLL('libc.so.6')


class ForkProcess(object):
    def __init__(self, exe_path):
        self.exe_path = exe_path

    def start_process(self, file_path):
        child_pid = os.fork()
        if child_pid:
            os.wait()
        else:
            libc.prctl(1, 15)
            # os.execv(self.exe_path, (self.exe_path, 'subprocess_test.py'))
            # os.execl(self.exe_path, self.exe_path, '/home/ehigh/work/CSframe/subprocess_test.py')
            # os.execvp(self.exe_path, (self.exe_path, 'subprocess_test.py'))
            os.execlp(self.exe_path, self.exe_path, file_path)