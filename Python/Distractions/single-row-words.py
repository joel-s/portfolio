#! /usr/bin/env python2

"""

Find the longest words (lines) in the imput that can be typed using
only a single row of the keyboard.

"""

import sys

rows = ["qwertyuiop", "asdfghjkl;", "zxcvbnm"]
keyToRow = {}

singleRowWords = [{}, {}, {}]

for i in range(len(rows)):
    for key in rows[i]:
        keyToRow[key] = i

for line in sys.stdin:
    word = line.rstrip().lower()
    row = keyToRow[word[0]]

    singleRowWord = True
    for i in range(1, len(word)):
        if keyToRow[word[i]] != row:
            singleRowWord = False
            break

    if singleRowWord:
        if singleRowWords[row].has_key(len(word)):  
            singleRowWords[row][len(word)].append(word)
        else:
            singleRowWords[row][len(word)] = [word]

for row in range(len(rows)):
    keys = singleRowWords[row].keys()
    keys.sort()
    print singleRowWords[row][keys[-1]]
    print singleRowWords[row][keys[-2]]
