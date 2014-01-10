#!/usr/bin/env python

"""
Generate a recursive triangular pattern of circles as an OpenOffice drawing
document and open it in an OpenOffice window. Requires the odf package.
"""


import math
import os
import subprocess
from odf.opendocument import OpenDocumentDrawing
from odf.style import Style, MasterPage, PageLayout, PageLayoutProperties, \
   GraphicProperties, DrawingPageProperties
from odf.draw import Page, G, Polygon, Rect, Circle

VIEWER_PATH = "\Program Files\OpenOffice.org 3\program\soffice.exe"
DRAWING_FILE = "out"
DRAWING_EXT = ".odg"


def main():
    # If an old drawing exists, remove it.
    if os.access(DRAWING_FILE + DRAWING_EXT, os.F_OK):
        os.remove(DRAWING_FILE + DRAWING_EXT)

    make_document()

    # Start the program (in a new window) to view the created file.
    subprocess.check_call([VIEWER_PATH, DRAWING_FILE + DRAWING_EXT])


def make_document():
    # Create the document
    doc = OpenDocumentDrawing()

    # Create the drawing page
    dpstyle = Style(family="drawing-page", name="DP1")
    dpstyle.addElement(DrawingPageProperties(backgroundsize="border",
                                             fill="none"))
    doc.automaticstyles.addElement(dpstyle)

    # Create page layout specifying dimensions
    plstyle = PageLayout(name="PM1")
    plstyle.addElement(PageLayoutProperties(margin="1in", pageheight="8.5in", pagewidth="11in", printorientation="landscape"))
    doc.automaticstyles.addElement(plstyle)

    # Create a master page
    masterpage = MasterPage(stylename=dpstyle, name="Default", pagelayoutname=plstyle)
    doc.masterstyles.addElement(masterpage)

    # Create a page to contain the drawing
    drawpage = Page(masterpagename=masterpage, name="page1", stylename=dpstyle)
    doc.drawing.addElement(drawpage)

    # Create a style for the circles
    circlestyle = Style(family="graphic", name="solid")
    circlestyle.addElement(
        GraphicProperties(fill="none", stroke="#000000", strokewidth="0.01in"))
    doc.automaticstyles.addElement(circlestyle)

    group=G()
    drawpage.addElement(group)

    circlePlotter = CirclePlotter(circlestyle)
    
    #nestedTriangle = NestedTriangle(group, circlePlotter, 0.25, 0.5, 0.5)
    #nestedTriangle = NestedTriangle(group, circlePlotter, 0.125, 0.75, 0.5)
    nestedTriangle = NestedTriangle(group, circlePlotter, 0.19, 0.625, 0.39)
    nestedTriangle.draw(5.5, 4.25, 3.5, 6)


    # Save the work
    doc.save(DRAWING_FILE, True)


class CirclePlotter:
    def __init__(self, style):
        self.style = style

    def draw(self, group, x, y, r):
        group.addElement(make_circle(x, y, r, self.style))


#TODO later: abstract drawing of branch graphic and possibly leaf graphic
class NestedTriangle:
    def __init__(self, group, plotter, center_size_ratio=0.25,
                 subarea_size_ratio=0.5, subarea_offset_ratio=0.5):
        self.group = group
        self.plotter = plotter
        self.center_size = center_size_ratio
        self.subarea_size = subarea_size_ratio
        self.subarea_offset = subarea_offset_ratio

    def draw(self, x, y, r, depth):
        # TODO: Possibly scale radius down based on subarea size/offset
        self.recursive_draw(x, y, r, depth)

    def recursive_draw(self, x, y, r, depth):
        self.plotter.draw(self.group, x, y, r*self.center_size)
        if depth == 1:
            return
        subarea_size = r * self.subarea_size
        subarea_offset = r * self.subarea_offset
        for i in range(3):
            theta = math.pi*(0.5+2*i)/3
            subx, suby = polar_to_xy(x, y, subarea_offset, theta)
            self.recursive_draw(subx, suby, subarea_size, depth-1)


def make_circle(cx, cy, r, style):
    x = to_inches(cx - r)
    y = to_inches(cy - r)
    height = width = to_inches(2*r)
    return Circle(x=x, y=y, height=height, width=width, stylename=style)


def to_inches(val):
    return "%0.5fin" % val


def polar_to_xy(originx, originy, r, theta):
    x = originx + (r * math.cos(theta))
    y = originy + (r * math.sin(theta))
    return (x, y)


if __name__ == '__main__':
    main()
