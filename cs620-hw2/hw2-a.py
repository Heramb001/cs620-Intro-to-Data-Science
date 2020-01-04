"""
CS 620
HW2-a
@author: Heramb
"""
#import Libraries
import numpy as np


"""Given two list of numbers that are already sorted, 
 return a single merged list in sorted order.
"""
def merge(sortedListA, sortedListB):
    #Complete this part
    sortedList = sorted(sortedListA + sortedListB)
    return sortedList

"""Given a list of numbers in random order, return the summary statistics 
that includes the max, min, mean, population standard deviation, median,
75 percentile, and 25 percentile.
"""    
def summaryStatistics(listOfNums):
    #Complete this part. 
    # You can decide to return the following statistics either in a sequence 
    # type (i.e., list, tuple), or a key-value pair (i.e., dictionary)
    return {'max': np.max(listOfNums), 
            'min': np.min(listOfNums), 
            'mean': np.mean(listOfNums), 
            'stdev': np.std(listOfNums),
            'median': np.median(listOfNums),
            'perc75': np.percentile(listOfNums,75),
            'perc25': np.percentile(listOfNums,25)}
    

"""Given a list of real numbers in any range, scale them to be 
between 0 and 1 (inclusive). For each number x in the list, the new number 
is computed with the formula ((x - min)/(max - min)) where max is the 
maximum value of the original list and min is the minimum value of the list. 
"""	
def scaleToDigits(listOfNums): 
    #complete this part
    newList = list(map(lambda x : ((x - np.min(listOfNums))/(np.max(listOfNums) - np.min(listOfNums))),listOfNums))
    return newList

#----Testing Data ------#
#---- Uncomment below lines to get the text data
""" 
listA = [1,2,3,4,5,6,7]
listB = [8,9,10,11]
listD = [1,5,6,9,11,3,7]
print('#-------# Func 1 - merge() #-------#')
print('--> A = ',listA)
print('--> B = ',listB)
print('--> C = ',merge(listB,listA))

print('#-------# Func 2 - summaryStatistics() #-------#')
print(summaryStatistics(listA))

print('#-------# Func 3 - scaleToDigits() #-------#')
print(scaleToDigits(listD))
"""
