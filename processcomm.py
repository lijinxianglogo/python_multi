# _*_ coding:utf-8 _*_
import os
import fcntl
import time
import multiprocessing
if not os.path.exists("./ll.txt"):
    os.mknod("./ll.txt")
pid1 = os.fork()
if pid1:
    pid2 = os.fork()
    if pid2:
        os.waitpid(pid1, 0)
        os.waitpid(pid2, 0)
    else:
        time.sleep(1)
        with open("./ll.txt", "a+") as f:
            # fcntl.flock(f, fcntl.LOCK_EX)
            f.write("李锦祥")
            # fcntl.flock(f, fcntl.LOCK_UN)

else:
    with open("./ll.txt", "a+") as f:
        # fcntl.flock(f, fcntl.LOCK_EX)
        f.write("我是")
        time.sleep(0.5)
        f.write("sdfsdfsdfsd")
        time.sleep(3)
        # fcntl.flock(f, fcntl.LOCK_UN)



