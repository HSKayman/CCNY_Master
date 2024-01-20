#include <stdio.h>
#include <stdlib.h>

// Function to compare two integers for qsort()
int compare(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

// Function to find the median of an array
double findMedian(int arr[], int n) {
    // Sort the array
    qsort(arr, n, sizeof(int), compare);

    // If the array size is even, return the average of the middle two elements
    // Else, return the middle element
    if (n % 2 == 0)
        return (arr[n / 2 - 1] + arr[n / 2]) / 2.0;
    else
        return arr[n / 2];
}

// Driver code
int main() {
    int arr[] = {12, 11, 15, 10, 20};
    int n = sizeof(arr) / sizeof(arr[0]);
    printf("Median = %.2f\n", findMedian(arr, n));
    return 0;
}
