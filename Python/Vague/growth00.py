import piddle
import math
from math import pi
from math import sin
from math import cos


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
    """Draw a rounded bezier curve -- something like ~.

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

    x2a,y2a = xyrt(x2,y2, r2,a2+pi/2)
    x2b,y2b = xyrt(x2,y2, r2,a2-pi/2)

    C = piddle.figureCurve
    A = piddle.figureArc

    return [
        (C,) +(x1a,y1a) +xyrt(x1a,y1a, d1,a1)
            +xyrt(x2a,y2a, d2,a2) +(x2a,y2a),
        (A, x2-r2,y2-r2, x2+r2,y2+r2, deg(a2-pi/2), 180),
        (C,) +(x2b,y2b) +xyrt(x2b,y2b, d2,a2)
            +xyrt(x1b,y1b, d1,a1) +(x1b,y1b),
        (A, x1-r1,y1-r1, x1+r1,y1+r1, deg(a1-pi/2), 180),
        ]



##def xc(x0,t,r):
##    return x0 + t*cos(r)
##def yc(y0,t,r):
##    return y0 + t*sin(r)

##def polarToXY(x,y,t,r):
##    T = pi/6
##    t0 = math.floor(t/T) * T
##    t1 = t0 + T
##    x0,y0 = x+r*cos(t0),y+r*sin(t0)
##    x1,y1 = x+r*cos(t1),y+r*sin(t1)
##    w1 = (t - t0) / T
##    w0 = 1.0 - w1
##    return x0*w0 + x1*w1, y0*w0 + y1*w1

##def polarFigToXY(x,y,fig):
##    res = []
##    for seg in fig:
##        segp,rem = list(seg[0:1]),list(seg[1:])
##        while rem != []:
##            xc,yc = polarToXY(x,y, rem[0],rem[1])
##            segp.append(xc)
##            segp.append(yc)
##            rem = rem[2:]
##        res.append(segp)
##    return res


foo = 0
def drawBranch(canvas, x,y, t,ts, r,rs, imax,i=1):
    global foo

    rp = r+rs
    tp1 = t + (pow(2,i)+0)*ts/3
    tp2 = t + (pow(2,i)+2.5)*ts/3
    tp3 = t + (pow(2,i)+3.7)*ts/3

    tw = 0.3/pow(i,3)
    tpw = 0.3/pow(i+1,3)
    C = piddle.figureCurve
    L = piddle.figureLine

    if i > 6:
        fc = piddle.black
    else:
        fc = piddle.white

##  polarFig = [
##      (C, t,r, t,r, tp1,r, tp1,rp),
##      (L, tp1,rp, tp1,rmax),
##      (L, t-ts/6,rmax, t+ts/6,rmax),
##      (L, tp2,rmax, tp2,rp),
##      (C, tp2,rp, tp2,r, t,r, t,r),
##      ]
##  canvas.drawFigure(polarFigToXY(x,y,polarFig),
##            fillColor=fc)
    polarFig1 = [
        (L, t-tw,r, tp1-tpw,rp),
        (L, tp1+tpw,rp, t+tw,r),
        ]
    polarFig2 = [
        (L, t-tw,r, tp2-tpw,rp),
        (L, tp2+tpw,rp, t+tw,r),
        ]
    polarFig3 = [
        (L, t-tw,r, tp3-tpw,rp),
        (L, tp3+tpw,rp, t+tw,r),
        ]

    canvas.drawFigure(polarFigToXY(x,y,polarFig1),
              fillColor=piddle.black)
    canvas.drawFigure(polarFigToXY(x,y,polarFig2),
              fillColor=piddle.black)
    canvas.drawFigure(polarFigToXY(x,y,polarFig3),
              fillColor=piddle.black)


    if i <= imax:
        drawBranch(canvas, x,y, tp1,ts/3, rp,rs*0.5, imax,i+1)
        drawBranch(canvas, x,y, tp2,ts/3, rp,rs*0.5, imax,i+1)
        drawBranch(canvas, x,y, tp3,ts/3, rp,rs*0.5, imax,i+1)
    elif foo == 0:
        print rp
        foo = 1

def drawFig(canvas, x0,y0, s):
    global rmax

    # leave canvas state as you found it, restores state when leaves scope
    saver = piddle.StateSaver(canvas)

    canvas.defaultLineColor = piddle.black
    canvas.defaultLineWidth = 0

    ITER = 6

    canvas.drawFigure(
        squiggleFig(x0,y0-s/2,s/4,1,s/10,
                    x0,y0+s/2,-s/4,1,s/10)
        )

    apply(canvas.drawEllipse, circleBox(x0-s/2,y0+s/2,s/10))

    return canvas

    

##    rmax = s * (0.15 + 0.22*(1-math.pow(0.6, ITER+1))/(1-0.6))
##    print rmax
##    router = rmax*1.25
##    rinner = rmax*0.995
    
####  canvas.drawEllipse(x0-router,y0-router,
####             x0+router,y0+router,
####             fillColor=piddle.black)
####  canvas.drawEllipse(x0-rinner,y0-rinner,
####             x0+rinner,y0+rinner,
####             fillColor=piddle.white)

##    for i in range(6):
##        if i == 1: canvas.defaultLineColor = piddle.black
##        drawBranch(canvas, x0,y0, i*pi/3+pi/6,pi/6,
##               s*0.15,s*0.22,
##               ITER)
    
###   canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
    
##    return canvas

