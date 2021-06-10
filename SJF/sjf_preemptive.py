def find_waiting_time(processes, n, wt):
    burst_times = [0] * n

    # put all burst_times of processes in list
    for i in range(n):
        burst_times[i] = processes[i][1]

    complete = 0
    time = 0
    minimum = 999999999  # minimum burst time
    short = 0            # the smallest process
    check = False        # to know this process ended or no

    # Process until all processes gets
    # completed >> when complete = num_of_processes
    while complete != n:
        # to determine the minimum burst time && the smallest process &&
        for j in range(n):
            # if arrival time at [j] less than or equal time &&
            # burst_times at [j] less than minimum &&
            # burst_times at [j] more than 0
            if (processes[j][2] <= time) and (burst_times[j] < minimum) and burst_times[j] > 0:
                minimum = burst_times[j]
                short = j
                check = True

        if not check:
            time += 1
            continue

        # Reduce remaining time by one
        burst_times[short] -= 1

        # Update minimum
        minimum = burst_times[short]
        if minimum == 0:
            minimum = 999999999

        # If a process gets completely
        # executed
        if burst_times[short] == 0:

            # Increment complete
            complete += 1
            check = False

            finish_time_of_current_process = time + 1

            # Calculate waiting time
            wt[short] = (finish_time_of_current_process - processes[short][1] -
                         processes[short][2])

            if wt[short] < 0:
                wt[short] = 0

        # Increment time
        time += 1


# Function to calculate turn around time
def find_turn_around_time(processes, n, wt, tat):
    # Calculating turnaround time
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]


# and turn-around times.
def find_avg_time(processes, n):
    waiting_time = [0] * n
    turn_around_time = [0] * n

    # Function to find waiting time
    # of all processes
    find_waiting_time(processes, n, waiting_time)

    # Function to find turn around time
    # for all processes
    find_turn_around_time(processes, n, waiting_time, turn_around_time)

    # Display processes along with all details
    print("Processes    Burst Time     Waiting", "Time     Turn-Around Time")
    total_waiting_time = 0
    total_around_time = 0
    for i in range(n):
        total_waiting_time = total_waiting_time + waiting_time[i]
        total_around_time = total_around_time + turn_around_time[i]
        print(" ", processes[i][0], "\t\t",
              processes[i][1], "\t\t\t\t",
              waiting_time[i], "\t\t\t\t", turn_around_time[i])

    print("\nAverage waiting time = %.5f " % (total_waiting_time / n))
    print("Average turn around time = ", total_around_time / n)