# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:43:00 2023

@author: HSK
"""

def lagrange_interpolation(x_values, y_values):
    def P(x):
        total = 0
        n = len(x_values)
        for i in range(n):
            xi, yi = x_values[i], y_values[i]

            def g(i, n):
                tot_mul = 1
                for j in range(n):
                    if i != j:
                        xj = x_values[j]
                        tot_mul *= (x - xj) / float(xi - xj)
                return tot_mul

            total += yi * g(i, n)
        return total
    
    return P

x_values = [1, 2, 3, 4, 5]
y_values = [2, 3, 5, 7, 11]
P = lagrange_interpolation(x_values, y_values)
print(P(0))  # This will print the interpolated value at x = 2.5

