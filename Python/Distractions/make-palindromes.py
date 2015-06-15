#! /usr/bin/env python2

"""

Generate sequences of words that are palindromes.

Don't choose the same word more than once.

Generate palindromes of increasing minimum length starting with 1.

This requires Python 2 and "grep" and "sed", although it could have been
done in "pure" Python.

"""

import sys
import string
import commands
import random
import traceback


DEBUG = 0

CASE_OPTION = ""  # "-i" to allow uppercase, "" otherwise


# -- DICTIONARY REPRESENTATION

##DICT_FILE = "/usr/share/dict/words"
DICT_FILE = "./words.lower"

_NUM_WORDS = None
def chooseRandomWord():
    global _NUM_WORDS
    if _NUM_WORDS is None:
        _NUM_WORDS = int(commands.getoutput(
            "sed -n -e '$=' " +DICT_FILE
            ))  # could use wc -l
    lineNum = random.randrange(0, _NUM_WORDS) + 1
    text = commands.getoutput(
        "sed -n -e '" +`lineNum` +"p' " +DICT_FILE
        )
    return text.strip()

def getValidWord(s):
    """Return a valid word with the given letters, if possible.

    If those letters cannot form a word, return None.

    """
    text = commands.getoutput(
        "grep " +CASE_OPTION +" ^" +s +"\\$ " +DICT_FILE
        )
    if text:
        return text.split()[0]
    else:
        return None

def wordsThatStartWith(s):
    """Return a list of valid words that start with a given string.

    Case insensitive. The string <s> itself can be in the return list.
    
    """
    text = commands.getoutput(
        "grep " +CASE_OPTION +" ^" +s +" " +DICT_FILE
        )
#    if DEBUG: print "   > startWith: " +string.join(text.split())
    return text.split()

def wordsThatEndWith(s):
    """Return a list of valid words that end with a given string.

    Case insensitive. The string <s> itself can be in the return list.
    
    """
    text = commands.getoutput(
        "grep " +CASE_OPTION +" " +s +"\\$ " +DICT_FILE
        )
#    if DEBUG: print "   > endWith: " +string.join(text.split())
    return text.split()





def reverseString(s):
    l = list(s)
    l.reverse()
    return string.join(l, "")

def isPalindrome(s):
    s = s.lower()
    return s == reverseString(s)

def makePalindrome(minWords):
    while 1:
        word = chooseRandomWord()
        rest = palindromeWithSuffix(reverseString(word), minWords - 1,
                                    (word,))
        if rest is not None:
            return word +" " +rest

def palindromeWithPrefix(s, minWords, blacklist=()):
    """Try to generate (beginning + palindrome) where beginning is <s>

    Must be at least minWords words in palindrome.

    Return None if unable to do so.
    
    """
    global debugStack
    
    if DEBUG: print " -D- palindromeWithPrefix(" +`s` +")"
    
    superWords = wordsThatStartWith(s)
    random.shuffle(superWords)

    if minWords <= 1:
        # Try to complete the palindrome
        for word in superWords:
            if word in blacklist: continue
            extraChars = word[len(s):]
            if isPalindrome(extraChars):
                debugStack = traceback.format_stack()
                return word
    
    # Find a longer word if possible
    for word in superWords: 
        if word in blacklist: continue
        extraChars = word[len(s):]
        rest = palindromeWithSuffix(reverseString(extraChars), minWords - 1,
                                    blacklist + (word,))
        if rest is not None:
            return word +" " +rest

    # Take off as much of the word as possible
    for splitPos in range(len(s) - 2, 0, -1):
        word = getValidWord(s[:splitPos])
        if word in blacklist: continue
        if word is not None:
            rest = palindromeWithPrefix(s[splitPos:], minWords - 1,
                                        blacklist + (word,))
            if rest is not None:
                return word +" " +rest

def palindromeWithSuffix(s, minWords, blacklist=()):
    """Try to generate (palindrome + ending) where ending is <s>

    Must be at least minWords words in palindrome.

    Return None if unable to do so.
    
    """
    if DEBUG: global debugStack
    
    if DEBUG: print " -D- palindromeWithSuffix(" +`s` +")"

    superWords = wordsThatEndWith(s)
    random.shuffle(superWords)

    if minWords <= 1:
        # Try to complete the palindrome
        for word in superWords:
            if word in blacklist: continue
            extraChars = word[:len(word)-len(s)]
            if isPalindrome(extraChars):
                if DEBUG: debugStack = traceback.format_stack()
                return word
    
    # Find a longer word if possible
    for word in superWords: 
        if word in blacklist: continue
        extraChars = word[:len(word)-len(s)]
        rest = palindromeWithPrefix(reverseString(extraChars), minWords - 1,
                                    blacklist + (word,))
        if rest is not None:
            return rest +" " +word

    # Take off as much of the word as possible
    for splitPos in range(1, len(s) - 1):
        word = getValidWord(s[splitPos:])
        if word in blacklist: continue
        if word is not None:
            rest = palindromeWithSuffix(s[:splitPos], minWords - 1,
                                        blacklist + (word,))
            if rest is not None:
                return rest +" " +word

for minWords in range(1,50):
    print "Palindromes with a minimum of %d words" % minWords
    print "-----"
    for i in range(5):
        pal = makePalindrome(minWords)
        print pal
        pal = pal.replace(" ", "")
        if DEBUG and pal != reverseString(pal):
            for line in debugStack:
                print line
            sys.exit()
