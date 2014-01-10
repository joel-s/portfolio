import piddle
import math
from math import pi
from math import sin
from math import cos

def xc(x0,t,r):
    return x0 + t*cos(r)
def yc(y0,t,r):
    return y0 + t*sin(r)

def polarToXY(x0,y0,t,r):
    r += r*cos(3*t)/9
    r *= 0.7
    return (x0 + r*cos(t), y0 + r*sin(t))

def polarFigToXY(x,y,fig):
    res = []
    for seg in fig:
        segp,rem = list(seg[0:1]),list(seg[1:])
        while rem != []:
            xc,yc = polarToXY(x,y, rem[0],rem[1])
            segp.append(xc)
            segp.append(yc)
            rem = rem[2:]
        res.append(segp)
    return res

DEGREES = 180.0 / math.pi  # degrees per radian

def roundedSeg(x0,y0,r0, x1,y1,r1):
    dx,dy = x1-x0, y1-y0
    d = math.sqrt(dx*dx + dy*dy)  # d = dist between pts
    if r0-r1 >= d:
        # line is circle: x0,y0,r0
        return [(piddle.figureArc, x0-r0, y0-r0, x0+r0, y0+r0, 0, 360)]
    if r1-r0 >= d:
        # line is circle: x1,y1,r1
        return [(piddle.figureArc, x1-r1, y1-r1, x1+r1, y1+r1, 0, 360)]
        
    t = math.atan2(dx,dy) * DEGREES
    # sin(dt) = (r1-r0) / d
    dt = math.asin((r1-r0) / d) * DEGREES
    return [
        (piddle.figureArc, x0-r0, y0-r0, x0+r0, y0+r0, t+dt, 180-2*dt),
        (piddle.figureArc, x1-r1, y1-r1, x1+r1, y1+r1, 180+t-dt, 180+2*dt),
        ]


foo = 0
def drawBranch(canvas, x,y, t,ts, r,rs, imax,i=1):
    global foo

    rp = r+rs
    tp1 = t + (pow(2,i)+0)*ts/3
    tp2 = t + (pow(2,i)+2)*ts/3
    tp3 = t + (pow(2,i)+4)*ts/3

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
##     elif foo == 0:
##         print rp
##         foo = 1

def drawFig(canvas, x0,y0, s):
    global rmax

    saver = piddle.StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
    canvas.defaultLineColor = piddle.black
    canvas.defaultLineWidth = 0

    ITER = 60

    rmax = s * (0.15 + 0.22*(1-math.pow(0.6, ITER+1))/(1-0.6))
##    print rmax
    router = rmax*1.25
    rinner = rmax*0.995
    
##  canvas.drawEllipse(x0-router,y0-router,
##             x0+router,y0+router,
##             fillColor=piddle.black)
##  canvas.drawEllipse(x0-rinner,y0-rinner,
##             x0+rinner,y0+rinner,
##             fillColor=piddle.white)

    t1 = 0
    dt = 2*math.pi / ITER
    for i in range(ITER):
            t2 = t1 + dt
            r = s * (2 + i % 2)/4
            r1 = s * (3 + 2*(i%2))/333
            r2 = s * (5 - 2*(i%2))/333
            x1,y1 = polarToXY(x0,y0, t1,r)
            x2,y2 = polarToXY(x0,y0, t2,r)
##             print (x1,y1,r1, x2,y2,r2)
##             print roundedSeg(x1,y1,r1, x2,y2,r2)
            canvas.drawFigure(roundedSeg(x1,y1,r1, x2,y2,r2),
                              fillColor=piddle.black)
            t1 += dt
            
##         if i == 1: canvas.defaultLineColor = piddle.black
##         drawBranch(canvas, x0,y0, i*pi/3+pi/6,pi/6,
##                s*0.15,s*0.22,
##                ITER)
    
#   canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
    
    return canvas

# Local Variables:
# tab-width: 4
# indent-tabs-mode: nil
# End:
