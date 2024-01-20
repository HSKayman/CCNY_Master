#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 100000

// Swap two elements
void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

// Lomuto partition scheme
int partitionLomuto(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// Hoare partition scheme
int partitionHoare(int arr[], int low, int high) {
    int pivot = arr[low];
    int i = low - 1, j = high + 1;

    while (1) {
        do {
            i++;
        } while (arr[i] < pivot);

        do {
            j--;
        } while (arr[j] > pivot);

        if (i >= j)
            return j;

        swap(&arr[i], &arr[j]);
    }
}

// Randomized version
int partitionRandom(int arr[], int low, int high) {
    srand(time(NULL));
    int random = low + rand() % (high - low);
    swap(&arr[random], &arr[high]);
    return partitionLomuto(arr, low, high);
}

// QuickSort using Lomuto partition scheme
void quickSortLomuto(int arr[], int low, int high) {
    if (low < high) {
        int pi = partitionLomuto(arr, low, high);
        quickSortLomuto(arr, low, pi - 1);
        quickSortLomuto(arr, pi + 1, high);
    }
}

// QuickSort using Hoare partition scheme
void quickSortHoare(int arr[], int low, int high) {
    if (low < high) {
        int pi = partitionHoare(arr, low, high);
        quickSortHoare(arr, low, pi);
        quickSortHoare(arr, pi + 1, high);
    }
}

// QuickSort using randomized version
void quickSortRandom(int arr[], int low, int high) {
    if (low < high) {
        int pi = partitionRandom(arr, low, high);
        quickSortRandom(arr, low, pi - 1);
        quickSortRandom(arr, pi + 1, high);
    }
}

// Function to print an array
void printArray(int arr[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// Driver code
int main() {
    int arr[SIZE], arr_copy1[SIZE], arr_copy2[SIZE];
    clock_t start, end;
    double cpu_time_used;

    // Generate SIZE random numbers between 1 and SIZE
    for(int i = 0; i < SIZE; i++)
        arr[i] = rand() % SIZE + 1;

    // Make copies of the array for the other two algorithms
    for(int i = 0; i < SIZE; i++) {
        arr_copy1[i] = arr[i];
        arr_copy2[i] = arr[i];
    }

    start = clock();
    quickSortLomuto(arr, 0, SIZE - 1);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by QuickSort with Lomuto partition: %f seconds\n", cpu_time_used);

    start = clock();
    quickSortHoare(arr_copy1, 0, SIZE - 1);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by QuickSort with Hoare partition: %f seconds\n", cpu_time_used);

    start = clock();
    quickSortRandom(arr_copy2, 0, SIZE - 1);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by QuickSort with randomized partition: %f seconds\n", cpu_time_used);

    return 0;
}
