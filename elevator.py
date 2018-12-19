# _*_ coding:utf-8 _*_ 

from time import sleep
from tools import wapper_localtask
from threading import Thread
from config import MAX_FLOOR,MIN_FLOOR,INIT_FLOOR
from globaltask import GlobalTask

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
        'current_floor out of range[%s:%s]'%(self.min_floor,self.max_floor)

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
        self.destination=0
        self.flag=0
        self.isalive=True

    def stop(self,):

        self.isalive=False

        ##stop之后会抹除destination,也可以选择不抹除，视需求而定
        self.flag=0

    @wapper_localtask
    def add_localtask(self,floor,refer='localtask'):
        ##上电梯内的人选择楼层
        ##在增加楼层的时候就确定本次电梯运行的终点
        ##add_localtask只会增加与其方向一致的路线

        if self.isalive:

            if self.flag==-1:

                if floor>=self.current_floor:
                    isaccept=False
                else:
                    isaccept=True
                    self.destination=min(self.destination,floor)

            elif self.flag==1:

                if floor<=self.current_floor:
                    isaccept=False
                   
                else:
                    isaccept=True
                    self.destination=max(self.destination,floor)

            elif self.flag==0:
                ##电梯未运行状态

                if floor>self.current_floor:
                    ##设置电梯为上行

                    self.flag=1
                    isaccept=True
                   

                elif floor<self.current_floor:
                    #设置电梯为下行

                    self.flag=-1
                    isaccept=True
                   


                elif floor==self.current_floor:
                    ##电梯保持原地不动

                    isaccept=False

                self.destination=floor

        
        else:
            ##电梯stop，不接受任何任务
            isaccept=False




        if isaccept:
            print u'elevator: %s accept the floor=%s you apply from %s'%(self.name,floor,refer)

            self.localtask.add(floor)
            
        else:
            print u'elevator: %s flag=%s,current_floor is %s,so cant accept the floor=%s you apply from %s'\
                %(self.name,self.flag,self.current_floor,floor,refer)

        return isaccept
        ##判断floor是否成功加入localtask


    def whether_open_by_local(self,):
        ##根据本地任务判断是否打开电梯门

        if self.current_floor in self.localtask:
            print u'open door for person who in elevator:%s,flag is %s,current_floor is %s,'\
            %(self.name,self.flag,self.current_floor)
            self.localtask.remove(self.current_floor)


            return True



    def run(self,):


        while True:

            try:

                if self.isalive:

                    if self.flag:
                        ##self.flag==-1 or self.flag==1
                        
                        while self.isalive:
                            # self.get_destination()

                            if self.flag==-1:
                                self.current_floor-=1
                            elif self.flag==1:
                                self.current_floor+=1

                            print u'elevator :%s flag=%s,current floor is %s'%(self.name,self.flag,self.current_floor)
                            isopen=self.whether_open_by_local()
                            if isopen:
                                print u' elevator:%s need open the door for people at %s floor,sleep 1 second'%(self.name,self.current_floor)
                                sleep(1)
                            else:
                                print u'elevator:%s sleep 0.2 second at %s floor '%(self.name,self.current_floor)
                                sleep(0.2)

                            if self.current_floor==self.destination:
                                print u'elevator:%s reach destination:%s,set flag=0'%(self.name,self.destination)
                                self.flag=0
                                break

                    else:

                        print u'elevator:%s does not have task,current_floor is:%s,sleep 2 second!'%(self.name,self.current_floor)
                        sleep(2)

                else:
                    ##电梯brenk
                    print u'elevator:%s is breaken,waiting for restart!!! '%(self.name)
                    sleep(10)

            except Exception,e:

                print e
                print u'catch except when elevator:%s runing'%(self.name)

                self.isalive=False
                print u'set elevator:%s isalive:%s'%(self.name,self.isalive)

                self.flag=0
                self.destination=0








def run(e):
    e1=e
    e1.add_localtask(8)
    e1.add_localtask(-6)
    e1.add_localtask(-3)
    e1.run()

if __name__ =='__main__':



    e1=Elevator(name='1')

    t1=Thread(target=apply_input,args=(e1,))
    t2=Thread(target=run,args=(e1,))
    t1.start()
    t2.start()

    t1.join()
    t2.join()
