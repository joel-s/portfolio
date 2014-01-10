#!/usr/bin/env python

import sys


LISTINGFLAG_HEADING_PER_ALBUM = 1
LISTINGFLAG_ALBUM_ON_EACH_LINE = 2
LISTINGFLAG_ARTIST_ON_EACH_LINE = 4
LISTINGFLAG_SUPPRESS_TRACK_YEAR = 8


def err(msg):
    sys.stderr.write(msg +"\n")

def die(msg):
    err(msg)
    sys.exit(2)

def fillText(text, continuationPrefix="", maxLineLength=76):
    """Add line-breaks to <text>.
    
    Replace ' ' with '\n'+<continuationPrefix> as necessary to ensure no
    line longer than <maxLineLength>. Return the result as a string, ending
    with '\n'.

    The text should not contain newlines, tabs, or multiple consecutive
    spaces.

    """
    text = text.rstrip()
    if len(text) <= maxLineLength:
        return text + "\n"

    # Find a space
    spaceIndex = text.rfind(" ", 0, maxLineLength + 1)
    if spaceIndex == -1 or text[:spaceIndex].rstrip() == "":
        # Couldn't find an embedded space w/in line length
        spaceIndex = text.find(" ", maxLineLength + 1)
        if spaceIndex == -1:
            # Couldn't find any embedded space in string
            return text + "\n"
    # Split the string
    returnText = text[:spaceIndex] + "\n" + continuationPrefix
    text = text[spaceIndex+1:]

    maxContLength = maxLineLength - len(continuationPrefix)
    while len(text) > maxLineLength:
        # Find a space
        spaceIndex = text.rfind(" ", 0, maxContLength + 1)
        if spaceIndex == -1:
            # Couldn't find an embedded space w/in line length
            spaceIndex = text.find(" ", maxLineLength + 1)
            if spaceIndex == -1:
                # Couldn't find any embedded space in string
                break
        # Split the string
        returnText += text[:spaceIndex] + "\n" + continuationPrefix
        text = text[spaceIndex+1:]

    return returnText + text + "\n"
