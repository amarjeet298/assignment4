'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Author: Minh Ho , Amarjeet Singh
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
Apr 10th Revision 1:
    Update FCFS implementation, fixed the bug when there are idle time slices between processes
    Thanks Huang Lung-Chen for pointing out
Revision 2:
    Change requirement for future_prediction SRTF => future_prediction shortest job first(SJF), the simpler non-preemptive version.
    Let initial guess = 5 time units.
    Thanks Lee Wei Ping for trying and pointing out the difficulty & ambiguity with future_prediction SRTF.
'''
import sys

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrive_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    n = len(process_list)
    remTime =[]	
    schedule = []
    current_time = 0
    waiting_time = 0
    flag = 0
    #temporary array to stre remaining time		
    for process in process_list:
        remTime.append(process.burst_time)

    processed = set(); # set which keeps track of process to counter idle time
    process_queue = [0]
    counter = 0
    prev = counter
    while len(process_queue) != 0 :
        current = process_queue.pop(0)
        if(remTime[current] <= time_quantum and remTime[current] > 0 ):
            if (prev != current):
                schedule.append((current_time, process_list[current].id)) # append current time and process id
            current_time += remTime[current]
            remTime[current] = 0
            flag = 1 # done with processing
            processed.add(current)
        elif (remTime[current] > 0 ):
            if (prev != current):
                schedule.append((current_time, process_list[current].id)) # append current time and process id
            remTime[current] -= time_quantum
            current_time += time_quantum
        if (remTime[current] == 0 and flag == 1 ):  # check if process is completed then record the waiting time and set the flag to 0
            waiting_time +=  (current_time - process_list[current].arrive_time - process_list[current].burst_time)
            flag = 0
        while(counter < n-1 and (process_list[counter+1].arrive_time <= current_time) )  :
            counter =  counter + 1
            process_queue.append(counter)
        if(remTime[current] > 0):
            process_queue.append(current)
        if((len(processed) -1) == counter and len(processed) != n ):
            current_time = process_list[counter+1].arrive_time
            counter =  counter + 1
            process_queue.append(counter)
        prev = current
    average_waiting_time = waiting_time/float(n)
    return schedule, average_waiting_time		

def SRTF_scheduling(process_list):
    n = len(process_list)
    remTime =[]
    schedule = []
    current_time = 0
    waiting_time = 0
    flag = 0
    completed = 0
    minT =  999
    prev = 999
    #temporary array to stre remaining time
    for process in process_list:
        remTime.append(process.burst_time)

    while (completed != n):
        for j in range(n)  :
            if((process_list[j].arrive_time <= current_time )and remTime[j] <= minT and remTime[j] > 0) :
                minT = remTime[j]
                shortest = j
                flag = 1;

        if(flag ==0 ):
            current_time = current_time +1
            continue
        if (prev != shortest):
            schedule.append((current_time, process_list[shortest].id))

        remTime[shortest] = remTime[shortest] -1
        minT = remTime[shortest]
        current_time = current_time +1
        if(minT ==0 ):
            minT = 999

        if(remTime[shortest] == 0):
            completed = completed +1
            wt=  (current_time - process_list[shortest].arrive_time - process_list[shortest].burst_time)
            if(wt< 0 ):
                wt = 0
            waiting_time = waiting_time + wt
            flag = 0
        prev = shortest
    average_waiting_time = waiting_time/float(n)
    return schedule, average_waiting_time

def SJF_scheduling(process_list, alpha):
    return (["to be completed, scheduling SJF without using information from process.burst_time"],0.0)


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 4)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
	main(sys.argv[1:])
