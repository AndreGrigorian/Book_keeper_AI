#include <stdio.h>
#include <stdlib.h>

void enterParameters(int *size, int **sequence) {
    printf("Enter size of sequence: ");
    scanf("%d", size);
    *sequence = (int *)malloc((*size) * sizeof(int));
    if (*sequence == NULL) {
        printf("Memory allocation failed\n");
        exit(1);
    }
}

int calculateDistanceFIFO(int start, int size, int *sequence) {
    int distance = abs(sequence[0] - start);
    for (int i = 0; i < size - 1; i++) {
        distance += abs(sequence[i + 1] - sequence[i]);
    }
    return distance;
}

int calculateDistanceSSTF(int start, int size, int *sequence) {
    int distance = 0;
    int *visited = (int *)calloc(size, sizeof(int));
    int current = start;
    
    for (int i = 0; i < size; i++) {
        int minDistance = __INT_MAX__;
        int nextIndex = -1;
        for (int j = 0; j < size; j++) {
            if (!visited[j] && abs(sequence[j] - current) < minDistance) {
                minDistance = abs(sequence[j] - current);
                nextIndex = j;
            }
        }
        visited[nextIndex] = 1;
        distance += minDistance;
        current = sequence[nextIndex];
    }
    free(visited);
    return distance;
}

int calculateDistanceScan(int start, int size, int *sequence, int direction) {
    int distance = 0;
    int *sortedSequence = (int *)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        sortedSequence[i] = sequence[i];
    }

    // Sort the sequence
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (sortedSequence[j] > sortedSequence[j + 1]) {
                int temp = sortedSequence[j];
                sortedSequence[j] = sortedSequence[j + 1];
                sortedSequence[j + 1] = temp;
            }
        }
    }

    if (direction == 1) { // Increasing
        int i;
        for (i = 0; i < size; i++) {
            if (sortedSequence[i] >= start) break;
        }
        distance += abs(start - sortedSequence[i]);
        for (int j = i + 1; j < size; j++) {
            distance += abs(sortedSequence[j] - sortedSequence[j - 1]);
        }
        for (int j = 0; j < i; j++) {
            distance += abs(sortedSequence[j + 1] - sortedSequence[j]);
        }
    } else { // Decreasing
        int i;
        for (i = size - 1; i >= 0; i--) {
            if (sortedSequence[i] <= start) break;
        }
        distance += abs(start - sortedSequence[i]);
        for (int j = i - 1; j >= 0; j--) {
            distance += abs(sortedSequence[j] - sortedSequence[j + 1]);
        }
        for (int j = size - 1; j > i; j--) {
            distance += abs(sortedSequence[j] - sortedSequence[j - 1]);
        }
    }

    free(sortedSequence);
    return distance;
}

int calculateDistanceCScan(int start, int size, int *sequence) {
    int distance = 0;
    int *sortedSequence = (int *)malloc(size * sizeof(int));
    for (int i = 0; i < size; i++) {
        sortedSequence[i] = sequence[i];
    }

    // Sort the sequence
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (sortedSequence[j] > sortedSequence[j + 1]) {
                int temp = sortedSequence[j];
                sortedSequence[j] = sortedSequence[j + 1];
                sortedSequence[j + 1] = temp;
            }
        }
    }

    int i;
    for (i = 0; i < size; i++) {
        if (sortedSequence[i] >= start) break;
    }
    distance += abs(start - sortedSequence[i]);
    for (int j = i + 1; j < size; j++) {
        distance += abs(sortedSequence[j] - sortedSequence[j - 1]);
    }
    for (int j = 0; j < i; j++) {
        distance += abs(sortedSequence[j + 1] - sortedSequence[j]);
    }

    free(sortedSequence);
    return distance;
}

void printMenu() {
    printf("Disk scheduling\n");
    printf("---------------\n");
    printf("1) Enter parameters\n");
    printf("2) Calculate distance to traverse tracks using FIFO\n");
    printf("3) Calculate distance to traverse tracks using SSTF\n");
    printf("4) Calculate distance to traverse tracks using Scan\n");
    printf("5) Calculate distance to traverse tracks using C-Scan\n");
    printf("6) Quit program and free memory\n");
    printf("Enter selection: ");
}

int main() {
    int *sequence = NULL;
    int size = 0;
    int choice;
    int direction;
    int start;

    while (1) {
        printMenu();
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                if (sequence != NULL) {
                    free(sequence);
                }
                enterParameters(&size, &sequence);
                break;
            case 2:
                if (sequence != NULL) {
                    printf("Enter starting track: ");
                    scanf("%d", &start);
                    printf("Enter sequence of tracks to seek: ");
                    for (int i = 0; i < size; i++) {
                        scanf("%d", &sequence[i]);
                    }
                    printf("The distance of the traversed tracks is: %d\n", calculateDistanceFIFO(start, size, sequence));
                } else {
                    printf("No sequence entered\n");
                }
                break;
            case 3:
                if (sequence != NULL) {
                    printf("Enter starting track: ");
                    scanf("%d", &start);
                    printf("Enter sequence of tracks to seek: ");
                    for (int i = 0; i < size; i++) {
                        scanf("%d", &sequence[i]);
                    }
                    printf("The distance of the traversed tracks is: %d\n", calculateDistanceSSTF(start, size, sequence));
                } else {
                    printf("No sequence entered\n");
                }
                break;
            case 4:
                if (sequence != NULL) {
                    printf("Enter starting track: ");
                    scanf("%d", &start);
                    printf("Enter sequence of tracks to seek: ");
                    for (int i = 0; i < size; i++) {
                        scanf("%d", &sequence[i]);
                    }
                    printf("Enter initial direction: (0=decreasing, 1=increasing): ");
                    scanf("%d", &direction);
                    printf("The distance of the traversed tracks is: %d\n", calculateDistanceScan(start, size, sequence, direction));
                } else {
                    printf("No sequence entered\n");
                }
                break;
            case 5:
                if (sequence != NULL) {
                    printf("Enter starting track: ");
                    scanf("%d", &start);
                    printf("Enter sequence of tracks to seek: ");
                    for (int i = 0; i < size; i++) {
                        scanf("%d", &sequence[i]);
                    }
                    printf("The distance of the traversed tracks is: %d\n", calculateDistanceCScan(start, size, sequence));
                } else {
                    printf("No sequence entered\n");
                }
                break;
            case 6:
                if (sequence != NULL) {
                    free(sequence);
                }
                printf("Quitting program...\n");
                return 0;
            default:
                printf("Invalid selection\n");
        }
    }
    return 0;
}

