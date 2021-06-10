from sjf_preemptive import find_avg_time
from sjf_non_preemptive import run

if __name__ == "__main__":

    select = 0
    while True:
        print('Select the number of which algorithm do you need!......')
        print('1- Shortest Job First (SJF) preemptive')
        print('2- Shortest Job First (SJF) non-preemptive')
        select = int(input("Algorithm Number: "))
        if select == 1 or select == 2:
            break
        else:
            print('Invalid Input Number, you have to select only 1 or 2...')
            print('------------------------------------------------------')
            continue

    NumOfProcesses = int(input("Enter the number of processes: "))
    BurstTimeList = []
    for i in range(0, NumOfProcesses):
        newList = []
        x = int(input("Enter the id for process " + str(i+1) + " : "))
        newList.append(x)
        x = int(input("Enter the burst time for process " + str(i+1) + " : "))
        newList.append(x)
        x = int(input("Enter the arrival time for process " + str(i+1) + " : "))
        newList.append(x)
        BurstTimeList.append(newList)

    if select == 1:
        find_avg_time(BurstTimeList, NumOfProcesses)
    elif select == 2:
        run(BurstTimeList, NumOfProcesses)
