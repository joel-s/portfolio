"""piddletest.py

This module puts the various PIDDLE backends through their paces.
"""

import piddle
import math
from math import pi
from math import sin
from math import cos

def xc(x0,t,r):
	return x0 + t*cos(r)
def yc(y0,t,r):
	return y0 + t*sin(r)

def polarToXY(x,y,t,r):
	t0 = math.floor(t*3/pi) * pi/3
	t1 = t0 + pi/3
	x0,y0 = x+r*cos(t0),y+r*sin(t0)
	x1,y1 = x+r*cos(t1),y+r*sin(t1)
	w1 = (t - t0) * 3/pi
	w0 = 1.0 - w1
	return x0*w0 + x1*w1, y0*w0 + y1*w1

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


foo = 0
def drawBranch(canvas, x,y, t,ts, r,rs, imax,i=1):
	global foo

	rp = r+rs
	tp1 = t - ts/2
	tp2 = t + ts/2

	tw = 0.3/pow(i,2)
	tpw = 0.3/pow(i+1,2)
	C = piddle.figureCurve
	L = piddle.figureLine

	if i > 6:
		fc = piddle.black
	else:
		fc = piddle.white

## 	polarFig = [
## 		(C, t,r, t,r, tp1,r, tp1,rp),
## 		(L, tp1,rp, tp1,rmax),
## 		(L, t-ts/6,rmax, t+ts/6,rmax),
## 		(L, tp2,rmax, tp2,rp),
## 		(C, tp2,rp, tp2,r, t,r, t,r),
## 		]
## 	canvas.drawFigure(polarFigToXY(x,y,polarFig),
## 			  fillColor=fc)
	polarFig1 = [
		(L, t-tw,r, tp1-tpw,rp),
		(L, tp1+tpw,rp, t+tw,r),
		]
	polarFig2 = [
		(L, t-tw,r, tp2+tpw,rp),
		(L, tp2-tpw,rp, t+tw,r),
		]
	canvas.drawFigure(polarFigToXY(x,y,polarFig1),
			  fillColor=piddle.black)
	canvas.drawFigure(polarFigToXY(x,y,polarFig2),
			  fillColor=piddle.black)


	if i <= imax:
		drawBranch(canvas, x,y, tp1,ts/2, rp,rs*0.5, imax,i+1)
		drawBranch(canvas, x,y, tp2,ts/2, rp,rs*0.5, imax,i+1)
	elif foo == 0:
		print rp
		foo = 1

def drawFig(canvas, x0,y0, s):
	global rmax

	saver = piddle.StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultLineColor = piddle.black
	canvas.defaultLineWidth = 0

	ITER = 6

	rmax = s * (0.15 + 0.22*(1-math.pow(0.6, ITER+1))/(1-0.6))
	print rmax
	router = rmax*1.25
	rinner = rmax*0.995
	
## 	canvas.drawEllipse(x0-router,y0-router,
## 			   x0+router,y0+router,
## 			   fillColor=piddle.black)
## 	canvas.drawEllipse(x0-rinner,y0-rinner,
## 			   x0+rinner,y0+rinner,
## 			   fillColor=piddle.white)

	for i in range(6):
		if i == 1: canvas.defaultLineColor = piddle.black
		drawBranch(canvas, x0,y0, i*pi/3+pi/6,pi/6,
			   s*0.15,s*0.22,
			   ITER)
	
#	canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
	
	return canvas

