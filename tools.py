# _*_ coding:utf-8 _*_ 
from config import MIN_FLOOR,MAX_FLOOR


def wapper_globaltask(func):
    ##装饰类方法，按照语法糖的原生理解方式理解的话会好理解很多
    ##用于判断globaltask的floor的范围

    def inner(cls,floor):

        if floor>=MIN_FLOOR and floor<=MAX_FLOOR:
            isaccept=func(cls,floor)
           
        else:
            print u'system get invalid floor:%s,floor must in range[%s,%s]'%(floor,MIN_FLOOR,MAX_FLOOR)
            isaccept=False

        return isaccept

    return inner


def wapper_localtask(func):
    ##装饰类方法，按照语法糖的原生理解方式理解的话会好理解很多
    ##用于判断globaltask的floor的范围

    def inner(cls,floor,refer='localtask'):

        if floor>=MIN_FLOOR and floor<=MAX_FLOOR:
            isaccept=func(cls,floor,refer)
           
        else:
            print u'system get invalid floor:%s,floor must in range[%s,%s]'%(floor,MIN_FLOOR,MAX_FLOOR)
            isaccept=False

        return isaccept

    return inner