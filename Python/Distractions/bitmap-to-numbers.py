#! /usr/bin/env python

"""
Convert a bitmap represented as text into a sequence of 16-bit numbers, and
convert it back to text.

TODO: This code could use more comments and fewer magic numbers.
"""


bitmap = [
    "xxx  xxx         xxx   xxx            xx    xx ",
    " x    x    x      x     x              x     x ",
    " x    x           x     x              x     x ",
    " xxxxxx   xx      x     x   xx  xx xx  x   xxx ",
    " x    x    x      x  x  x  x  x  xx    x  x  x ",
    " x    x    x      x x x x  x  x  x     x  x  x ",
    "xxx  xxx  xxx     xx   xx   xx  xxx   xxx  xxxx",
    "FEDCBA9876543210FEDCBA9876543210",
    "F               F               ",
    "               0               0",
    "F              0F              0",
    ]


def textToNumber(text):
    result = 0
    for char in text:
        result <<= 1
        if char != " ":
            result += 1
    return result

def bitmapTextToNumbers(textArray):
    numberArray = []
    for line in textArray:
        arrayLine = []
        while line != "":
            next16, line = line[0:16], line[16:]
            if len(next16) < 16:
                next16 += " " * (16 - len(next16))
            arrayLine.append(textToNumber(next16))
        numberArray.append(arrayLine)
    return numberArray

def numberToText(number, bits):
    text = ""
    for bit in range(bits):
        if number & 1:
            text = "%" + text
        else:
            text = " " + text
        number >>= 1
    return text

def numbersToBitmapText(numberArray):
    textArray = []
    for line in numberArray:
        textLine = ""
        while line:
            number, line = line[0], line[1:]
            textLine += numberToText(number, 16)
        textArray.append(textLine)
    return textArray

numberArray = bitmapTextToNumbers(bitmap)
for line in numberArray:
    print(line)
print()

textArray = numbersToBitmapText(numberArray)
for line in textArray:
    print(line)
print()
