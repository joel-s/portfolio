#! /usr/bin/env python

"""
Count different ways that coins can be combined to make a total amount.
"""

# A dictionary of (coins, total) -> count
# where coins is a tuple of coin denominations in descending order
comboDict = {}

def countCombos(coins, total):
    """Count the number of ways coins can be combined to make a total.
    
    'coins' is a tuple of coin denominantions in decreasing order.
    'total' is the total the coins must add up to.

    The basic algorithm is:
        Find the index of the largest coin we can use as part of the total
        For each coin we can use, starting with the largest:
            Use this coin (subtract it from the total to form a new total)
            Calculate the number of ways we can use the remaining coins to make the new,
                reduced total (by calling this function recursively)
    """
    if len(coins) == 0:
        return 0
    smallestCoin = coins[len(coins)-1]
    if total == 0:
        return 1    # 1 way to make a total of 0 
    if total < smallestCoin:
        return 0    # can't make a total smaller than the smallest coin
    if total == smallestCoin:
        return 1
    
    # If we have already calculated the number of combinations, just return it
    if comboDict.has_key((coins,total)):
        return comboDict[(coins,total)]

    largestUsableCoinIndex = getLargestUsableCoinIndex(coins, total)
    count = 0
    for i in range(largestUsableCoinIndex, len(coins)):
        newTotal = total - coins[i]
        count += countCombos(coins[i:], newTotal)
    comboDict[(coins,total)] = count  # Save count so we can recalculate it quickly
    return count

def getLargestUsableCoinIndex(coins, total):
    for i in range(len(coins)):
        if coins[i] <= total:
            return i

coins = [1, 2, 5, 10, 20, 50, 100, 200]
coins.reverse()
print countCombos(tuple(coins), 200)
