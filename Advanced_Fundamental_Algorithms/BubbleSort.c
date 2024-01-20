#include <stdio.h>
#include <stdbool.h>
#include <time.h>

#define SIZE 10000

// Function to swap two elements
void swap(int *xp, int *yp) {
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

// Basic Bubble Sort
void bubbleSort(int arr[], int n) {
   for (int i = 0; i < n-1; i++) {     
       for (int j = 0; j < n-i-1; j++) {
           if (arr[j] > arr[j+1])
              swap(&arr[j], &arr[j+1]);
       }
   }
}

// Optimized Bubble Sort
void optimizedBubbleSort(int arr[], int n) {
   int i, j;
   bool swapped;
   for (i = 0; i < n-1; i++) {
     swapped = false;
     for (j = 0; j < n-i-1; j++) {
        if (arr[j] > arr[j+1]) {
           swap(&arr[j], &arr[j+1]);
           swapped = true;
        }
     }
  
     // If no two elements were swapped by inner loop, then the array is sorted
     if (swapped == false)
        break;
   }
}

// Recursive Bubble Sort
void recursiveBubbleSort(int arr[], int n) {
   // Base case
   if (n == 1)
      return;
  
   // One pass of bubble sort. After this pass, the largest element is moved to end.
   for (int i=0; i<n-1; i++) {
      if (arr[i] > arr[i+1])
         swap(&arr[i], &arr[i+1]);
   }
  
   // Largest element is fixed, recur for remaining array
   recursiveBubbleSort(arr, n-1);
}

int main() {
    int arr[SIZE];
    clock_t start, end;
    double cpu_time_used;

    // Seed the random number generator
    srand(time(NULL));

    // Generate 100,000 random numbers between 1 and SIZE
    for(int i = 0; i < SIZE; i++)
        arr[i] = rand() % SIZE + 1;

    start = clock();
    bubbleSort(arr, SIZE);
    end = clock();
    cpu_time_used = ((double) (end - start));
    printf("Time taken by basic Bubble Sort: %f seconds\n", cpu_time_used);

    // Generate 100,000 random numbers between 1 and SIZE
    for(int i = 0; i < SIZE; i++)
        arr[i] = rand() % SIZE + 1;

    start = clock();
    optimizedBubbleSort(arr, SIZE);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by optimized Bubble Sort: %f seconds\n", cpu_time_used);

    // Generate 100,000 random numbers between 1 and SIZE
    for(int i = 0; i < SIZE; i++)
        arr[i] = rand() % SIZE + 1;

    start = clock();
    recursiveBubbleSort(arr, SIZE);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken by recursive Bubble Sort: %f seconds\n", cpu_time_used);

    return 0;
}