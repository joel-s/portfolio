#! /usr/bin/env python

import math

"""Get the Nth permutation of a set of consecutive numbers.
N is zero-based.
For example, the second permutation (n=1) of 0,1,2 is 0,2,1.
"""
def nth_permutation(numbers, n):
    if len(numbers) == 1:
        return numbers
    # Calculate number of permutations for all items but the first 
    perms_of_remainder = math.factorial(len(numbers)-1)
    # Calculate the index of the number to put first
    i = n / perms_of_remainder
    # Take out the number at index i
    remaining_nums = numbers[0:i] + numbers[i+1:]
    return [numbers[i]] + \
           nth_permutation(remaining_nums, n % perms_of_remainder)


# Main program
print nth_permutation(range(0,10), 0)
print nth_permutation(range(0,10), 1)
print nth_permutation(range(0,10), 2)
print nth_permutation(range(0,10), 1000000-1)

