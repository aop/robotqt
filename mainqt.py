import sys

from PyQt4 import QtGui, QtCore
from math import sin, cos, radians, degrees
import numpy as np

#Debug boolean
debug = False

class Robot(QtGui.QWidget):
	xOffset = 300
	yOffset = 350
	angle1 = 0
	angle2 = 0
	angle3 = 0
	length1=100
	length2=50
	length3=25
	xend = 0
	yend = 0
	numofJoints = 2
	mousePressed = False
	clickPoints = []

	#angle1calculated = QtCore.pyqtsignal(float)
	#angle2calculated = QtCore.Signal(float)
	#angle3calculated = QtCore.Signal(float)

	def __init__(self,parent):
		super(Robot,self).__init__(parent)
		self.mouseTracking = True


	def calcFKinematics(self):
		startpoints = np.array([0,0,0,1])
		f1 = self.createMatrix(radians(self.angle1),0)
		f2 = self.createMatrix(radians(self.angle2),self.length1)
		f3 = self.createMatrix(radians(self.angle3),self.length2)
		f4 = self.createMatrix(radians(0),self.length3)
		t02 = f1.dot(f2)
		t03 = t02.dot(f3)
		t04 = t03.dot(f4)
		points = []
		points.append(startpoints)
		points.append(t02.dot(startpoints))
		points.append(t03.dot(startpoints))
		points.append(t04.dot(startpoints))
		return points

	def calcIKinematics(self,x,y):
		#print("np.sqrt: %f > %f" % (np.sqrt(x**2+y**2),self.length1+self.length2))
		if(np.sqrt(x**2+y**2)) > (self.length1+self.length2):
			print("Too far away")
			return
		if debug:
			print((x,y))
			print("%f/%f = %f "%((x**2+y**2-(self.length1)**2-(self.length2)**2),(2*self.length1*self.length2),(x**2+y**2-(self.length1)**2-(self.length2)**2)/(2*self.length1*self.length2)))
		angle2=np.arccos((x**2+y**2-(self.length1)**2-(self.length2)**2)/(2*self.length1*self.length2))
		beta = np.arctan2(y,x)
		xii = np.arccos((x**2+y**2+self.length1**2-self.length2**2)/(2*self.length1*np.sqrt(x**2+y**2)))
		if angle2 < 0:
			angle1 = beta - xii
		else:
			angle1 = beta + xii
		self.angle1 = degrees(angle1)
		self.angle2 = degrees(angle2)
		if debug:
			print((self.angle1,self.angle2))
		return (self.angle1,self.angle2)

	def paintEvent(self,event):
		painter = QtGui.QPainter()
		painter.begin(self)

		#painter.setWindow(QtCore.QRect(0,0,self.height(),self.width()))
		points = self.calcFKinematics()
		for i in range(1,self.numofJoints+1):
			painter.setPen(QtCore.Qt.white)			
			self.drawArm1(painter,points[i-1],points[i])
			painter.setBrush(QtCore.Qt.red)
			painter.setPen(QtCore.Qt.red)
			painter.drawEllipse(QtCore.QPoint(self.xOffset+points[i][0],self.yOffset-points[i][1]),2,2)
		painter.setBrush(QtCore.Qt.green)
		painter.setPen(QtCore.Qt.green)
		painter.drawEllipse(QtCore.QPoint(self.xOffset,self.yOffset),2,2) #Draw start of robot green
		painter.drawEllipse(QtCore.QPoint(0,0),2,2) #Draw origin green
		#for p in self.clickPoints:
		#	painter.drawEllipse(QtCore.QPoint(p[0],p[1]),2,2) #Draw origin green
		painter.end()

	def mousePressEvent(self,event):
		event.accept()
		if debug:
			print("Mouse pressed event at %d %d" % (event.x(), event.y()))
		# The origin of the robot is taken account here
		xend = event.x() - self.xOffset
		yend = event.y() - self.yOffset
		if debug:
			print("Mouse press fixed to %d %d" % (float(xend), float(yend)))
		#self.clickPoints.append((event.x(), event.y())) #???
		angles = self.calcIKinematics(float(xend),float(yend))

		self.repaint()

	def mouseMoveEvent(self,event):
		event.accept()
		if debug:
			print("Mouse move event at %d %d" % (event.x(), event.y()))
		# The origin of the robot is taken account here
		xend = event.x() - self.xOffset
		yend = event.y() - self.yOffset
		if debug:
			print("Mouse move fixed to %d %d" % (float(xend), float(yend))) 
		#self.clickPoints.append((event.x(), event.y())) #???
		angles = self.calcIKinematics(float(xend),-float(yend))

		self.repaint()

	def createMatrix(self,angle,lenght):
		m = np.array([[cos(angle),-sin(angle),0,lenght],
						[sin(angle),cos(angle),0,0],
						[0,0,1,0],
						[0,0,0,1]])
		return m

		# painter.drawEllipse(QtCore.QPoint(xOffset+end[0],yOffset+end[1]),2,2)
		# end = self.drawArm(painter,end,self.angle2,100,2)
		# painter.setPen(QtCore.Qt.red)
		# painter.drawEllipse(QtCore.QPoint(xOffset+end[0],yOffset+end[1]),2,2)

	def drawArm1(self,painter,startpoints,endpoints,width=1):
		white = (255,255,255)
		painter.setPen(QtGui.QColor(*white))
		#print("Drawing from %d,%d to %d,%d" % (int(startpoints[0]),int(startpoints[1]),int(endpoints[0]),int(endpoints[1])))
		#print("Drawing really from %d,%d to %d,%d" % (int(self.xOffset+startpoints[0]),int(self.yOffset+startpoints[1]),int(self.xOffset+endpoints[0]),int(self.yOffset+endpoints[1])))
		painter.drawLine(int(self.xOffset+startpoints[0]),int(self.yOffset-startpoints[1]),int(self.xOffset+endpoints[0]),int(self.yOffset-endpoints[1]))
		

	def drawArm(self,painter,startpoints,angle,lenght,width=1):
		x = startpoints[0]+lenght*cos(radians(angle))
		y = startpoints[1]+lenght*sin(radians(angle))
		white = (255,255,255)
		painter.setPen(QtGui.QColor(*white))
		painter.drawLine(int(startpoints[0]),int(startpoints[1]),x,y)
		return (x,y)

	def angle1Changed(self,value):
		self.angle1= value
		print("Angle1: "+ str(value))
		self.repaint()

	def angle2Changed(self,value):
		self.angle2= value
		self.repaint()

	def angle3Changed(self,value):
		self.angle3= value
		self.repaint()
		#self.paintEvent(None)

def main():
	app = QtGui.QApplication(sys.argv)

	w = QtGui.QWidget()
	w.resize(600,600)
	w.setWindowTitle('Robot test')
	
	layout = QtGui.QVBoxLayout()
	layout.setSpacing(0)
	layout.setMargin(0)
	pal = QtGui.QPalette()
	pal.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
	w.setAutoFillBackground(True)
	w.setPalette(pal)

	w2 = Robot(w)
	w2.resize(300,300)
	layout.addWidget(w2)

	slider = QtGui.QSlider(QtCore.Qt.Horizontal,w)
	slider.setMinimum(0)
	slider.setMaximum(180)
	slider.valueChanged.connect(w2.angle1Changed)
	layout.addWidget(slider)

	slider2 = QtGui.QSlider(QtCore.Qt.Horizontal,w)
	slider2.setMinimum(-180)
	slider2.setMaximum(180)
	slider2.valueChanged.connect(w2.angle2Changed)
	layout.addWidget(slider2)


	slider3 = QtGui.QSlider(QtCore.Qt.Horizontal,w)
	slider3.setMinimum(-180)
	slider3.setMaximum(180)
	slider3.valueChanged.connect(w2.angle3Changed)
	layout.addWidget(slider3)
	w.setLayout(layout)

	w.show()

	sys.exit(app.exec_())



if __name__ == '__main__':
	main()