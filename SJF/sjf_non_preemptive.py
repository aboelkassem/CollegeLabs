def sort_processes(num_of_processes, main_list):
    swap_list = []
    viz = []
    for i in range(1000):
        viz.append(i)
        viz[i] = 0
    # sorting according  to least burst time
    for i in range(0, num_of_processes):
        c = i
        for j in range(i + 1, num_of_processes):
            if main_list[j][1] < main_list[c][1]:
                c = j
        if c != i:
            swap_list = main_list[c]
            main_list[c] = main_list[i]
            main_list[i] = swap_list

    list = []  # to store the new sorted elements
    end = []  # to store the finish time for each process
    last_time = 0
    cnt = 0  # the current number of picked elements
    # iterate over all elements and pick the suitable one 
    while cnt < num_of_processes:
        index = -1
        index2 = -1
        nearest = 1000
        for i in range(0, num_of_processes):
            # check if the arrival time of the ith process less than last_time
            if viz[i] == 0 and main_list[i][2] <= last_time:
                index = i
                break
            elif viz[i] == 0 and main_list[i][2] < nearest:  # else choose the nearest process
                nearest = main_list[i][2]
                index2 = i

        if index != -1:  # this means we find a ready process
            viz[index] += 1
            list.append(main_list[index])
            last_time += main_list[index][1]
            end.append(last_time)
        else:
            viz[index2] += 1
            list.append(main_list[index2])
            last_time = (nearest + main_list[index2][1])
            end.append(last_time)
        cnt += 1

    return list, end


def calculate_average_waiting(num_of_processes, wt):
    waiting_time = 0
    for i in range(num_of_processes):
        waiting_time += wt[i]
    return waiting_time / num_of_processes


def calculate_average_turn_around(num_of_processes, tt):
    turn_around = 0
    for i in range(num_of_processes):
        turn_around += tt[i]
    return turn_around / num_of_processes


def SJFNonPreemptive(num_of_processes, main_list):
    GanttChart = []
    wt = []
    tt = []
    List, end = sort_processes(num_of_processes, main_list)

    for i in range(0, num_of_processes):
        if i == 0:  # calculate the waiting time for each process
            wt.append(0)
        else:
            wt.append(max(0, end[i - 1] - List[i][2]))
        tt.append(end[i] - List[i][2])  # calculate the turn around for each process

    return List, wt, tt, end


def GanttOutput(NumOfProcesses, List, end):
    GanttChart = []

    for i in range(NumOfProcesses):  # build the gantt chart for processes
        for j in range(0, List[i][1]):
            GanttChart.append(List[i][0])

    qu = []  # store the time of each process
    for i in range(NumOfProcesses):
        for j in range(end[i] - List[i][1], end[i]):
            qu.append(j)
    first_line = "|"
    above_line = "_"
    under_line = "‾"
    second_line = ""
    for i in range(0, len(GanttChart)):
        first_line = first_line + "P" + str(GanttChart[i]) + "|"
        if qu[i] < 10:
            second_line = second_line + "  " + str((qu[i]))
        else:
            second_line = second_line + " " + str((qu[i]))

    back = qu[len(qu) - 1] + 1
    if back < 10:
        second_line = second_line + "  " + str(back)
    else:
        second_line = second_line + " " + str(back)
    for i in range(1, len(first_line)):
        under_line += "‾"
        above_line += "_"
    second_line = second_line.replace(' ', '', 2)
    print(above_line + "\n" + first_line + "\n" + under_line + "\n" + second_line)


def run(burst_time_list, num_of_processes):
    List, wt, tt, end = SJFNonPreemptive(num_of_processes, burst_time_list)

    print("\n Process ID \t Burst Time \t Arrival Time \t Waiting Time \t Turnaround Time")
    for i in range(num_of_processes):
        print(
            str(List[i][0]) + "\t\t\t\t" + str(List[i][1]) + "\t\t\t\t" + str(List[i][2]) + "\t\t\t\t" + str(
                wt[i]) + "\t\t\t\t" + str(tt[i]) + "\n")
    print("GanttChart :")
    GanttOutput(num_of_processes, List, end)
    print("waiting time = ", calculate_average_waiting(num_of_processes, wt))
    print("Turn Around time = ", calculate_average_turn_around(num_of_processes, tt))
