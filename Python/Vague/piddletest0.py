"""piddletest.py

This module puts the various PIDDLE backends through their paces.
"""

import pagesizes
from piddle import *
import string
import sys
import math
from math import pi
from math import sin
from math import cos

backends = ['piddlePDF','piddlePIL','piddleVCR','piddleTK',
		    'piddlePS','piddleAI','piddleQD','piddleGL', 'piddleWX']
backends.sort()

#----------------------------------------------------------------------
# note, these tests do not flush() the canvas
#----------------------------------------------------------------------
def minimal(canvasClass):
	"""Just a very basic test of line drawing and canvas size."""
	canvas = canvasClass(pagesizes.A6, "testA")		# A6 is a quarter page
	drawMinimal(canvas)
	return canvas

def drawMinimal(canvas):
	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	size = canvas.size	# (actual size *may* differ from requested size)
	canvas.defaultLineColor = green
	canvas.drawLine(1,1,size[0]-1,size[1]-1)
	canvas.drawLine(1,size[1]-1,size[0]-1,1)
	canvas.drawRect(1,1,size[0]-1,size[1]-1, edgeWidth=5)

	return canvas

#----------------------------------------------------------------------
def basics(canvasClass):
	"""A general test of most of the drawing primitives except images and strings."""
	canvas = canvasClass((400,400), "test-basics")
	return drawBasics(canvas)


def drawTree(canvas, x,y, scale, t, tscale, i):
	xp = x + cos(t)*scale/9
	yp = y + sin(t)*scale/9
	canvas.drawLine(x, y, xp, yp)
	if i > 0:
		drawTree(canvas, xp,yp, scale*8/9, t - tscale, tscale*6/7, i-1)
		drawTree(canvas, xp,yp, scale*8/9, t + tscale, tscale*6/7, i-1)

def drawBasics(canvas):
	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultLineColor = black
	canvas.defaultLineWidth = 2

	for i in range(6):
		drawTree(canvas, 200.0,200.0, 250.0, i*pi/3, pi/16.5, 10)
	
#	canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
	
	return canvas


#----------------------------------------------------------------------
def advanced(canvasClass):
	"""A general test of most of the drawing primitives except images and strings."""
	canvas = canvasClass((400,400), "test-basics")
	return drawBasics(canvas)


def drawBranch(canvas, x,y, t,ts, r,rs, i):
	x0 = x + cos(t)*r
	y0 = y + sin(t)*r
	rp = r+rs
	tp1 = t - ts/2
	tp2 = t + ts/2
	canvas.drawLine(x0, y0, x + cos(tp1)*rp, y + sin(tp1)*rp)
	canvas.drawLine(x0, y0, x + cos(tp2)*rp, y + sin(tp2)*rp)
	if i > 0:
		drawBranch(canvas, x,y, t-ts/2,ts/2, rp,rs*4/5, i-1)
		drawBranch(canvas, x,y, t+ts/2,ts/2, rp,rs*4/5, i-1)

def drawAdvanced(canvas):
	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultLineColor = black
	canvas.defaultLineWidth = 2

	for i in range(3):
		drawBranch(canvas, 200.0,200.0, i*2*pi/3,pi/3, 0.0,40.0, 8)
	
#	canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
	
	return canvas

def drawAdvanced2(canvas):
	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultLineColor = black
	canvas.defaultLineWidth = 2

	for i in range(6):
		drawBranch(canvas, 200.0,200.0,250.0, i*2*pi/3,pi/6, 200.0,4/5.0, 6)
	
#	canvas.drawCurve( 20,20, 100,50, 50,100, 160,160 )
	
	return canvas


#----------------------------------------------------------------------
## def advanced(canvasClass):
## 	"""A test of figures and images."""
## 	canvas = canvasClass((300,300), "test-advanced")
## 	return drawAdvanced(canvas)

## def drawAdvanced(canvas):
## 	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
## 	figure = [
## 			( figureCurve, 20,20, 100,50, 50,100, 160,160 ),
## 			( figureLine, 200,200, 250,150 ),
## 			( figureArc, 50,10, 250,150, 10,90 ) ]

## 	canvas.drawFigure(figure, fillColor=yellow, edgeWidth=4)
		
## 	try:
## 		import Image
## 	except:
## 		canvas.drawString("PIL not available!", 20,200)
## 		Image = None
	
## 	if Image:
## 		img = Image.open("python.gif")
## 		canvas.drawImage( img, 120,50,120+32,50+64 );
## 		canvas.drawImage( img, 0,210,300,210+32 );

## 	return canvas


#----------------------------------------------------------------------
def bluefunc(x):  return 1.0 / (1.0 + math.exp(-10*(x-0.6)))
def redfunc(x): return 1.0 / (1.0 + math.exp(10*(x-0.5)))
def greenfunc(x): return 1 - pow(redfunc(x+0.2),2) - bluefunc(x-0.3)

def spectrum(canvasClass):
	canvas = canvasClass((300,300), "test-spectrum")
	return drawSpectrum(canvas)

def drawSpectrum(canvas):
	"""Generates a spectrum plot; illustrates colors and useful application."""
	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	def plot(f,canvas,offset=0):
		for i in range(0,100):
			x = float(i)/100
			canvas.drawLine(i*3+offset,250, i*3+offset,250-100*f(x))
	
	def genColors(n=100):
		out = [None]*n;
		for i in range(n):
			x = float(i)/n
			out[i] = Color(redfunc(x), greenfunc(x), bluefunc(x));
		return out
	

	colors = genColors(300)

	# draw a black background for the spectrum
	canvas.drawRect( 0,0,300,100, edgeColor=black, fillColor=black )

	# draw the spectrum
	for i in range(len(colors)):
		canvas.drawLine(i,20,i,80, colors[i])

	# plot the components of the spectrum
	canvas.defaultLineColor = red
	plot(redfunc, canvas)

	canvas.defaultLineColor = blue
	plot(bluefunc, canvas, 1)

	canvas.defaultLineColor = green
	plot(greenfunc, canvas, 2)
	
	return canvas

#----------------------------------------------------------------------
def strings(canvasClass):
	canvas = canvasClass( size=(400,400), name="test-strings" )
	return drawStrings(canvas)


def CenterAndBox(canvas, s, cx=200, y=40):
	"tests string positioning, stringWidth, fontAscent, and fontDescent"
	canvas.drawLine(cx,y-30, cx,y+30, color=yellow)
	w = canvas
	w = canvas.stringWidth(s)

	canvas.drawLine(cx-w/2, y, cx+w/2, y, color=red)
	canvas.drawString(s, cx-w/2, y )
	canvas.defaultLineColor = Color(0.7,0.7,1.0)	# light blue
	canvas.drawLine(cx-w/2, y-20, cx-w/2, y+20)	# left
	canvas.drawLine(cx+w/2, y-20, cx+w/2, y+20)	# right
	asc, desc = canvas.fontAscent(), canvas.fontDescent()
	canvas.drawLine(cx-w/2-20, y-asc, cx+w/2+20, y-asc)		# top
	canvas.drawLine(cx-w/2-20, y+desc, cx+w/2+20, y+desc)	# bottom



def drawStrings(canvas):
	"""Checks font metrics, and also illustrates the standard fonts."""

	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	def Write(canvas, s, font, curs):
		if font: canvas.defaultFont = font
		text = s
		while text and text[-1] == '\n': text = text[:-1]
		canvas.drawString(text, x=curs[0], y=curs[1])
		if s[-1] == '\n':
			curs[0] = 10
			curs[1] = curs[1] + canvas.fontHeight() + canvas.fontDescent()
		else:
			curs[0] = curs[0] + canvas.stringWidth(s)
	
	
	def StandardFonts(canvas, Write):
		canvas.defaultLineColor = black
		curs = [10,70]
		for size in (12, 18):
			for fontname in ("times", "courier", "helvetica", "symbol",
							"monospaced", "serif", "sansserif"):			
				curs[0] = 10
				curs[1] = curs[1] + size*1.5
				Write(canvas, "%s %d " % (fontname,size), Font(face=fontname, size=size), curs)
				Write(canvas, "bold ", Font(face=fontname, size=size, bold=1), curs)
				Write(canvas, "italic ", Font(face=fontname, size=size, italic=1), curs)
				Write(canvas, "underline", Font(face=fontname, size=size, underline=1), curs)
	
	CenterAndBox(canvas, "spam, spam, spam, baked beans, and spam!")
	StandardFonts(canvas, Write)
	return canvas

#----------------------------------------------------------------------
def rotstring(canvasClass):
	canvas = canvasClass( (450,300), name='test-rotstring' )
	return drawRotstring(canvas)

def drawRotstring(canvas):
	"""Draws rotated strings."""
	saver = StateSaver(canvas) # leave canvas state as you found it, restores state when leaves scope
	canvas.defaultFont = Font(bold=1)
	
	canvas.defaultLineColor = (blue + white)/2
	canvas.drawLine(0,150, 300,150)
	canvas.drawLine(150,0, 150,300)
	
	s = " __albatros at "
	w = canvas.stringWidth(s)
	canvas.drawEllipse(150-w,150-w, 150+w, 150+w, fillColor=transparent)
	
	colors = [red,orange,yellow,green,blue,purple]
	cnum = 0
	for ang in range(0, 359, 30):
		canvas.defaultLineColor = colors[cnum]
		s2 = s + str(ang)
		canvas.drawString(s2, 150, 150, angle=ang)
		cnum = (cnum+1) % len(colors)

      	canvas.drawString( "This is  a\nrotated\nmulti-line string!!!", 350, 100, angle= -90, font=Font(underline=1) )
        #canvas.drawString( "This is  a\nrotated\nmulti-line string!!!", 400, 175, angle= -45, font=Font(underline=1) )
	return canvas

#----------------------------------------------------------------------
#----------------------------------------------------------------------
def tkTest(testfunc):
	# piddleTK tests are called from here because need TK's event loop
	try :
		import piddleTK
		import Tkinter
	except:
		print "A module needed for piddleTK is not available, select another backend"
		return

	root = Tkinter.Tk()
	frame = Tkinter.Frame(root)  # label='piddletestTK'

	#tkcanvas = piddleTK.TKCanvas(size=(400,400), name='piddletestTK', master = frame)
        # try new Tk canvas
        tkcanvas = piddleTK.TKCanvas(size=(400,400), name='piddletestTK', master = frame)
	bframe = Tkinter.Frame(root)

	minimalB=Tkinter.Button(bframe, text='minimal test',
				command= lambda c=tkcanvas : (c.clear(),drawMinimal(c), c.flush())).pack(side=Tkinter.LEFT)
	basicB = Tkinter.Button(bframe, text='basic test',
				command= lambda c=tkcanvas: (c.clear(),drawBasics(c),c.flush()) ).pack(side=Tkinter.LEFT)
	spectB =Tkinter.Button(bframe, text='spectrum test',
			       command= lambda c=tkcanvas: (c.clear(),drawSpectrum(c),c.flush()) ).pack(side=Tkinter.LEFT)
	stringsB = Tkinter.Button(bframe, text='strings test',
				  command= lambda c=tkcanvas:(c.clear(),drawStrings(c),c.flush()) ).pack(side=Tkinter.LEFT)
	rotstrB = Tkinter.Button(bframe, text='rotated strings test',
				 command= lambda c=tkcanvas:(c.clear(), drawRotstring(c),c.flush()) ).pack(side=Tkinter.LEFT)
	advancedB = Tkinter.Button(bframe, text='advanced test',
				   command= lambda c=tkcanvas:(c.clear(), drawAdvanced(c),c.flush() ) ).pack(side=Tkinter.LEFT)
        bframe.pack(side=Tkinter.TOP)
	frame.pack()
	# try to draw before running mainloop
	if testfunc== minimal:
		drawMinimal(tkcanvas)
	elif testfunc == basics:
		drawBasics(tkcanvas)
	elif testfunc == advanced :
		drawAdvanced(tkcanvas)
	elif testfunc == spectrum :
		drawSpectrum(tkcanvas)
	elif testfunc == strings :
		drawStrings(tkcanvas)
	elif testfunc == rotstring :
		drawRotstring(tkcanvas)
        else :
                print "Illegal testfunc handed to tkTest"
                raise "Unsupported testfunc"

        tkcanvas.flush() 
	
	root.mainloop()
	root.destroy()

#----------------------------------------------------------------------
def wxTest(testfunc):
	try :
		import piddleWX
		from wxPython.wx import wxApp
	except:
		print "A module needed for piddleWX is not available, select another backend"
		return

        global wx_app
        if not globals().has_key("wx_app"):
                class CanvasApp(wxApp):
                        "The wxApp that runs canvas.  Initializes windows, and handles redrawing"
                        def OnInit(self):
                                return 1

                wx_app = CanvasApp(0)

	# run the test, passing the canvas class and returning the canvas
	canvas = testfunc(piddleWX.WXCanvas)
	
	canvas.flush()

        # Run the main loop
        wx_app.MainLoop()


def runtest(backend, testfunc):

	# special cases:
	if backend=='piddleTK':
		tkTest(testfunc) # takes care of import, etc.
		return

	if backend=='piddleWX':
		wxTest(testfunc) # takes care of import, etc.
		return

	# import the relevant module		
	module = __import__(backend)

	# figure out the canvas class name (e.g., "PILCanvas") and get that
	canvasClass = getattr(module, backend[6:]+"Canvas")

	# run the test, passing the canvas class and returning the canvas
	canvas = testfunc(canvasClass)
	
	# do post-test cleanup
	canvas.flush()
        # handle save's here
	if backend == 'piddlePIL':
		canvas.save(format='png')		# save as a PNG file
        elif backend == 'piddleVCR':
		filename = canvas.name + ".vcr"
		canvas.save(filename)
		print filename, "saved"
        else:     # if backend == 'piddlePS' or backend== 'piddlePDF':
                canvas.save()  # should be "pass'ed" by Canvas's that don't use save


def mainLoop():
	global tests, backends
	backend = None
	test = None

	if len(sys.argv) == 2:
		runtest('piddleTK', advanced)
		sys.exit(0)
		

	while 1:
		# print backends on left, tests on right, indicate chosen one of each
		i = 0
		while i < len(backends) or i < len(tests):
			try: bstr = str(i+1) + '. ' + backends[i]
			except: bstr = ''
			try: tstr = chr(65+i) + '. ' + tests[i].__name__
			except: tstr = ''
			if i == backend: bflag = '==>'
			else: bflag = ''
			if i == test: tflag = '==>'
			else: tflag = ''
			print "%10s %-20s %10s %-20s" % (bflag, bstr, tflag, tstr)
			i = i+1		
		print
		
		inp = raw_input("Selection (0 to exit): ")
		print

		if inp == '0': return
		if inp:
			testinp = ''
			if inp[-1] in string.letters: testinp = inp[-1]
			elif inp[0] in string.letters: testinp = inp[0]
			backinp = string.join(filter(lambda x:x in '0123456789',inp))
			if backinp:
				backend = int(backinp)-1
				if backend < len(backends):
					docstr = __import__(backends[backend]).__doc__
					if docstr: print docstr
					else: print "<no doc string>"
				else: backend = None
			if testinp:
				test = ord(string.upper(testinp[0])) - ord('A')
				if test >= 0 and test < len(tests):
					docstr = tests[test].__doc__
					if docstr:
                                          print docstr
				else: test = None
		print
		
		# now, if we have a valid backend and test, run it
		if backend != None and test != None:
			runtest(backends[backend], tests[test])
		

tests = (minimal, basics, advanced, spectrum, strings, rotstring)

if __name__=='__main__':
	mainLoop()
