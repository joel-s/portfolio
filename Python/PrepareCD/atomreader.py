#!/usr/bin/env python

"""
Read 

$Header: /home/joel/cvs/prepare-cd/atomreader.py,v 1.4 2003/06/23 07:07:25 joel Exp $

"""
__version__='$Revision: 1.4 $'[11:-2]


from shared import *
import sys
import re


# A constant to indicate a cache variable is unset.
class CacheEmptyType:
    def __repr__(self): return "CacheEmpty"
CacheEmpty = CacheEmptyType()


#-----------------------------------------------------------------------------
# LINE READER
#-----------------------------------------------------------------------------

class LineReader:
    """A line input stream object with a one-line lookahead capability.
    """

    def __init__(self, input):
        self._input = input
        self._nextLine = CacheEmpty

    def peekline(self):
        if self._nextLine is CacheEmpty:
            self._nextLine = self._input.readline()
##            except StopIteration:
##                self._nextLine = ""
        return self._nextLine

    def readline(self):
        line = self.peekline()
        if self._nextLine != "":
            self._nextLine = CacheEmpty
        return line

    def close(self):
        self._input.close()


#-----------------------------------------------------------------------------
# ATOM CLASSES
#-----------------------------------------------------------------------------

class Atom:
    """An abstract class for atoms read from an MP3 CD description file.
    """

    def constructFromInput(cls, lineReader):
        """Attempt to read an instance of this atom class from the input.

        <lineReader> should be an instance of LineReader.

        Return an atom object if successful, None otherwise. Eat lines from
        LineReader iff they are part of the returned atom.

        (This is an abstract method.)

        """
        pass
    constructFromInput = classmethod(constructFromInput)

    def __init__(self):
        pass

_atomClasses = []


class TrackAtom(Atom):
    _atomRE = re.compile(r"\s*([0-9:]*)\s*('\d{2}|\d{4})?\s*-\s*(\S+\.mp3)\s*$")

    def constructFromInput(cls, lineReader):
        m = cls._atomRE.match(lineReader.peekline())
        if m is None:
            return None
        lineReader.readline()  # ignore result since we already peeked
        length = m.group(1)
        year = m.group(2)
        fileName = m.group(3)

        if year is not None and year.startswith("'"):
            if year[1] in ("01"): century = "20"
            else: century = "19"
            year = century + year[1:]

        return TrackAtom(fileName, length, year)

    constructFromInput = classmethod(constructFromInput)

    def __init__(self, fileName, length, year=None):
        self.fileName = fileName
        self.length = length
        self.year = year
        Atom.__init__(self)

_atomClasses.append(TrackAtom)


class YearAtom(Atom):
    _atomRE = re.compile(r"\s*(\d{4}|--)\s*$")

    def constructFromInput(cls, lineReader):
        m = cls._atomRE.match(lineReader.peekline())
        if m is None:
            return None
        lineReader.readline()  # ignore result since we already peeked
        year = m.group(1)
        if year == "--": year = None
        return YearAtom(year)
    constructFromInput = classmethod(constructFromInput)

    def __init__(self, yearText):
        self.yearText = yearText
        Atom.__init__(self)

_atomClasses.append(YearAtom)


class FolderHeadingAtom(Atom):
    _atomRE = re.compile(r"\[([^]]*)\]\s*$")

    def constructFromInput(cls, lineReader):
        m = cls._atomRE.match(lineReader.peekline())
        if m is None:
            return None
        lineReader.readline()  # ignore result since we already peeked
        return FolderHeadingAtom(m.group(1).strip())
    constructFromInput = classmethod(constructFromInput)

    def __init__(self, folderName):
        self.folderName = folderName
        Atom.__init__(self)

_atomClasses.append(FolderHeadingAtom)


class SectionHeadingAtom(Atom):
    _atomRE = re.compile(r"\[\[ (\d+)( ([-a-z]+))? \]\]\s*$")

    def constructFromInput(cls, lineReader):
        m = cls._atomRE.match(lineReader.peekline())
        if m is None:
            return None
        lineReader.readline()  # ignore result since we already peeked
        listingMode = m.group(3) or "default"
        if listingMode == "default":
            listingFlags = LISTINGFLAG_ARTIST_ON_EACH_LINE | \
                           LISTINGFLAG_SUPPRESS_TRACK_YEAR
        elif listingMode == "include-track-year":
            listingFlags = LISTINGFLAG_ARTIST_ON_EACH_LINE
        elif listingMode == "album-instead-of-artist":
            listingFlags = LISTINGFLAG_ALBUM_ON_EACH_LINE | \
                           LISTINGFLAG_SUPPRESS_TRACK_YEAR
        elif listingMode == "include-album-headers":
            listingFlags = LISTINGFLAG_HEADING_PER_ALBUM | \
                           LISTINGFLAG_SUPPRESS_TRACK_YEAR
        elif listingMode == "track-name-only":
            listingFlags = LISTINGFLAG_SUPPRESS_TRACK_YEAR
        else:
            die("invalid listing mode: " + listingMode)
        return SectionHeadingAtom(m.group(1), listingFlags)
    constructFromInput = classmethod(constructFromInput)

    def __init__(self, sectionNum, listingFlags):
        self.sectionNum = sectionNum
        self.listingFlags = listingFlags
        Atom.__init__(self)

_atomClasses.append(SectionHeadingAtom)


class CommentAtom(Atom):
    _atomRE = re.compile(r"\s*\* (.*)$")

    def constructFromInput(cls, lineReader):
        m = cls._atomRE.match(lineReader.peekline())
        if m is None:
            return None
        comment = ""
        while m is not None:
            lineReader.readline()  # ignore result since we already peeked
            # the join/split combo below normalizes whitespace
            comment += " ".join(m.group(1).split()) + " "
            m = cls._atomRE.match(lineReader.peekline())
        return CommentAtom(comment[:-1])
    constructFromInput = classmethod(constructFromInput)

    def __init__(self, commentText):
        self.commentText = commentText
        Atom.__init__(self)

_atomClasses.append(CommentAtom)


#-----------------------------------------------------------------------------
# ATOM READER
#-----------------------------------------------------------------------------

class AtomReader:
    """A class that returns atoms from an MP3 CD description file.

    Files can have at most one atom per line. Some atoms can span multiple
    lines.

    """

    def __init__(self, input):
        """Initialize. Argument should be a file stream object."""
        self._lineReader = LineReader(input)
        self._nextAtom = CacheEmpty

    def _readAtom(self):

        while self._lineReader.peekline() != "":
            for atomClass in _atomClasses:
                atom = atomClass.constructFromInput(self._lineReader)
                if atom is not None:
                    return atom

            # No match on this line, go on to next one.
            self._lineReader.readline()  

        # end of file
        return None

    def peekAtom(self):
        """Return the next atom in the stream, or None if stream is empty.
        """
        if self._nextAtom is CacheEmpty:
            self._nextAtom = self._readAtom()
        return self._nextAtom

    def readAtom(self):
        atom = self.peekAtom()
        if self._nextAtom is not None:
            self._nextAtom = CacheEmpty
        return atom


#-----------------------------------------------------------------------------
# SELF-TEST
#-----------------------------------------------------------------------------

def _test():
    import fileinput
    atomReader = AtomReader(fileinput.input())
    while 1:
        atom = atomReader.readAtom()
        if atom is None:
            return
        print " found:", atom #DEBUG

if __name__ == "__main__":
    sys.exit(_test())
