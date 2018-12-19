# _*_ coding:utf-8 _*_ 

from collections import defaultdict
from tools import wapper_globaltask



class GlobalTask(object):
    ##所有电梯都能接受到的任务

    task=defaultdict(set)

    @classmethod
    @wapper_globaltask
    def add_up(cls,floor):

        print u'someone wait up at %s floor'%floor
        cls.task['up'].add(floor)

    @classmethod
    @wapper_globaltask
    def add_down(cls,floor):

        print u'someone wait down at %s floor'%floor
        cls.task['down'].add(floor)

    @classmethod
    @wapper_globaltask
    def add_exigency_up(cls,floor):

        print u'exigency! someone wait up at %s floor'%floor
        cls.task['exigency_up'].add(floor)

    
    @classmethod
    @wapper_globaltask
    def add_exigency_down(cls,floor):
        ##紧急事件，不顾系统的其他调度，直接调度最近的电梯

        print u'exigency! someone wait down at %s floor'%floor
        cls.task['exigency_down'].add(floor)






def test_GlobalTask():

    g=GlobalTask()
    g.add_down(7)
    g.add_up(100)
    g.add_exigency_down(167)
    g.add_exigency_down(67)
    g.add_exigency_up(-2)
    print g.task

if __name__=='__main__':

    test_GlobalTask()