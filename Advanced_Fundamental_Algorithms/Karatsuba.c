#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to multiply single digit numbers
char* multiply(char num1, char num2) {
    int n1 = num1 - '0';
    int n2 = num2 - '0';
    int prod = n1 * n2;

    char* result = malloc(3 * sizeof(char));
    sprintf(result, "%d", prod);

    return result;
}

// Function to find the maximum of two numbers
int maxi(int a, int b) {
    return (a > b) ? a : b;
}

// Function to add leading zeros to a string
char* addLeadingZeros(char* str, int n) {
    if(n <= 0)
        return str;

    char* result = malloc((strlen(str) + n + 1) * sizeof(char));
    for(int i = 0; i < n; i++)
        result[i] = '0';

    strcpy(result + n, str);

    return result;
}

// Function to add trailing zeros to a string
char* addTrailingZeros(char* str, int n) {
    if(n <= 0)
        return str;

    char* result = malloc((strlen(str) + n + 1) * sizeof(char));
    strcpy(result, str);
    for(int i = strlen(str); i < strlen(str) + n; i++)
        result[i] = '0';

    result[strlen(str) + n] = '\0';

    return result;
}

// Function to add two strings as integers
char* addStrings(char* num1, char* num2) {
    int len1 = strlen(num1);
    int len2 = strlen(num2);
    int len = maxi(len1, len2);

    char* result = malloc((len + 2) * sizeof(char));
    int carry = 0;
    for(int i = 0; i < len; i++) {
        int n1 = (i < len1) ? num1[len1 - 1 - i] - '0' : 0;
        int n2 = (i < len2) ? num2[len2 - 1 - i] - '0' : 0;
        int sum = n1 + n2 + carry;
        result[len - i] = (sum % 10) + '0';
        carry = sum / 10;
    }

    result[0] = carry + '0';
    result[len + 1] = '\0';

    return result;
}

// Function to implement the Karatsuba algorithm
char* karatsuba(char* num1, char* num2) {
    int len1 = strlen(num1);
    int len2 = strlen(num2);

    // Base case
    if(len1 == 1 && len2 == 1)
        return multiply(num1[0], num2[0]);

    // Find the maximum length and split the numbers
    int len = maxi(len1, len2);
    int mid = len / 2;

    char* Xl = addLeadingZeros(num1, len1 - mid);
    char* Xr = num1 + len1 - mid;
    char* Yl = addLeadingZeros(num2, len2 - mid);
    char* Yr = num2 + len2 - mid;

    // Recursive calls
    char* P1 = karatsuba(Xl, Yl);
    char* P2 = karatsuba(Xr, Yr);
    char* P3 = karatsuba(addStrings(Xl, Xr), addStrings(Yl, Yr));

    // Combine the results
    char* result = addStrings(addStrings(addTrailingZeros(P1, 2*mid), addTrailingZeros(P3, mid)), P2);

    return result;
}

int main() {
    char num1[] = "1234";
    char num2[] = "5678";

    char* result = karatsuba(num1, num2);

    printf("%s\n", result);

    return 0;
}
