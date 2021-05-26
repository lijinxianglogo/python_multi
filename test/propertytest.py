# _*_ coding:utf-8 _*_


class PropertyTest(object):
    def __init__(self):
        self.__func_test = None
        self.a1 = 1
        self.a2 = 2
        self.a3 = 3

    @property
    def test_callback(self):
        return self.__func_test

    @test_callback.setter
    def test_callback(self, func):
        self.__func_test = func


def test_callback(a1, a2, a3):
    print a1+a2+a3


my_test = PropertyTest()
my_test.test_callback = test_callback
my_test.test_callback(1, 2, 3)
