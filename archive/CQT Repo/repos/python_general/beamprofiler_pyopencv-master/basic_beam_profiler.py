
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 18:32:34 2015

@author: nick
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
import pylab as pyl
from scipy.optimize import curve_fit
from math import log10, floor

#init var
stagger = 12 #fit every N frames, drop frames in between, required for slow PC
waist_x_cumulative = np.array([])
waist_y_cumulative = np.array([])

#init camera
cap = cv2.VideoCapture(0) #Chose capture device may need to change to 1 if using laptop with a webcam
cap.set(3,640)#Sets image to half size
cap.set(4,480)#Sets image to half size
cap.set(15,120)# Sets exmposure time should stay fixed changed att as needed
ret, frame = cap.read()# Reads in one frame to stop crashing issues

#init plt
plt.axis([0, cap.get(3), 0, 255])#sets plots axis
plt.ion()#sets iteractive plot means constant update
plt.show()# shows plotting window

def gauss_function(x, a, x0, sigma,C):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))+C

def round_sig(x, sig=3):
	return round(x, sig-int(floor(log10(x)))-1)

i=0
j=0
while(True):
	# Capture frame-by-frame
	plt.clf() #clears plots
	ret, img = cap.read()
	#Set threshold value to make binary image so centre can be found accurately
	ret,thresh = cv2.threshold(img,80,255,0)
	#Calcualtes image moments
	M = cv2.moments(thresh)

	if M['m00'] != 0.0 and i%stagger==0: #stops division by zero error
		i=0
		cx = int(M['m10']/M['m00'])#Calculates beam center x
		cy = int(M['m01']/M['m00'])#Calculates beam center y
		linex = img[cy,:] #1D array of pixel values through x centre
		liney = img[:,cx] #1D array of pixel values through y centre

		#Fitting x direction
		plt.subplot(211)
		x = pyl.arange(len(linex)) #Creates array of x points for fit  
		p0x = [max(linex),cx,np.std(linex),5] #intial values x fit
		poptx, pcovx = curve_fit(gauss_function, x, linex,p0x) #fitting algorithm
		plt.plot(linex) #plots x line plot data
		plt.plot(gauss_function(x,*poptx),color='red') #plots fit to this
		waist_x = round_sig(poptx[2]*4*3.75e-3,3) #x width in pixel times pixel size
		plt.title('Waist x '+str(waist_x)+' mm')

		#Fitting y direction
		plt.subplot(212)
		y = pyl.arange(len(liney)) #Creates array of x points for fit
		p0y = [max(liney),cy,np.std(liney),5] #intial values x fit
		popty, pcovy = curve_fit(gauss_function,y,liney,p0y) #fitting algorithm
		plt.plot(liney) #plots y line plot data
		plt.plot(gauss_function(y,*popty),color='red') #plots fit to this
		waist_y = round_sig(popty[2]*4*3.75e-3,3) #y width in pixel times pixel size to give waist in mm
		plt.title('Waist y '+str(waist_y)+' mm')
			 
		cv2.line(img,(cx+int(poptx[2]),cy),(cx-int(poptx[2]),cy),255,1)#draws x line
		cv2.line(img,(cx,cy+int(popty[2])),(cx,cy-int(popty[2])),255,1)#draws y line
		cv2.ellipse(img,(cx,cy),(int(poptx[2]),int(popty[2])),0,0,360,255,1)#draws ellipse 
		plt.draw()
        
        #Calc cummulative average
		if j%10==0:        
			j=1
			print 'w_x: ',waist_x_cumulative.mean(),'+/-',waist_x_cumulative.std(),'mm'
			print 'w_y: ',waist_y_cumulative.mean(),'+/-',waist_y_cumulative.std(),'mm'
			waist_x_cumulative = np.append([],waist_x)
			waist_y_cumulative = np.append([],waist_y)
		else:
			waist_x_cumulative = np.append(waist_x_cumulative,waist_x)
			waist_y_cumulative = np.append(waist_y_cumulative,waist_y)
			j=j+1
        
		print 'w: [',waist_x, waist_y,']','I0: [',int(round(poptx[0])),int(round(popty[0])),']'
	cv2.imshow('img',img)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		break
	i+=1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
