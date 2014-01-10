#!/bin/env python2

"""
Read text from stdin and create .desc files that describe JPG images.
The .desc files are used by "curator" as image subtitles on a web site.

This code could definitely use more comments.
"""

import sys
import os
import glob
import commands

if not os.path.exists("01"):
    print "d'oh!"
    sys.exit(1)

commands.getoutput("rm */*.txt */*.desc")

inp = sys.stdin

dirIndex = 0

while 1:
    line = inp.readline()
    if not line:
        sys.exit()

    line = line.rstrip()
    if line == "" or line.startswith(" "):
        continue

    if line.startswith("== "):
        dirIndex += 1
        dir = "%02d" % dirIndex

        desc = open(dir +"/desc.txt", "w")
        desc.write(line[3:] +"\n")
        while 1:
            line = inp.readline().strip()
            if not line:
                break
            desc.write(line +" ")
        desc.write("\n")
        desc.close()

        images = glob.glob(dir +"/*.jpg")
        i = 0
        while i < len(images):
            if images[i].endswith("--thumb.jpg"):
                del images[i]
            else:
                i += 1
        images.sort()
        continue

    # Pop next filename off top of list
    if len(images) == 0: continue
    filename = images[0]
    images = images[1:]

    # Strip off .jpg
    base = filename[:-4]

    print filename
    print "   " +line
    
    desc = open(base +".desc", "w")
    desc.write("title: " +line +"\n")
    desc.write("\n")
    desc.write("description: ")
    while 1:
        line = inp.readline().strip()
        if not line:
            break
        desc.write(line +"\n")
    desc.write("\n")
    desc.close()
