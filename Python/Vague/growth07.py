import piddle
import math
from math import pi
from math import sin
from math import cos
import libvague
from libvague import deg
from libvague import squiggleFig



def drawBranch(canvas, m, r,ri,rf, t,tr, w, imax,i=1):
    """Draw a branch (recursive).

    m = mapper
    r = radius of the root of this branch
    ri = radius increment for this section
    rf = radius increment factor (for recursive invocations)
    t,tr = branch occupies angle range from t-tr to t+tr
    w = width of branch

    """
    rp = r+ri
    tp1 = t - tr/2
    tp2 = t + tr/2

    rp2a = r+ri*0.6
    tp2a = t + tr*0.45

    x0,y0 = m.xy(r,t)
    x1,y1 = m.xy(rp,tp1)
    x2,y2 = m.xy(rp,tp2)
    x2a,y2a = m.xy(rp2a,tp2a)

    skew = pi/7

    if i % 2:
        canvas.defaultLineColor = piddle.red
        canvas.defaultFillColor = piddle.red
    else:
        canvas.defaultLineColor = piddle.black
        canvas.defaultFillColor = piddle.black

    canvas.defaultLineWidth = w
    libvague.drawSquiggle(canvas,
                          x0,y0,ri*0.5,m.out(r,t)+skew,w,
                          x1,y1,-ri*0.5,m.out(rp,tp1)+skew,w)

    libvague.drawSquiggle(canvas,
                          x0,y0,ri*0.2,m.out(r,t)+skew,w,
                          x2a,y2a,-ri*0.2,m.out(rp2a,tp2a)-skew*0.7,w)
    libvague.drawSquiggle(canvas,
                          x2a,y2a,ri*0.2,m.out(rp2a,tp2a)-skew*0.7,w,
                          x2,y2,-ri*0.2,m.out(rp,tp2)+skew,w)
    
    if i <= imax:
        drawBranch(canvas, m, rp,ri*rf,rf, tp1,tr/2, w, imax,i+1)
        drawBranch(canvas, m, rp,ri*rf,rf, tp2,tr/2, w, imax,i+1)

def drawFig(canvas, x0,y0, s):
    global rmax

    # leave canvas state as you found it, restores state when leaves scope
    saver = piddle.StateSaver(canvas)

    canvas.defaultLineColor = piddle.black
    canvas.defaultLineWidth = 0
    canvas.setCapStyle("round")


##    canvas.drawFigure(
##        squiggleFig(x0,y0-s/2,s/4,1,s/10,
##                    x0,y0+s/2,-s/4,1,s/10)
##        )
##    apply(canvas.drawEllipse, circleBox(x0-s/2,y0+s/2,s/10))
###   canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )

    iter = 8
    rf = 0.7
    r0 = 0 * s
    r1 = 0.25 * s

    rmax = r0 + r1*(1-math.pow(rf, iter+1))/(1-rf)
    router = rmax*1.05
    rinner = rmax*0.995
    
    canvas.drawEllipse(x0-router,y0-router,
               x0+router,y0+router,
               fillColor=piddle.black)
    canvas.drawEllipse(x0-rinner,y0-rinner,
               x0+rinner,y0+rinner,
               fillColor=piddle.white)

    m = libvague.PolarMapper(x0,y0)

    for i in range(3):
        if i == 1: canvas.defaultLineColor = piddle.black
        drawBranch(canvas, m, r0,r1,rf,
                   i*pi*2/3,pi/3,
                   s/100,
                   iter)

    return canvas

