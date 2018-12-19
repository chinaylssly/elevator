# _*_ coding:utf-8 _*_ 
from elevator import Elevator
from globaltask import GlobalTask
from threading import Thread
from config import MAX_FLOOR

class FactoryElevator(object):

    count=0

    @classmethod
    def add_elevator(cls,):
        cls.count+=1
        return Elevator(name=cls.count)

   

class Schedule(Thread):

    def __init__(self,count=3):

        Thread.__init__(self)

        self.elevators=[FactoryElevator.add_elevator() for i in range(count)]
        self.GlobalTask=GlobalTask

    def __new__(cls,):
        ##单例模型

        if hasattr(cls,'instance'):

            print u'Schedule has been instance'

        else:

            cls.instance=Thread.__new__(cls)

        return cls.instance




    def add_globaltask_to_localtask(self,):
        ##add_globaltask_to_localtask
            
        exigency_up=GlobalTask.task['exigency_up']
        flagdict={'exigency_up',1,'up':1,'exigency_down'=-1,'down':-1}

        for key,value in GlobalTask.task.items():

            for floor in value:

                distancelist=[]
                for index,elevator in enumeration(elevators):

                    task_flag=flagdict[key]

                    if elevator.flag==task_flag:

                        distance=floor-evevator.current_floor

                        if elevator.flag ==1:
                            ##电梯向上运动

                            if distance>=0:
                                pass
                            else:
                                distance=elevator.destination - elevator.current_floor + elevator.destination - floor

                        elif elevator.flag ==-1:
                            ##电梯向下运动

                            if distance<=0:
                                distance=abs(distance)

                            else:
                                distance=elevator.current_floor - elevator.destination + floor - elevator.destination

                    elif elevator.flag ==1 and task_flag==-1:

                        distance=elevator.destination - elevator.current_floor + abs(elevator.destination - floor)

                    elif elevator.flag ==-1 and task_flag==1:

                        distance=elevator.current_floor - elevator.destination + abs(floor - elevator.destination)

                    elif elevator.flag ==0:

                        distance=abs(elevator.current_floor - floor)


                    distancelist.append(distance)

                min_distance=min(distancelist)


                index=distancelist.index(min_distance)
                elevator=elevators[index]
                isaccept=elevator.add_localtask(floor=floor)

                if isaccept:
                    ##有电梯接受了globaltask中的楼层申请，从globaltask中移除
                    globaltask[key].remove(floor)
                    print u'elevator:%s accept globaltask flag=%s,floor=%s'%(elevator.name,key,floor)

                else:
                    ##所有的电梯都与globaltask中的任务冲突，即任务没有被接受，暂留globaltask
                    print u'no elevator accept globaltask flag=%s,floor=%s'%(key,floor)











       






        




def test():
    elevators=[FactoryElevator.add_elevator() for i in range(5)]
    print FactoryElevator.count


if __name__ =='__main__':

    test()


