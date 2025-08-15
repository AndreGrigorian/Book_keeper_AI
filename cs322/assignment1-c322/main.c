//Andre Grigorian

#include <stdio.h>
#include <stdlib.h>

#define MAX_PROCESSES 100

typedef struct Node {
    int childID;
    struct Node* next;
} Node;

typedef struct {
    int parent;
    Node* children;
} PCB;

PCB pcbArray[MAX_PROCESSES];
int processCount = 0;

//  function prototyps
void initializeProcessHierarchy();
void createChildProcess();
void destroyDescendants(int p);
void displayProcessList();
void freeMemory();
Node* createNode(int childID);
void freeChildList(Node* head);

int main() {
    int choice;
    initializeProcessHierarchy();
    do {
        printf("--------------------------------\n");
        printf("1) Initialize process hierarchy\n");
        printf("2) Create a new child process\n");
        printf("3) Destroy all descendants of a process\n");
        printf("4) Quit program and free memory\n");
        printf("Enter selection: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                initializeProcessHierarchy();
                break;
            case 2:
                createChildProcess();
                break;
            case 3:
                printf("Enter the parent process whose descendants are to be destroyed: ");
                int parentId;
                scanf("%d", &parentId);
                destroyDescendants(parentId);
                break;
            case 4:
                freeMemory();
                printf("Quitting program...\n");
                break;
            default:
                printf("Not a choice \n");
        }
        displayProcessList();
    } while (choice != 4);

    return 0;
}

void initializeProcessHierarchy() {
    processCount = 1;
    for (int i = 0; i < MAX_PROCESSES; i++) {
        pcbArray[i].parent = -1;
        pcbArray[i].children = NULL;
    }
    pcbArray[0].parent = 0;
}

void createChildProcess() {
    if (processCount >= MAX_PROCESSES) {
        printf("Max processes reached.\n");
        return;
    }

    int parentId;
    printf("Enter the parent process id: ");
    scanf("%d", &parentId);

    if (parentId < 0 || parentId >= processCount) {
        printf("Process id out of bounds.\n");
        return;
    }

    int childId = processCount++;
    pcbArray[childId].parent = parentId;
    Node* newNode = createNode(childId);
    newNode->next = pcbArray[parentId].children;
    pcbArray[parentId].children = newNode;

}

void destroyDescendants(int p) {
    Node* current = pcbArray[p].children;
    while (current != NULL) {
        int childID = current->childID;
        destroyDescendants(childID);
        current = current->next;
        free(pcbArray[childID].children);
        pcbArray[childID].children = NULL;
        pcbArray[childID].parent = -1;
    }
    freeChildList(pcbArray[p].children);
    pcbArray[p].children = NULL;
}

void displayProcessList() {
    printf("Process list:\n");
    for (int i = 0; i < processCount; i++) {
        if (pcbArray[i].parent != -1) {
            printf("Process id: %d\n", i);
            if (pcbArray[i].parent == i) {
                printf("    No parent process\n");
            } else {
                printf("    Parent process: %d\n", pcbArray[i].parent);
            }
            if (pcbArray[i].children) {
                
                int childIDs[MAX_PROCESSES];
                int childCount = 0;
                
                for (Node* child = pcbArray[i].children; child != NULL; child = child->next) {
                    childIDs[childCount++] = child->childID;
                }
                
                for (int i = childCount - 1; i >= 0; i--) {
                    printf("    Child process: %d\n", childIDs[i]);
                }
            } else {
                printf("    No child processes\n");
            }
        }
    }
}

void freeMemory() {
    for (int i = 0; i < MAX_PROCESSES; i++) {
        freeChildList(pcbArray[i].children);
        pcbArray[i].children = NULL;
    }
}

Node* createNode(int childID) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Cannot allocate memory allocation\n");
        exit(1);
    }
    newNode->childID = childID;
    newNode->next = NULL;
    return newNode;
}

void freeChildList(Node* head) {
    Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}

