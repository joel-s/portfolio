import math
from math import pi
from math import sin
from math import cos
import piddle

DEG_PER_RAD = 180.0 / pi
def deg(t):
    return t * DEG_PER_RAD

def xyrt(x,y, r,t):
    """Add two vectors together and return x,y.

    The first vector is given in coordinates; the second vector is given in
    polar coordinates.

    """
    return (x+r*cos(t), y+r*sin(t))

def fixPolar(r,t):
    if r >= 0:
        return r,t
    else:
        return -r,t+pi

def circleBox(x,y,r):
    """Return the coordinates of the box enclosing a circle."""
    return x-r,y-r,x+r,y+r
    
def squiggleFig(x1,y1,d1,a1,w1, x2,y2,d2,a2,w2):
    """Return a rounded bezier curve -- something like ~.

    This is the naive implementation, using 2 identical slightly-offset
    bezier curves to outline the figure. It looks uneven or calligraphic.

    xn,yn = endpoints
    dn = distance of control point from endpoint
    an = angle (in radians) of control point from endpoint
    wn = width (thickness) of curve at endpoint
    
    """
    # make sure the distances are positive
    d1,a1 = fixPolar(d1,a1)
    d2,a2 = fixPolar(d2,a2)
    
    r1 = w1/2
    r2 = w2/2
    
    x1a,y1a = xyrt(x1,y1, r1,a1+pi/2)
    x1b,y1b = xyrt(x1,y1, r1,a1-pi/2)

    x2a,y2a = xyrt(x2,y2, r2,a2-pi/2)
    x2b,y2b = xyrt(x2,y2, r2,a2+pi/2)

    C = piddle.figureCurve
    A = piddle.figureArc # args: x1,y1,x2,y2, -t0, extent

    return [
        (C,) +(x1a,y1a) +xyrt(x1a,y1a, d1,a1)
            +xyrt(x2a,y2a, d2,a2) +(x2a,y2a),
        (A, x2-r2,y2-r2, x2+r2,y2+r2, deg(pi/2-a2), 180),
        (C,) +(x2b,y2b) +xyrt(x2b,y2b, d2,a2)
            +xyrt(x1b,y1b, d1,a1) +(x1b,y1b),
        (A, x1-r1,y1-r1, x1+r1,y1+r1, deg(pi/2-a1), 180),
        ]

def drawSquiggle(canvas, x1,y1,d1,a1,w1, x2,y2,d2,a2,w2,
                 color=piddle.black):
    """Draw a rounded bezier curve -- something like ~.

    xn,yn = endpoints
    dn = distance of control point from endpoint
    an = angle (in radians) of control point from endpoint
    wn = width (thickness) of curve at endpoint

    Caller should set defaultFillColor == defaultLineColor
    
    """
    # make sure the distances are positive
    d1,a1 = fixPolar(d1,a1)
    d2,a2 = fixPolar(d2,a2)

    if w1 == w2:
        apply(canvas.drawCurve,
              (x1,y1) +xyrt(x1,y1, d1,a1)
              +xyrt(x2,y2, d2,a2) +(x2, y2),
              {"edgeWidth": w1, "edgeColor": color,
               "fillColor": piddle.transparent})
    else:
        not_implemented()

    # Following code not needed yet.

##    # Draw rounded end caps. Last 2 args are arc start (opposite sign from
##    # what you might expect) and arc extent.
##    apply(canvas.drawEllipse,
##          circleBox(x1,y1, w1),
##          {"edgeWidth": 0, "edgeColor": color, "fillColor": color})
##    apply(canvas.drawEllipse,
##          circleBox(x2,y2, w2),
##          {"edgeWidth": 0, "edgeColor": color, "fillColor": color})

    return canvas


class Mapper:
    """Abstract base class for mappers.

    A mapper maps from a virtual coordinate system with origin 0,0 to
    coordinates on a page. The virtual coordinates are named r,t -- they are
    usually intended as polar coordinates but don't have to be.

    --- Base classes must define these functions ---

      - xy(r,t) returns x,y corresponding to r,t

      - out(r,t) returns the angle in radians of the 'out' direction at
        point r,t  

    """
    pass

##    ## this concept only works for (boring) figureLine
##    def mapFigure(x,y,fig):
##        res = []
##        for seg in fig:
##            segp,rem = list(seg[0:1]),list(seg[1:])
##            while rem != []:
##                xc,yc = polarToXY(x,y, rem[0],rem[1])
##                segp.append(xc)
##                segp.append(yc)
##                rem = rem[2:]
##            res.append(segp)
##        return res


class PolarMapper(Mapper):
    """Map from polar to x,y coordinates.
    """
    def __init__(self, x0,y0, rs=1.0, t0=0.0,ts=1.0):
        """Initailize polar mapper.

        x0,y0 = origin coords in destination space
        rs = scaling factor for radii
        t0 = offset to angles
        ts = scaling factor for angles

        """
        self.x0 = x0
        self.y0 = y0
        self.rs = rs
        self.t0 = t0
        self.ts = ts
        
    def xy(self, r,t):
        r = r*self.rs
        t = self.t0 + t*self.ts
        return self.x0 + r*cos(t), self.y0 + r*sin(t)

    def out(self, r,t):
        return self.t0 + t*self.ts

class WedgeMapper(Mapper):
    def polarToXY(x0,y0,t,r):
        r += r*cos(3*t)/9
        r *= 0.7
        return (x0 + r*cos(t), y0 + r*sin(t))

##def polarToXY(x,y,t,r):
##    T = pi/6
##    t0 = math.floor(t/T) * T
##    t1 = t0 + T
##    x0,y0 = x+r*cos(t0),y+r*sin(t0)
##    x1,y1 = x+r*cos(t1),y+r*sin(t1)
##    w1 = (t - t0) / T
##    w0 = 1.0 - w1
##    return x0*w0 + x1*w1, y0*w0 + y1*w1

