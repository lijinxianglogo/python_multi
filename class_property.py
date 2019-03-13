#_*_ coding:utf-8 _*_
class property_test(object):
    def __init__(self):
        self._func_test = None
        self.a1 = 1
        self.a2 = 2
        self.a3 = 3
    @property
    def test_callback(self):
        return self._func_test

    @test_callback.setter
    def test_callback(self, func):
        self._func_test = func

    def sum_all(self):
        self.test_callback(self.a1, self.a2, self.a3)

def test_callback(a1, a2, a3):
    print a1+a2+a3

mytest = property_test()
mytest.test_callback = test_callback
mytest.sum_all()