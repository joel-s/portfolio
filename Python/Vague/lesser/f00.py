"""piddletest.py

This module puts the various PIDDLE backends through their paces.
"""

import piddle
import math
from math import pi
from math import sin
from math import cos



def drawBranch(canvas, x,y, t,ts, r,rs, i):
	x0 = x + cos(t)*r
	y0 = y + sin(t)*r
	rp = r+rs
	tp1 = t - ts/2
	tp2 = t + ts/2
	canvas.drawCurve(x0,y0, x0,y0, x+cos(tp1)*r,y+sin(tp1)*r,
			 x + cos(tp1)*rp, y + sin(tp1)*rp)
	canvas.drawCurve(x0,y0, x0,y0, x+cos(tp2)*r,y+sin(tp2)*r,
			 x + cos(tp2)*rp, y + sin(tp2)*rp)
	if i > 0:
		drawBranch(canvas, x,y, tp1,ts/2, rp,rs*2/3, i-1)
		drawBranch(canvas, x,y, tp2,ts/2, rp,rs*2/3, i-1)

def drawFig(canvas, x0,y0, s):
	saver = piddle.StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultLineColor = piddle.black
	canvas.defaultLineWidth = 2

	for i in range(12):
		if i == 1: canvas.defaultLineColor = piddle.black
		drawBranch(canvas, x0,y0, i*pi/6,pi/12, s*0.9,s*-0.30, 8)
	
#	canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
	
	return canvas

