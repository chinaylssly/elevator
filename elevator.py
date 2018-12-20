# _*_ coding:utf-8 _*_ 

from time import sleep
from tools import wapper_localtask
from threading import Thread
from config import MAX_FLOOR,MIN_FLOOR,INIT_FLOOR
from globaltask import GlobalTask
from traceback import format_exc

class ElevatorBase(object):
    ##电梯

    def __init__(self,min_floor=MIN_FLOOR,max_floor=MAX_FLOOR,init_floor=INIT_FLOOR,name='BASE'):

        self._name=name
        self.init_floor=INIT_FLOOR
        self.min_floor=MIN_FLOOR
        self.max_floor=MAX_FLOOR
        self._current_floor=self.init_floor
        self.flag=0


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
        self.flag=0
        self.isalive=True

    def __str__(self,):

        return '< elevator:%s at %s floor,destination=%s,flag=%s,isalive=%s >'\
        %(self.name,self.current_floor,self.destination,self.flag,self.isalive)

    def stop(self,):

        self.isalive=False
        self.localtask=set()
        ##stop之后会抹除destination,也可以选择不抹除，视需求而定
        self.flag=0
        self.destination=None

        print u'close elevator:%s,set flag=0,destination=current_floor'%(self.name)

    def restart(self,):
        ##重启电梯，逻辑上需要在stop之后才能调用restart

        self.isalive=True
        print u'restart elevator:%s at %s floor,flag is:%s'%(self.name,self.current_floor,self.flag)

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
                ##电梯未运行状态

                self.destination=floor

                if floor>self.current_floor:
                    ##设置电梯为上行

                    self.flag=1
                    isaccept=True

                   

                elif floor<self.current_floor:
                    #设置电梯为下行

                    self.flag=-1
                    isaccept=True
                   


                elif floor==self.current_floor:

                    ##电梯保持原地不动,

                    if refer=='globaltask':

                        self.flag=0
                        self.destination=floor
                        isaccept=True

                    elif refer=='localtask':
                        self.flag=0
                        isaccept=False
                        self.destination=None


        
        else:
            ##电梯stop，不接受任何任务
            isaccept=False




        if isaccept:

            print u'%s accept the floor=%s you apply from %s'%(self,floor,refer)
            self.localtask.add(floor)
            
        else:
            print u'%s cant accept the floor=%s you apply from %s'%(self,floor,refer)

        return isaccept
        ##判断floor是否成功加入localtask


    def whether_open_by_local(self,):
        ##根据本地任务判断是否打开电梯门

        if self.current_floor in self.localtask:

            print u'open door for person who in %s,'%(self)
            self.localtask.remove(self.current_floor)
            return True

        else:
            print u'%s dont need open the door '%(self)
            return False



    def run(self,):

        while True:
            try:

                while self.isalive:

                    isopen=self.whether_open_by_local()

                    if isopen:
                        sleep(1)
                    else:
                        sleep(0.1)

                    if self.flag:
                        ##self.flag==-1 or self.flag==1

                        if self.current_floor==self.destination:
                            print u'%s reach destination:%s,set flag=0'%(self,self.destination)
                            self.flag=0
                            self.destination=None
                            break

                        if self.flag==-1:
                            self.current_floor-=1
                        elif self.flag==1:
                            self.current_floor+=1

                        print u'%s rearch  %s floor'%(self,self.current_floor)
        
                        
                    else:

                        print u'%s has no task,sleep 2 second!'%(self)
                        sleep(2)

                else:
                    ##电梯brenk
                    print u'elevator:%s is broken at %s floor,waiting for restart!!! '%(self.name,self.current_floor)
                    sleep(10)

            except:

                
                print u'catch except:%s when elevator:%s runing'%(format_exc(),self.name)

                self.isalive=False
                print u'set elevator:%s isalive:%s'%(self.name,self.isalive)

                self.flag=0
                self.destination=None



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
                elevator.add_localtask(8,refer='globaltask')
                
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
