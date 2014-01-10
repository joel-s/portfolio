#!/usr/bin/env python

"""
Generate a directory containing MP3 files and an ASCII text catalog.

An example of the text catalog format is shown below.

++ START EXAMLE ++

Key:
  Artist: Track Name <MM:SS>
  Album - Track Name <MM:SS>


<<< 1 >>>

Comment goes here.

    [[ Random Stuff ]]
      ~~~
    Comment goes here.
      ~~~
       1. -1924- Pale Saints: Kinky Love <7:27>
       2. -1972- Cocteau Twins: Mizake the Mizan (2012) <2:56>
       3. -2002- Pizzicato Five: Tokyo Mon Amour (Discotique 96 Mix)
          <2:25>


<<< 2 >>>

Comment goes here.

    [[ Dzihan and Kamien ]]
      ~~~
    These Austrian dub DJs (D & K) should not be confused
    with the more popular Austrian dub DJs K & D.
      ~~~
    Refreaked (1925)
       1. Before (Herbert) . . . . . . . . . . . . . . 7:43
       2. Smile (Eddy & Dus) . . . . . . . . . . . . . 5:02
      ~~~
    Unfreaked
       1. Really Really Long Song Title <12:25>

++ END EXAMPLE ++

$Header: /home/joel/cvs/prepare-cd/prepareCD.py,v 1.4 2003/06/24 06:33:36 joel Exp $

"""
__version__='$Revision: 1.4 $'[11:-2]


from shared import *
from atomreader import *

import sys
import string
import commands
import os
import stat


MP3_ROOT_DIR = "/home/joel/mp3/"

ID3FIELD_ARTIST = 0
ID3FIELD_ALBUM = 1
ID3FIELD_TRACKNAME = 2
ID3FIELD_YEAR = 3
ID3FIELD_NUM_CONSTANTS = 4



def usage(msg=None):
    if msg is not None:
        err(msg)
    die("usage: " + os.path.basename(sys.argv[0]) +
        " dest-dir [input-file...]")

_UNPUNCT_OK_CHARS = string.lowercase + string.digits + " "
def unpunctuate(name):
    """Translate ' [A-Z]' to '_[a-z]' in <name> and remove punctionation.
    """
    name = name.lower()
    name = str(filter((lambda n: n in _UNPUNCT_OK_CHARS), name))
    name = name.replace(" ", "_")
    return name


#-----------------------------------------------------------------------------
# CD DATA CLASSES
#-----------------------------------------------------------------------------

class Track:
    """A pointer to an MP3 file and some info about it.
    """

    def constructFromInput(atomReader, trackNum, year):
        atom = atomReader.peekAtom()
        if not isinstance(atom, TrackAtom):
            return None
        atomReader.readAtom()  # eat the atom we looked at
        track = Track(trackNum, atom.fileName, atom.length,
                      year or atom.year)
        return track
    constructFromInput = staticmethod(constructFromInput)

    def __init__(self, trackNum, mp3, length, year=None):
        if not mp3.startswith("/"):
            mp3 = MP3_ROOT_DIR + mp3
        
        self._trackNum = trackNum # the number of this track within a folder
        self._mp3 = mp3 # full path to mp3 file
        self._length = length # string such as "2:35"
        self._year = year or self.getId3Field(ID3FIELD_YEAR)
        # ^ string such as "1999"

    def getYear(self):
        return self._year

    def getId3Field(self, fieldNumber):
        """Return the a field stored in the ID3 tag of an MP3 file.

        ID3 info is cached for efficiency.

        """
        try:
            return self.__id3Info[fieldNumber]
        except AttributeError:
            # Create cache var self.__id3Info

            # The order of '%n's below matches the order of the ID3FIELD_
            # constants.
            cmd = "mp3info -p '%a!_!%l!_!%t!_!%y' " + self._mp3
            status, out = commands.getstatusoutput(cmd)
            if status != 0:
                die(`cmd` + " failed, output was: " + `out`)
            self.__id3Info = out.split("!_!")
            assert len(self.__id3Info) == ID3FIELD_NUM_CONSTANTS

            if self.__id3Info[ID3FIELD_YEAR] in ("0", ""):
                self.__id3Info[ID3FIELD_YEAR] = None

            return self.__id3Info[fieldNumber]

    def createImage(self, folderDir):
        destName = folderDir + "%02d_"%self._trackNum + \
                   unpunctuate(self.getId3Field(ID3FIELD_TRACKNAME)) + \
                   ".mp3"
        os.link(self._mp3, destName)

    def toText(self, listingFlags, prefix="    "):

        # First create a one-line string containing the track info.
        line = prefix + "%4d."%self._trackNum
        if self._year is not None and \
           not (listingFlags & LISTINGFLAG_SUPPRESS_TRACK_YEAR):
            line += " -" + self._year + "-"
        if listingFlags & LISTINGFLAG_ARTIST_ON_EACH_LINE:
            line += " " + self.getId3Field(ID3FIELD_ARTIST) +":"
        if listingFlags & LISTINGFLAG_ALBUM_ON_EACH_LINE:
            line += " " + self.getId3Field(ID3FIELD_ALBUM) +" -"
        line += " " + self.getId3Field(ID3FIELD_TRACKNAME)
        line += " <" + self._length +">"

        # Now break the string into multiple lines, if it is too long.
        return fillText(line, prefix + "    ")

class Folder:
    """A folder contains tracks.
    """

    def constructFromInput(atomReader):
        atom = atomReader.peekAtom()
        if not isinstance(atom, FolderHeadingAtom):
            return None
        folder = Folder(atom.folderName)
        atomReader.readAtom()  # eat the atom we looked at

        atom = atomReader.peekAtom()
        if isinstance(atom, CommentAtom):
            folder._comment = atom.commentText
            atomReader.readAtom()  # eat the atom we looked at

        albumYear = None
        trackNum = 1
        while 1:
            atom = atomReader.peekAtom()
            if isinstance(atom, TrackAtom):
                track = Track.constructFromInput(atomReader, trackNum,
                                                 albumYear)
                if track is not None:
                    folder._tracks.append(track)
                    trackNum += 1
            elif isinstance(atom, YearAtom):
                albumYear = atom.yearText
                atomReader.readAtom()  # eat the atom we looked at
            else:
                return folder
       
    constructFromInput = staticmethod(constructFromInput)

    def __init__(self, name):
        self._name = name
        self._comment = None

        self._tracks = []

    def createImage(self, folderPrefix):
        folderDir = folderPrefix + unpunctuate(self._name) + "/"
        os.mkdir(folderDir)
        for track in self._tracks:
            track.createImage(folderDir)

    def writeText(self, out, listingFlags, prefix="    "):

        addAlbumNames = listingFlags & LISTINGFLAG_HEADING_PER_ALBUM
        prevAlbum = ""

        title = "[[ " + self._name + " ]]"
        out.write("\n")
        out.write(prefix + title + "\n")

        if self._comment is not None:
            out.write(prefix + "  ~~~\n")
            out.write(fillText(prefix + self._comment, prefix))

        if not addAlbumNames:
            out.write(prefix + "  ~~~\n")

        for track in self._tracks:
            if addAlbumNames:
                album = track.getId3Field(ID3FIELD_ALBUM)
                year = track.getYear()
                if album != prevAlbum:
                    out.write(prefix + "  ~~~\n")
                    out.write(prefix + album)
                    if year is not None:
                        out.write(" (" + year + ")")
                    out.write("\n")
                    prevAlbum = album
            out.write(track.toText(listingFlags, prefix))

class Section:
    """A section contains folders.
    """

    def constructFromInput(atomReader):
        atom = atomReader.peekAtom()
        if not isinstance(atom, SectionHeadingAtom):
            return None
        section = Section(atom.sectionNum, atom.listingFlags)
        atomReader.readAtom()  # eat the atom we looked at

        atom = atomReader.peekAtom()
        if isinstance(atom, CommentAtom):
            section._comment = atom.commentText
            atomReader.readAtom()  # eat the atom we looked at

        while 1:
            atom = atomReader.peekAtom()
            if isinstance(atom, FolderHeadingAtom):
                folder = Folder.constructFromInput(atomReader)
                if folder is not None:
                    section._folders.append(folder)
            else:
                return section
       
    constructFromInput = staticmethod(constructFromInput)
    
    def __init__(self, sectionNum, listingFlags):
        self._sectionNum = sectionNum
        self._listingFlags = listingFlags
        self._comment = None

        self._folders = []

    def createImage(self, destDir):
        if self._sectionNum == "0":
            folderPrefix = destDir
        else:
            folderPrefix = destDir + "s" + self._sectionNum + "_-_"
        for folder in self._folders:
            folder.createImage(folderPrefix)

    def writeText(self, out, prefix=""):

        addAlbumNames = self._listingFlags & LISTINGFLAG_HEADING_PER_ALBUM
        prevAlbum = ""

        if self._sectionNum != "0":
            title = "<<< " + self._sectionNum + " >>>"
            out.write("\n")
            #out.write(prefix + len(title)*"=" + "\n")
            out.write(prefix + title + "\n")
            #out.write(prefix + len(title)*"=" + "\n")

        if self._comment is not None:
            out.write("\n")
            out.write(fillText(prefix + self._comment, prefix))

        for folder in self._folders:
            folder.writeText(out, self._listingFlags, prefix + "    ")

        out.write("\n")

class CD:
    """A CD contains sections.
    """

    def constructFromInput(atomReader):
        cd = CD()
        while 1:
            atom = atomReader.peekAtom()
            if isinstance(atom, SectionHeadingAtom):
                section = Section.constructFromInput(atomReader)
                if section is not None:
                    cd._sections.append(section)
            else:
                if atom is not None:
                    err("warning: tokens remain in input stream, " +
                        "next token is " + X().__class__.__name__)
                return cd
       
    constructFromInput = staticmethod(constructFromInput)
    
    def __init__(self):
        self._sections = []

    def createImage(self, destDir):
        os.mkdir(destDir)
        for section in self._sections:
            section.createImage(destDir)

    def writeText(self, out, prefix=""):
        for section in self._sections:
            section.writeText(out, prefix)


def main():
    destDir = sys.argv[1]
    del sys.argv[1]

    if destDir.endswith("/"):
        destDir = destDir[:-1]
    if os.path.exists(destDir):
        usage(destDir + " already exists")
    if not os.path.exists(os.path.dirname(destDir)):
        usage(os.path.dirname(destDir) + ": no such directory")
    destDir += "/"
    
    import fileinput
    atomReader = AtomReader(fileinput.input())
    cd = CD.constructFromInput(atomReader)
    if cd is None:
        die("no meaningful input")

    cd.createImage(destDir)
    outf = open(destDir + "Contents.txt", "w")
    cd.writeText(outf)
    outf.close()

if __name__ == "__main__":
    main()
