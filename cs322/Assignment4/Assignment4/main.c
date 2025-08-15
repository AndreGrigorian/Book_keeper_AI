
#include <stdio.h>
#include <stdlib.h>

typedef struct block {
    int id;
    int start;
    int end;
    struct block *next;
} Block;

Block *head = NULL;
int pm_size = 0;

void enterParameters() {
    printf("Enter size of physical memory: ");
    scanf("%d", &pm_size);
}

Block *createBlock(int id, int size) {
    Block *newBlock = (Block *)malloc(sizeof(Block));
    if (newBlock == NULL) {
        printf("Memory allocation failed.\n");
        return NULL;
    }
    newBlock->id = id;
    newBlock->start = -1; // Invalid start and end until placed
    newBlock->end = -1;
    newBlock->next = NULL;
    return newBlock;
}

void addBlock(Block *newBlock, int start, int size) {
    newBlock->start = start;
    newBlock->end = start + size;
    if (head == NULL) {
        head = newBlock;
    } else {
        Block *temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newBlock;
    }
}

int findFirstFit(int size) {
    int start = 0;
    Block *current = head;
    if (current == NULL) {
        return start;
    }

    while (current != NULL) {
        if (current->start - start >= size) {
            return start;
        }
        start = current->end;
        current = current->next;
    }

    if (pm_size - start >= size) {
        return start;
    }
    return -1; // No sufficient space found
}

int findBestFit(int size) {
    int bestStart = -1;
    int minGap = pm_size + 1;
    int start = 0;

    Block *current = head;
    while (current != NULL) {
        int gap = current->start - start;
        if (gap >= size && gap < minGap) {
            bestStart = start;
            minGap = gap;
        }
        start = current->end;
        current = current->next;
    }

    if (pm_size - start >= size && (pm_size - start) < minGap) {
        bestStart = start;
    }

    return bestStart;
}

void allocateMemory(int method) {
    int id, size;
    printf("Enter block id: ");
    scanf("%d", &id);
    printf("Enter block size: ");
    scanf("%d", &size);

    Block *current = head;
    while (current != NULL) {
        if (current->id == id) {
            printf("Error: Block ID already exists.\n");
            return;
        }
        current = current->next;
    }

    int start = (method == 1) ? findFirstFit(size) : findBestFit(size);
    if (start == -1) {
        printf("Allocation failed. No sufficient space.\n");
        return;
    }

    Block *newBlock = createBlock(id, size);
    addBlock(newBlock, start, size);
    printf("Block allocated: ID %d, Start %d, End %d\n", id, start, start + size);
}

void deallocateMemory() {
    int id;
    printf("Enter block id to deallocate: ");
    scanf("%d", &id);

    Block *current = head, *prev = NULL;
    while (current != NULL && current->id != id) {
        prev = current;
        current = current->next;
    }

    if (current == NULL) {
        printf("Error: No such block found.\n");
        return;
    }

    if (prev == NULL) {
        head = current->next;
    } else {
        prev->next = current->next;
    }

    free(current);
    printf("Block %d deallocated.\n", id);
}

void defragment() {
    if (head == NULL) {
        return;
    }

    Block *current = head;
    int start = 0;
    while (current != NULL) {
        if (current->start != start) {
            current->end = start + (current->end - current->start);
            current->start = start;
        }
        start = current->end;
        current = current->next;
    }
    printf("Memory defragmented.\n");
}

void printBlocks() {
    Block *current = head;
    printf("ID\tStart\tEnd\n");
    printf("-------------------\n");
    while (current != NULL) {
        printf("%d\t%d\t%d\n", current->id, current->start, current->end);
        current = current->next;
    }
}

int main() {
    int choice;
    do {
        printf("Hole-fitting Algorithms\n");
        printf("-----------------------\n");
        printf("1) Enter parameters\n");
        printf("2) Allocate memory for block using First-fit\n");
        printf("3) Allocate memory for block using Best-fit\n");
        printf("4) Deallocate memory for block\n");
        printf("5) Defragment memory\n");
        printf("6) Quit program\n");
        printf("Enter selection: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: enterParameters(); break;
            case 2: allocateMemory(1); break;
            case 3: allocateMemory(2); break;
            case 4: deallocateMemory(); break;
            case 5: defragment(); printBlocks(); break;
            case 6: printf("Quitting program...\n"); break;
            default: printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 6);

    // Cleanup
    Block *temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }

    return 0;
}
