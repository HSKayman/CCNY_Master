#include <stdio.h>

// Returns true if there is a subset of set[] with sum equal to given sum
int isSubsetSum(int set[], int n, int sum) {
    // The value of subset[i][j] will be true if there is a subset of set[0..j-1] with sum equal to i
    int subset[n+1][sum+1];

    // If sum is 0, then answer is true
    for (int i = 0; i <= n; i++)
      subset[i][0] = 1;

    // If sum is not 0 and set is empty, then answer is false
    for (int i = 1; i <= sum; i++)
      subset[0][i] = 0;

     // Fill the subset table in bottom up manner
     for (int i = 1; i <= n; i++) {
       for (int j = 1; j <= sum; j++) {
         if(j<set[i-1])
         subset[i][j] = subset[i-1][j];
         if (j >= set[i-1])
           subset[i][j] = subset[i-1][j] || subset[i - 1][j-set[i-1]];
       }
     }

     return subset[n][sum];
}

int main() {
    int set[] = {3, 34, 4, 12, 5, 2};
    int sum = 9;
    int n = sizeof(set)/sizeof(set[0]);
    if (isSubsetSum(set, n, sum) == 1)
         printf("Found a subset with given sum");
    else
         printf("No subset with given sum");
    return 0;
}
