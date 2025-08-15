//
//  main.c
//  Assignment3
//
//  Created by Andre Grigorian on 4/7/24.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RESOURCES 100
#define MAX_PROCESSES 100

int resources[MAX_RESOURCES];
int available[MAX_RESOURCES];
int max_claim[MAX_PROCESSES][MAX_RESOURCES];
int allocated[MAX_PROCESSES][MAX_RESOURCES];
int need[MAX_PROCESSES][MAX_RESOURCES];
int num_res, num_proc;

void create_claim_graph();
void request_resource();
void release_resource();
void determine_safe_sequence();
void update_need();
int find_safe_sequence(int []);
void print_state();







int main(int argc, const char * argv[]) {

    int choice;
    do{
        printf("Banker's Algorithm\n------------------\n");
        printf("1) Enter claim graph\n");
        printf("2) Request resource\n");
        printf("3) Release resource\n");
        printf("4) Determine safe sequence\n");
        printf("5) Quit program\n");
        printf("\nEnter selection: ");
        scanf("%d", &choice);
        
        switch(choice){
            case 1:
                create_claim_graph();
                print_state();
                break;
            case 2:
                request_resource();
                print_state();
                break;
            case 3:
                release_resource();
                print_state();
                break;
            case 4:
                determine_safe_sequence();
                break;
            case 5:
                printf("Quitting program...\n");
                break;
            default:
                printf("Invalid selection. \n");
                break;
        }
    }while(choice != 5);
    
    return 0;
}


void create_claim_graph(){
    printf("Enter number of resources: ");
    scanf("%d", &num_res);
    printf("Enter number of units for resources (r0 to r%d): ", num_res-1);
    for (int i = 0; i < num_res; i++) {
        scanf("%d", &resources[i]);
        available[i] = resources[i];
    }
    printf("Enter number of processes: ");
    scanf("%d", &num_proc);
    for(int i = 0; i<num_proc; i++){
        printf("Enter maximum number of units process p%d will claim from each resource (r0 to r%d): ", i, num_res-1);
        for (int j = 0; j < num_res; j++) {
            scanf("%d", &max_claim[i][j]);
        }
    }
    for(int i = 0; i<num_proc; i++){
        printf("Enter number of units of each resource (r0 to r%d) currently allocated to process p%d: ", num_res-1, i);
        for (int j = 0; j < num_res; j++) {
            scanf("%d", &allocated[i][j]);
            available[j] -= allocated[i][j];
        }
    }
    
    update_need();
}

void request_resource() {
    char p_input[100], r_input[100];
    int p_index, r_index;
    
    int process, resource, units;
    printf("Enter requesting process (p0 to p%d): ", num_proc - 1);
    scanf("%s", p_input);
    sscanf(p_input, "p%d", &p_index);
    printf("Enter requested resource (r0 to r%d): ", num_res - 1);
    scanf("%s", r_input);
    sscanf(r_input, "p%d", &r_index);
    printf("Enter number of units process %d is requesting from resource r%d: ", process, resource);
    scanf("%d", &units);

    if (units <= need[process][resource] && units <= available[resource]) {
        allocated[process][resource] += units;
        available[resource] -= units;
        need[process][resource] -= units;
    } else {
        printf("Request cannot be granted.\n");
    }
}

void release_resource() {
    char p_input[100], r_input[100];
    int p_index, r_index;
    
    int process, resource, units;
    printf("Enter releasing process (p0 to p%d): ", num_proc - 1);
    scanf("%s", p_input);
    sscanf(p_input, "p%d", &p_index);
    printf("Enter released resource (r0 to r%d): ", num_res - 1);
    scanf("%s", r_input);
    sscanf(r_input, "p%d", &r_index);
    printf("Enter number of units process %d is releasing from resource r%d: ", process, resource);
    scanf("%d", &units);

    if (units <= allocated[process][resource]) {
        allocated[process][resource] -= units;
        available[resource] += units;
        need[process][resource] += units;
    } else {
        printf("Cannot release more units than allocated.\n");
    }
}

void determine_safe_sequence() {
    int work[MAX_RESOURCES];
    memcpy(work, available, sizeof(available));
    int finish[MAX_PROCESSES] = {0};

    if (find_safe_sequence(work)) {
        printf("System is in a safe state.\n");
    } else {
        printf("System is NOT in a safe state.\n");
    }
}

int find_safe_sequence(int work[]) {
    int finish[MAX_PROCESSES] = {0}, safe_seq[MAX_PROCESSES], count = 0;

    while (count < num_proc) {
        int found = 0;
        for (int i = 0; i < num_proc; i++) {
            if (!finish[i]) {
                printf("Comparing: < ");
                for (int j = 0; j < num_res; j++) {
                    printf("%d ", need[i][j]);
                }
                printf("> <= < ");
                for (int j = 0; j < num_res; j++) {
                    printf("%d ", work[j]);
                }
                printf("> : ");

                int j;
                for (j = 0; j < num_res; j++)
                    if (need[i][j] > work[j])
                        break;

                if (j == num_res) {
                    for (int k = 0; k < num_res; k++)
                        work[k] += allocated[i][k];
                    safe_seq[count++] = i;
                    finish[i] = 1;
                    found = 1;
                    printf("Process p%d can be sequenced\n", i);
                } else {
                    printf("Process p%d cannot be sequenced\n", i);
                }
            }
        }

        if (!found) {
            printf("No safe sequence found.\n");
            return 0; // Return failure if no process can be added to the safe sequence
        }
    }

    printf("Safe sequence of processes:");
    for (int i = 0; i < count; i++)
        printf(" p%d", safe_seq[i]);
    printf("\n");
    return 1; // Return success if a safe sequence is found
}



void update_need() {
    for (int i = 0; i < num_proc; i++) {
        for (int j = 0; j < num_res; j++) {
            need[i][j] = max_claim[i][j] - allocated[i][j];
        }
    }
}

void print_state() {
    
    printf("\nResources:\n");
    for (int i = 0; i < num_res; i++) {
        printf("\tr%d", i);
    }
    printf("\n\t");
    for (int i = 0; i < num_res; i++) {
        printf("%d\t", resources[i]);
    }

    printf("\n");
    
    printf("\nAvailable:\n");
    for (int i = 0; i < num_res; i++) {
        printf("\tr%d", i);
    }
    printf("\n\t");
    for (int i = 0; i < num_res; i++) {
        printf("%d\t", available[i]);
    }

    printf("\n");
    
    printf("\nMax Claim:\n");
    for (int i = 0; i < num_res; i++) {
        printf("\tr%d", i);
    }
    printf("\n\t");
    for (int i = 0; i < num_proc; i++) {
        printf("p%d\t", i);
        for (int j = 0; j < num_res; j++) {
            printf("%d\t", max_claim[i][j]);
        }
        printf("\n");
    }

    printf("\n");

    printf("Allocated:\n");
    for (int i = 0; i < num_res; i++) {
        printf("\tr%d", i);
    }
    printf("\n\t");
    for (int i = 0; i < num_proc; i++) {
        printf("p%d\t", i);
        for (int j = 0; j < num_res; j++) {
            printf("%d\t", allocated[i][j]);
        }
        printf("\n");
    }

    printf("\n");

    printf("Need:\n");
    for (int i = 0; i < num_res; i++) {
        printf("\tr%d", i);
    }
    printf("\n\t");
    for (int i = 0; i < num_proc; i++) {
        printf("p%d\t", i);
        for (int j = 0; j < num_res; j++) {
            printf("%d\t", need[i][j]);
        }
        printf("\n");
    }
    
    printf("\n");
}
