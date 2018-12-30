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

        flag=random.choice(l)

        if flag=='l':

            print u'choice add localtask'
            elevator=random.choice(schedule.elevators)
            floor=random.choice(range(MIN_FLOOR,MAX_FLOOR+1))
            print u'add localtask floor=%s to %s'%(floor,elevator)
            elevator.add_localtask(floor=floor)


        elif flag=='g':

            print u'choice add globaltask'
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
                add_elevator(elevator,ts)

            else:
                print 'elevators count reach max count'
                l.remove(flag)

        elif flag =='s':
            ##随机关闭一部电梯

            print u'you choice random close a elevator'
            elevator=random.choice(schedule.elevators)
            l.remove(flag)
            elevator.stop()

        elif flag =='r':
            ##重启电梯

            print u'choice restart closed elevator'
            schedule.restart_elevator()


        print u'wait 0.2 second to accept new task'
        sleep(0.2)


def show_status(schedule):
    ##监控电梯系统

    while True:

        schedule.show_all_elevators_status()
        print u'wait 10 second reflash  elevator status'
        sleep(10)


def run_elevator(elevator):
    ##根据index启动电梯，也可以根据电梯名字，但没必要

    while True:
        elevator.run()


def add_elevator(elevator,ts):

    print u'create new Thread for elevator:%s'%(elevator.name)
    name=u'Thread-elevator-%s'%(elevator.name)
    t=Thread(target=run_elevator,args=(elevator,),name=name)
    ts.append(t)
    t.start()






def main():

    schedule=Schedule()

    ts=[]
    ##存放电梯运行的线程

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


    

    while True:
        ##用于监听是否有运行中的电梯线程挂掉

        broken_list=[]
         ##用于存放挂掉的线程

        for t in ts:

            if t.is_alive():

                print u'%s is alive'%(t.name)

            else:
                print u'%s is broken'%(t.name)
                broken_list.append(t)

                ##线程结束了，对应的电梯就无法启动了，那么需要开辟一个新的线程运行该电梯
                for elevator in schedule.elevators:
                    name=u'Thread-elevator-%s'%elevator.name
                    if  name ==t.name:
                        add_elevator(elevator,ts)
                        print u'apppend broken Thread:%s back to ts'%(t.name)
                        break

        for t in broken_list:
            if t in ts:
                ts.remove(t)
                ##从ts中移除挂掉的线程

        sleep(10)




if __name__ =='__main__':


    main()