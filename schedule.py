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
        ##add_globaltask_to_localtask
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




def accept_input(schedule):

    while True:
        flag=raw_input('input "l" run add_localtask,input "g" run add_globaltask:')

        if flag=='l':

            index=raw_input(u'choose which evevator you want add localtask:')
            floor=raw_input(u'which gloor you want reacher:')

            schedule.add_localtask_by_elevator_index(index=int(index),floor=int(floor))

        elif flag=='g':

            flag=raw_input(u'choose which flag you want add globaltask:')
            floor=raw_input(u'which gloor you want reacher:')
            schedule.add_globaltask_with_flag(floor=int(flag),flag=int(flag))

        schedule.add_globaltask_to_localtask()

        sleep(1)

def random_input(schedule,ts):

    # elevators_count=schedule.get_elevators_count()
    ##模拟输入
    
    # l=['l','g','L','G','l','l','g','L','G','l','l','g','L','G','l','a','s']
    l=['l','g','a','s']

    while True:
        elevators_count=schedule.get_elevators_count()
        flag=random.choice(l)
        print u'current choice l is:%s'%l
        if flag=='l':

            index=random.choice(range(elevators_count))
            floor=random.choice(range(MIN_FLOOR,MAX_FLOOR+1))
            print u'add localtask floor=%s to elevators[%s]'%(floor,index)
            schedule.add_localtask_by_elevator_index(index=int(index),floor=int(floor))


        elif flag=='g':

            flag=random.choice([-1,1])
            floor=random.choice(range(MIN_FLOOR,MAX_FLOOR+1))
            print u'add flag=%s ,floor=%s to globaltask'%(flag,floor)
            schedule.add_globaltask_with_flag(flag=int(flag),floor=int(floor))
            schedule.add_globaltask_to_localtask()

        elif flag=='a':

            print u'choice add new elevator'
            if FactoryElevator.count<6:
                elevator=schedule.add_elevator()
                print u'current elevators count is:%s'%(FactoryElevator.count)

                run=elevator.run
                t=Thread(target=run,args=())
                ts.append(t)
                print u'add new elevator:%s to ts'%(elevator.name)
            else:

                print 'elevators count reacher max count'
                l.remove(flag)

        elif flag =='s':
            ##随机关闭一部电梯

            print u'you choice random close a elevator'
            elevator=random.choice(schedule.elevators)
            l.remove(flag)
            elevator.stop()
            


        print u'wait 1 second to accept new task'
        sleep(1)


def show_status(schedule):
    ##监控电梯系统

    while True:

        schedule.show_all_elevators_status()
        print u'wait 10 second reflash  elevator status'
        sleep(10)


def run_elevator(schedule,index):
    ##根据index启动电梯，也可以根据电梯名字，但没必要
    while True:
        schedule.elevators[index].run()


def add_elevator(schedule,ts):
    ##增加一部电梯

    elevator=schedule.add_elevator()
    run=elevator.run
    t=Thread(target=run,args=())
    ts.append(t)

def restart_elevator(schedule,name=None):
    ##重启电梯

    count=0
    while True:

        schedule.restart_elevator(name=name)
        sleep(60)
        print u'sleep 60 second wait for stop elevator'
        count+=1

        if count==10:
            print u'wont check stop elevator any more'
            break



def main():

    schedule=Schedule()
    elevators_count=schedule.get_elevators_count()
    ts=[]
    t1=Thread(target=random_input,args=(schedule,ts))
    ##任务线程
    t2=Thread(target=show_status,args=(schedule,))
    ##监控线程

    t3=Thread(target=restart_elevator,args=(schedule,))
    # ##重启线程

    t1.start()
    t2.start()
    t3.start()

    for i in range(elevators_count):

        t=Thread(target=run_elevator,args=(schedule,i))

        ts.append(t)


    while True:
        ##用于监听是否有新电梯加入线程


        for t in ts:

            if t.is_alive():

                print u'ts["%s"] is runing'%(t.name)

            else:
                print u'start new Thread for  new elevator'
                t.start()

        sleep(10)








def test():
    elevators=[FactoryElevator.add_elevator() for i in range(5)]
    print FactoryElevator.count


if __name__ =='__main__':

    # test()
    main()


