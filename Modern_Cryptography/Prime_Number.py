# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:52:49 2024

@author: HSK
"""

def primeFinder(x):
    if x <= 1:
        return False
    
    if x <= 3:
        return True
    
    if x % 2 == 0 or x % 3 == 0:
        return False
    
    i = 5
    
    while i*i <= x:
        if x%i == 0:
            return False
        i+=6
        
    return True

count = 1
for i in range(1000, 1100):
    if primeFinder(i):
        print(count,". ->",i)
        count+=1