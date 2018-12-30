# _*_ coding:utf-8 _*_ 
from elevator import Elevator
from globaltask import GlobalTask
from threading import Thread
from config import MAX_FLOOR,MIN_FLOOR
from time import sleep
import random
from copy import deepcopy

class FactoryElevator(object):

    count=0

    @classmethod
    def add_elevator(cls,):
        cls.count+=1
        return Elevator(name=cls.count)

   

class Schedule(object):

    def __init__(self,count=3):

        self.elevators=[FactoryElevator.add_elevator() for i in range(count)]
        self.GlobalTask=GlobalTask

    def __new__(cls):
        ##单例模型

        if hasattr(cls,'instance'):
            print u'Schedule exists instance'

        else:
            cls.instance=object.__new__(cls)
        return cls.instance


    def analyze_distance(self,elevator,task_flag,floor):
        ##计算任务与电梯距离

        if elevator.isalive:

            if elevator.flag==1 :

                if floor>=elevator.destination:
                    distance=floor - elevator.current_floor

                elif floor < elevator.destination and floor >= elevator.current_floor:
                    if task_flag==1:
                        distance=floor - elevator.current_floor

                    else:
                        # distance=elevator.destination  - elevator.current_floor + elevator.destination - floor
                        distance=MAX_FLOOR*2
                else:
                    # distance=elevator.destination  - elevator.current_floor + elevator.destination - floor
                    distance=MAX_FLOOR*2

            elif elevator.flag==0:
                distance=abs(elevator.current_floor - floor)

            else:
                ## elevator.flag==-1

                if floor >=elevator.current_floor:
                    # distance=elevator.current_floor - elevator.destination + floor - elevator.destination
                    distance=MAX_FLOOR*2

                elif floor <=elevator.destination:
                    distance= elevator.current_floor - floor

                else:
                    if task_flag ==-1:
                        distance = elevator.current_floor - floor

                    else:
                        # distance = elevator.current_floor - elevator.destination + floor - elevator.destination
                        distance=MAX_FLOOR*2

        else:
            ##elevator已关闭

            print u'%s already stop'%(elevator)
            distance=MAX_FLOOR*2

        return distance


    def add_globaltask_to_localtask(self,):
        ##任务分配算法
            
        flagdict={'exigency_up':1,'up':1,'exigency_down':-1,'down':-1}
        print u'analyze the best blue print!'

        ##deepcopy一个globaltask的副本，集合和字典在遍历的时候不能被修改
        tempdict=deepcopy(GlobalTask.task)

        for key,value in tempdict.items():

            task_flag=flagdict.get(key)
            for floor in value:

                distancelist=[]
                for elevator in self.elevators:

                    distance=self.analyze_distance(elevator=elevator,task_flag=task_flag,floor=floor)
                    distancelist.append(distance)

                print u'GlobalTask.task["%s"]=%s distancelist is %s'%(key,floor,distancelist)
                min_distance=min(distancelist)

                if min_distance==MAX_FLOOR*2:
                    ##所有电梯的运行进度与任务都不一致

                    isaccept=False

                else:

                    index=distancelist.index(min_distance)
                    elevator=self.elevators[index]
                    isaccept=elevator.add_localtask(floor=floor,refer='globaltask')

                ##调度还会出现一个问题，提交了相同任务多次，可能会导致同一个任务会被分配到多个电梯中，这是无法避免的，也无需优化
                if isaccept:
                    ##有电梯接受了globaltask中的楼层申请
                    print u'%s accept globaltask flag=%s,floor=%s'%(elevator,key,floor)
                  
                else:
                    ##所有的电梯运行状态都与globaltask中的任务冲突，即任务没有被接受，暂留任务于globaltask
                    print u'no elevator accept globaltask flag=%s,floor=%s,this task is invalid'%(key,floor)

                self.GlobalTask.task[key].remove(floor)
                print u'remove %s from GlobalTask.task["%s"]'%(floor,key)




    def add_localtask_by_elevator_index(self,index,floor):
        ##向电梯添加本地任务

        if index < len(self.elevators):
            self.elevators[index].add_localtask(floor=floor,refer='localtask')

        else:
            print 'elevator:%s dont exists'%(index+1)

    def stop_elevator_by_index(self,index,):
        ##用于关闭电梯

        elevator=self.elevators[index]
        elevator.stop()
        print u'close elevator:%s,set isalive to False'%(elevator.name)


    def add_globaltask_with_flag(self,floor,flag):
        ##添加全局任务

        if flag == 1:
            self.GlobalTask.add_up(floor=floor)

        elif flag == -1:
            self.GlobalTask.add_down(floor=floor)

    def add_elevator(self,):
        ##增加电梯

        elevator=FactoryElevator.add_elevator()
        self.elevators.append(elevator)
        return elevator

    def get_elevators_count(self,):
        ##查看电梯数目

        return FactoryElevator.count
        return len(self.elevators)


    def restart_elevator(self,name=None):
        ##重启关闭的电梯
        print u'try restart all stop elevator'
        for elevator in self.elevators:
            ##已启动的电梯不受影响

            if name is None: 
                if elevator.isalive is False:  
                    elevator.restart()
        
            else:
                if elevator.name == name:
                    elevator.restart()


    def show_all_elevators_status(self,):

        print u'--------------------------------'
        print u'--------------------------------'
        print u'current elevators count is : %s'%(FactoryElevator.count)

        for elevator in self.elevators:

            if elevator.isalive:

                if elevator.flag == 0:

                    print u'%s is empty,task is: %s'%(elevator,elevator.localtask)
                    print 

                else:

                    print u'%s is runing,task is: %s'%(elevator,elevator.localtask)
                    print 

            else:

                print u'%s already broken, task is: %s'%(elevator,elevator.localtask)
                print 

        for key,value in GlobalTask.task.items():

            print u'GlobalTask.task["%s"] is %s'%(key,value)

        print u'--------------------------------'
        print u'--------------------------------'



def test():
    elevators=[FactoryElevator.add_elevator() for i in range(5)]
    print FactoryElevator.count


if __name__ =='__main__':

    test()


