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

def polarFigToXY(x,y,fig):
	res = []
	for seg in fig:
		segp,rem = list(seg[0:1]),list(seg[1:])
		while rem != []:
			segp.append(x+cos(rem[0])*rem[1])
			segp.append(y+sin(rem[0])*rem[1])
			rem = rem[2:]
		res.append(segp)
	return res

def drawBranch(canvas, x,y, t,ts, r,rs, i):
	rp = r+rs
	tp1 = t - ts/2
	tp2 = t + ts/2

	rw = rs/8
	tw = ts/8
	C = piddle.figureCurve
	polarFig = [
		(C, tp1+tw,rp, tp1+tw,r+rw, t,r+rw, t,r+rw),
		(C, t,r-rw, t,r-rw, tp2+tw,r-rw, tp2+tw,rp),
		(C, tp2-tw,rp, tp2-tw,r+rw, t,r+rw, t,r+rw),
		(C, t,r-rw, t,r-rw, tp1-tw,r-rw, tp1-tw,rp),
		]
#	print polarFigToXY(x,y,polarFig)
	canvas.drawFigure(polarFigToXY(x,y,polarFig),
			  fillColor=piddle.black)
	if i > 0:
		drawBranch(canvas, x,y, tp1,ts/2, rp,rs*0.45, i-1)
		drawBranch(canvas, x,y, tp2,ts/2, rp,rs*0.45, i-1)

def drawFig(canvas, x0,y0, s):
	saver = piddle.StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultLineColor = piddle.black
	canvas.defaultLineWidth = 0.1

	for i in range(12):
		if i == 1: canvas.defaultLineColor = piddle.black
		drawBranch(canvas, x0,y0, i*pi/6,pi/12, s*0.75,s*-0.35, 9)
	
#	canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
	
	return canvas

