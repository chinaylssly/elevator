# _*_ coding:utf-8 _*_ 

from collections import defaultdict,OrderedDict

def wapper(func):

    def inner():

        return 'inner'
    return inner

@wapper
def raw():

    return 'raw'


print raw()
