# _*_ coding:utf-8 _*_ 

from config import MIN_FLOOR,MAX_FLOOR
from schedule import Schedule,FactoryElevator
from threading import Thread
from time import sleep
import random
from copy import deepcopy

def random_input(schedule,ts):
    ##模拟输入
    
    localtask=['l']*10
    globaltask=['g']*8
    addtask=['a']*2
    stoptask=['s']*1
    restarttask=['r']*2

    l=localtask+globaltask+addtask+stoptask+restarttask

    while True:

        elevators_count=schedule.get_elevators_count()
        flag=random.choice(l)

        if flag=='l':

            print u'choice add localtask'
            index=random.choice(range(elevators_count))
            floor=random.choice(range(MIN_FLOOR,MAX_FLOOR+1))
            elevator=schedule.elevators[index]
            print u'add localtask floor=%s to elevators[%s],elevator name is:%s'%(floor,index,elevator.name)
            schedule.add_localtask_by_elevator_index(index=int(index),floor=int(floor))


        elif flag=='g':
            print u'choice add new globaltask'
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
                add_elevator_to_ts(elevator,ts)
            else:

                print 'elevators count reacher max count'
                l.remove(flag)

        elif flag =='s':
            ##随机关闭一部电梯

            print u'you choice random close a elevator'
            elevator=random.choice(schedule.elevators)
            l.remove(flag)
            elevator.stop()

        elif flag =='r':

            print u'choice restart closed elevator'
            schedule.restart_elevator()

            


        print u'wait 1 second to accept new task'
        sleep(1)


def show_status(schedule):
    ##监控电梯系统

    while True:

        schedule.show_all_elevators_status()
        print u'wait 10 second reflash  elevator status'
        sleep(10)


def run_elevator(elevator):
    ##根据index启动电梯，也可以根据电梯名字，但没必要

    elevator.run()


def add_elevator_to_ts(elevator,ts):

    print u'create new Thread for elevator:%s'%(elevator.name)
    run=elevator.run
    name=u'Thread-elevator-%s'%(elevator.name)
    t=Thread(target=run,args=(),name=name)
    ts.append(t)








def main():

    schedule=Schedule()
    ts=[]
    t1=Thread(target=random_input,args=(schedule,ts),name='Thread-task')
    ##任务线程

    t2=Thread(target=show_status,args=(schedule,),name='Thread-monitoring')
    ##监控线程

  
    t1.start()
    t2.start()

    for elevator in schedule.elevators:

        name='Thread-elevator-%s'%(elevator.name)
        t=Thread(target=run_elevator,args=(elevator,),name=name)
        ts.append(t)


    broken_Thread=[]
    ##用以存储挂掉的电梯线程

    while True:
        ##用于监听是否有新电梯加入线程

        for t in ts:

            if t.is_alive():

                print u'%s is runing'%(t.name)

            else:
                print u'try start new elevator'

                try:
                    t.start()
                except:
                ##捕捉线程已经启动过，但任务结束的异常
                    print u'something wrong at: %s' %(t.name)

                    # ts.remove(t)
                    # print u'remove broken Thread:%s'%(t.name)

                    broken_list.apppend(t)
                    print u'apppend broken %s to broken_list'%(t.name)

                    ##线程结束了，对应的电梯无法启动了，那么需要开辟一个新的线程运行该电梯
                    for elevator in schedule.elevators:
                        name=u'Thread-elevator-%s'%elevator.name
                        if  name ==t.name:
                            add_elevator_to_ts(elevator,ts)
                            print u'apppend broken Thread:%s back to ts'%(t.name)
                            break


        sleep(10)






if __name__ =='__main__':


    main()