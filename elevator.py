# _*_ coding:utf-8 _*_ 

from time import sleep
from tools import wapper_localtask
from threading import Thread
from config import MAX_FLOOR,MIN_FLOOR,INIT_FLOOR
from globaltask import GlobalTask
from traceback import format_exc
import random

class ElevatorBase(object):
    ##电梯

    def __init__(self,min_floor=MIN_FLOOR,max_floor=MAX_FLOOR,init_floor=INIT_FLOOR,name='BASE'):

        self._name=name
        self.init_floor=INIT_FLOOR
        self.min_floor=MIN_FLOOR
        self.max_floor=MAX_FLOOR
        self._current_floor=self.init_floor


        print u'create elevator:%s successfully!'%(self.name)

    @property
    def name(self):
        ##设置name为只读属性
        return self._name

    @property
    def current_floor(self):
        return self._current_floor

    @current_floor.setter
    def current_floor(self,value):

        assert value>=self.min_floor and value<=self.max_floor,\
        'current_floor out of range[%s:%s] but get %s'%(self.min_floor,self.max_floor,value)

        self._current_floor=value
        print u'set elevator:%s at %d floor'%(self.name,self.current_floor)

    def run(self):
        pass

    def analyze(self,):
        pass


    def __str__(self,):

        return 'elevator:%s at %s floor'%(self.name,self.current_floor)


class Elevator(ElevatorBase):

    def __init__(self,name='child'):

        ElevatorBase.__init__(self,name=name)

        self.globaltask=GlobalTask.task
        self.localtask=set()
        self.destination=None
        self.isalive=True
        self.ismoving=False
        self.isopen=False


    def __str__(self,):

        return '< elevator:%s at %s floor,destination=%s,flag=%s,isalive=%s >'\
        %(self.name,self.current_floor,self.destination,self.flag,self.isalive)


    @property
    def flag(self,):
        ##电梯运行方向，设置为只读

        if self.destination is None:
            self._flag=0

        else:
            if self.destination > self.current_floor:
                self._flag=1

            elif self.destination < self.current_floor:
                self._flag=-1

            else:
                self._flag=0

        return self._flag


    def stop(self,):
        ##电梯停运，检修

        self.isalive=False
        self.localtask=set()
        self.destination=None

        print u'stop %s'%(self)

    def restart(self,):
        ##重启电梯，逻辑上需要在stop之后才能调用restart

        self.isalive=True
        self.localtask=set()
        self.destination=None
        print u'restart %s'%(self)
        # self.run()


    def open_door(self,):
        ##开启电梯门

        if  self.ismoving:

            print u'Warning: %s is runing,Disallow open the door!'%(self,)

        else:
            self.isopen=True
            print u'%s open the door,then sleep 1 second!'%(self,)
            sleep(1)

    def close_door(self,):
        ##关闭电梯门

        if self.isopen:

            self.isopen=False
            print u'%s close the door'%(self,)

        else:
            print u'%s door is closed,with no need for closing!'%(self,)


    @wapper_localtask
    def add_localtask(self,floor,refer='localtask'):
        ##上电梯内的人选择楼层
        ##在增加楼层的时候就确定本次电梯运行的终点
        ##add_localtask只会增加与其方向一致的路线

        if self.isalive:

            if self.flag==-1:

                if floor>self.current_floor:
                    isaccept=False

                else:
                    isaccept=True
                    self.destination=min(self.destination,floor)

            elif self.flag==1:

                if floor<self.current_floor:
                    isaccept=False
                   
                else:
                    isaccept=True
                    self.destination=max(self.destination,floor)


            elif self.flag==0:


                if self.current_floor == floor:

                    if refer == 'localtask':
                        isaccept=False

                    elif refer=='globaltask':
                        isaccept=True
                        self.destination=floor

                else:

                    isaccept=True
                    self.destination=floor
            
        else:
            ##电梯stop，不接受任何任务
            isaccept=False

        if isaccept:
            print u'%s accept task %s from %s'%(self,floor,refer)
            self.localtask.add(floor)

        else:
            print u'%s ignore task %s from %s'%(self,floor,refer)

        return isaccept



    def whether_open_door_when_runing(self,):
        ##根据本地任务判断是否打开电梯门

        if self.current_floor in self.localtask:
            ##有可能判断是否开门的时候，isalive恰好被更改了

            self.open_door()
            self.close_door()

            try:
                print u'%s remove %s from localtask:%s'%(self,self.current_floor,self.localtask)
                self.localtask.remove(self.current_floor)
            except:
                raise
                
            return True

        else:
            print u'%s with no need for open the door,sleep 0.1 second!'%(self)
            return False


    def run(self,):

        print u'run %s'%(self)

        while self.isalive:

            try:

                isopen=self.whether_open_door_when_runing()

                if self.current_floor == self.destination:

                        print u'%s reach destination'%(self)
                        self.destination=None
              
                if self.flag==-1:
                    self.current_floor-=1
                    print u'%s rearch new floor'%(self)

                elif self.flag==1:
                    self.current_floor+=1
                    print u'%s rearch new floor'%(self)
                    
    
                else:
                    print u'%s has no task,sleep 2 second!'%(self)
                    sleep(2)

            except:

                print u'catch exception when elevator:%s runing,will stop this elevator'%(self.name)
                print u'%s traceback info: \n%s'%(self,format_exc())
                self.stop()
        else:

            print u'%s is broken ,sleep 5 second waiting for restart!!! '%(self)
            sleep(5)

       

def test_elevator(elevator):

    elevator.add_localtask(7)
    elevator.add_localtask(8)
    elevator.add_localtask(-3)
    elevator.add_localtask(-18)
    elevator.run()


def test():

    elevator=Elevator()
    from  threading import Thread

    def test_input(elevator):
        
        while True: 

            if elevator.flag ==0:

                refer=random.choice(['globaltask','localtask'])
                elevator.add_localtask(8,refer=refer)
                
            else:
                print u'pass add input'

            sleep(2)
                

    t1=Thread(target=test_elevator,args=(elevator,))
    t2=Thread(target=test_input,args=(elevator,))

    t1.start()
    t2.start()

if __name__ =='__main__':



    # test_elevator()
    test()
