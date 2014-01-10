#! /usr/bin/env python

import sys
import re

class Histogram:
    """A histogram read from a file formatted like: name (number).
    """
    def __init__(self, file):
        self.hist = []
        regexp = re.compile(r"([^)]+) \(([^)]+)\)")
        for line in file:
            line = line.strip()
            if not line:
                continue
            print line
            m = regexp.match(line)
            name = m.group(1)
            val = int(m.group(2))
            self.hist.append((name, val))

    def sort(self):
        self.hist.sort(lambda a, b: -cmp(a[1], b[1])) # - reverses order

    def show(self, out):
        maxval = self.hist[0][1]
        for name, val in self.hist:
            print "%-20s %5d "  % (name, val),
            print "*" * (70 * val / maxval)
            
def main():
    file = open("Skills.txt", "r")
    hist = Histogram(file)
    file.close()

    hist.sort()
    hist.show(sys.stdout)

main()
