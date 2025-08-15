//
//  main.c
//  Assignment2
//
//  Created by Andre Grigorian on 3/10/24.
//
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>


typedef struct {
    int id;
    int arrival;
    int total_cpu;
    int total_remaining;
    int done;
    int start_time;
    int already_started;
    int end_time;
    int turnaround_time;
} Process;

int num_processes = 0;
Process* processes = NULL;

void init_parameters(){
    printf("Enter total number of processes: ");
    scanf("%d", &num_processes);
    processes = (Process*)malloc(num_processes * sizeof(Process));
    for(int i = 0; i < num_processes; i++){
        printf("Enter arrival cycle for process %d: ", i+1);
        scanf("%d", &processes[i].arrival);
        printf("Enter total cycle for process %d: ", i+1);
        scanf("%d", &processes[i].total_cpu);
        processes[i].total_remaining = processes[i].total_cpu;
        processes[i].done = 0;
        processes[i].already_started = 0;
        processes[i].id = i+1;
    }
}

void sort_processes_by_arrival(){ //sort from earliest arrival to latest
    
    for(int i = 0; i<num_processes; i++){
        int max_arrival = processes[i].arrival;
        int max_arrival_index = i;
        for(int j = 0; j<num_processes-i; j++){
            if(processes[j].arrival < max_arrival){
                max_arrival = processes[j].arrival;
                max_arrival_index = j;
            }
        }
        //place max at the end
        Process temp = processes[num_processes-i-1];
        processes[num_processes-i-1] = processes[max_arrival_index];
        processes[max_arrival_index] = temp;
    }
}

void sort_processes_by_total_cpu(){ //sort from least to most
    
    for(int i = 0; i<num_processes; i++){
        int max_cpu = processes[i].arrival;
        int max_cpu_index = i;
        for(int j = 0; j<num_processes-i; j++){
            if(processes[j].total_cpu < max_cpu){
                max_cpu = processes[j].total_cpu;
                max_cpu_index = j;
            }
        }
        
        //place max at the end
        Process temp = processes[num_processes-i-1];
        processes[num_processes-i-1] = processes[max_cpu_index];
        processes[max_cpu_index] = temp;
    }
}



void sched_w_fifo(){
    sort_processes_by_arrival();
    int current_time = 0;
    for(int i = 0;i<num_processes; i++){
        if(current_time < processes[i].arrival){
            current_time = processes[i].arrival;
        }
        processes[i].start_time = current_time;
        current_time += processes[i].total_cpu;
        processes[i].end_time = current_time;
        processes[i].turnaround_time = processes[i].end_time - processes[i].arrival;
    }
}


void sched_w_sjf(){
    sort_processes_by_total_cpu();
    int currentTime = 0, executedProcesses = 0;
    while(executedProcesses < num_processes) {
        // Find the process with the shortest total_cpu time
        int shortestJobIndex = -1;
        int shortestTime = INT_MAX;
        for (int i = 0; i < num_processes; i++) {
            if (processes[i].arrival <= currentTime && !processes[i].done && processes[i].total_cpu < shortestTime) {
                shortestTime = processes[i].total_cpu;
                shortestJobIndex = i;
            }
        }

        if (shortestJobIndex == -1) {
            currentTime++;
            continue;
        }

        Process *p = &processes[shortestJobIndex];

        if (p->start_time == -1) {
            p->start_time = currentTime;
        }

        currentTime += p->total_cpu;
        p->end_time = currentTime;
        p->turnaround_time = p->end_time - p->arrival;
        p->done = 1;
        executedProcesses++;
    }
}

void sched_w_srt() {
    int currentTime = 0, completedProcesses = 0;
    int shortestRemainingTime, index;

    
    for (int i = 0; i < num_processes; i++) {
        processes[i].total_remaining = processes[i].total_cpu;
        processes[i].start_time = -1;
    }

    while (completedProcesses < num_processes) {
        shortestRemainingTime = INT_MAX;
        index = -1;

        // Find the process with the shortest remaining time that has arrived
        for (int i = 0; i < num_processes; i++) {
            if (processes[i].arrival <= currentTime && processes[i].total_remaining < shortestRemainingTime && processes[i].total_remaining > 0) {
                shortestRemainingTime = processes[i].total_remaining;
                index = i;
            }
        }

        if (index == -1) {
            currentTime++;
            continue;
        }

        if (processes[index].start_time == -1) {
            processes[index].start_time = currentTime;
        }

        processes[index].total_remaining--;
        currentTime++;
        
        if (processes[index].total_remaining == 0) {
            completedProcesses++;
            processes[index].end_time = currentTime;
            processes[index].turnaround_time = processes[index].end_time - processes[index].arrival;
        }
    }
}



void print_table(){
    printf("PID Arrival Total Start End Turnaround\n");
    printf("--------------------------------------------------\n");
    for (int i = 0; i < num_processes; i++) {
        printf("%d    %d        %d      %d      %d    %d\n",
               processes[i].id,
               processes[i].arrival,
               processes[i].total_cpu,
               processes[i].start_time,
               processes[i].end_time,
               processes[i].turnaround_time);
    }
}

void quit(){
    free(processes);
    processes = NULL;
    printf("Quitting program\n");
}

int main(int argc, const char * argv[]) {
    int choice;
    do{
        printf("Batch scheduling\n----------------\n");
        printf("1) Enter Parameters\n");
        printf("2) Schedule processes with FIFO algorithm\n");
        printf("3) Schedule processes with SJF algorithm\n");
        printf("4) Schedule processes with SRT algorithm\n");
        printf("5) Quit program and free memory\n");
        printf("\nEnter selection: ");
        scanf("%d", &choice);
        
        switch(choice){
            case 1:
                init_parameters();
                print_table();
                break;
            case 2:
                sched_w_fifo();
                print_table();
                break;
            case 3:
                sched_w_sjf();
                print_table();
                break;
            case 4:
                sched_w_srt();
                print_table();
                break;
            case 5:
                quit();
                break;
            default:
                printf("Invalid selection. \n");
                break;
        }
    }while(choice != 5);
    
    return 0;
}
