#هذا من فضل ربي
#اللهم إني أعوذ بك من الحسد و العين
#ما شاء الله
from PyQt5 import QtCore , QtGui , QtWidgets
import sys
import cv2 
import numpy as np
import cvzone
import math
import time
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from datetime import datetime
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.HandTrackingModule import HandDetector
	
pro = QtWidgets.QApplication(sys.argv)
win = QtWidgets.QWidget()

#Inputs for configuring the webcam
print("This program Developped By Khali Della3a Studio")
Ncam = input("Enter number 0 for using your first and 1 for your second camera: ") 
fps = input("Enter the exact number of fps of your camera: ")
dosto = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
folder = "Snapshot"
print(dosto)

#A function for Capturing the webcam without anything
def capturing():
	datos = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
	vid = cv2.VideoCapture(int(Ncam),cv2.CAP_DSHOW)
	frame_width = int(vid.get(3))
	frame_height = int(vid.get(4))
	size = (frame_width, frame_height)
	out = cv2.VideoWriter(f'output\\CamScopeoutput_{time.time()}.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), int(fps), (frame_width,frame_height))
	while(True):
		ret, frame = vid.read()
		cv2.imshow('Camera Window', frame)
		if ret == True:
			out.write(frame) 
			cv2.imshow('Camera Window', frame)
			if cv2.waitKey(1) & 0xFF == ord('n'):
				break 
	vid.release()
	out.release()
	cv2.destroyAllWindows()		
	
#A function for Capturing the webcam and removing the background			
def bgRemove():
	date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
	vido = cv2.VideoCapture(int(Ncam),cv2.CAP_DSHOW)
	framewidth = int(vido.get(3))
	frameheight = int(vido.get(4))
	seg = SelfiSegmentation()
	size = (framewidth, frameheight)
	bgout = cv2.VideoWriter(f'output\\CamScopeoutput_{time.time()}.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), int(fps), (framewidth,frameheight))
	while(True):
		success, windo = vido.read()
		noBG = seg.removeBG(windo,(0,250,0), threshold=0.5)
		if success == True:
			bgout.write(noBG) 
			cv2.imshow('Backgroud remove', noBG)
			if cv2.waitKey(1) & 0xFF == ord('n'):
				break     	
	vido.release()
	bgout.release()
	cv2.destroyAllWindows()
	
#This Feature will be more developped 				    	
def faceCM():
	vodo = cv2.VideoCapture(int(Ncam),cv2.CAP_DSHOW)
	fwidth = int(vodo.get(3))
	fheight = int(vodo.get(4))
	dect = FaceMeshDetector(maxFaces=1)
	while(True):
		imgo, wind = vodo.read()
		wind,faces = dect.findFaceMesh(wind,)	
		cv2.imshow('Face Distance Measurement', wind)	
		if cv2.waitKey(1) & 0xFF == ord('n'):	
				break		
						    	
				    	
	vodo.release()
	cv2.destroyAllWindows()	
#There is many problems here please fix it		
def ASL():
	capt = cv2.VideoCapture(int(Ncam), cv2.CAP_DSHOW)
	Fwidth = int(capt.get(3))
	Fheight = int(capt.get(4))
	decto = HandDetector(maxHands=2)
	DM = cv2.VideoWriter(f'output\\CamScopeoutput_{time.time()}.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), int(fps), (Fwidth,Fheight))
	DM1 = cv2.VideoWriter(f'output\\CamScopeoutput_{time.time()}ImageCrop.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), int(fps), (Fwidth,Fheight))
	DM2 = cv2.VideoWriter(f'output\\CamScopeoutput_{time.time()}ImageWhiteSquare.mp4',cv2.VideoWriter_fourcc('m','p','4','v'), int(fps), (Fwidth,Fheight))
	while(True):
		imag, frm = capt.read()
		hands, frm = decto.findHands(frm)	
		ImgSize = 300
		DM.write(frm)
		if hands:
			hand = hands[0]
			x, y, w, h = hand["bbox"]
			imgWht = np.ones((ImgSize,ImgSize,3),np.uint8)*255
			ImgCrop = frm[y-20:y + h+20 ,x-20:x + w+20]
			imgCropShape = ImgCrop.shape
			aspRat = h/w
			if aspRat >1:
				con = ImgSize/h
				WiCal = math.ceil(con * w)
				ImgResize = cv2.resize(ImgCrop,(WiCal,ImgSize))
				ImgResizu = ImgResize.shape
				Wigap = math.ceil((ImgSize-WiCal)/2)
				imgWht[:, Wigap:WiCal+Wigap] = ImgResize
				
			else:
				con = ImgSize/w
				HiCal = math.ceil(con * h)
				ImgResize = cv2.resize(ImgCrop,(ImgSize,HiCal))
				ImgResizus = ImgResize.shape
				Higap = math.ceil((ImgSize-HiCal)/2)
				h, w = imag.shape
				size =( w,h)
				imgWht[Higap:HiCal+Higap,:] = ImgResize	
				
			cv2.imshow("Hand Crop",ImgCrop)
			cv2.imshow("Image with white color", imgWht)
			DM1.write(ImgCrop)
			DM2.write(imgWht)
				
		cv2.imshow('American Sign Language', frm)	
		if cv2.waitKey(1) & 0xFF == ord('n'):
				break		
	capt.release()
	DM.release()
	DM1.release()
	DM2.release()
	cv2.destroyAllWindows()		
		
win.resize(1100, 600)
win.move(200, 50)
win.setWindowTitle('CamScope v1.0')
win.setStyleSheet('background-color:rgb(20, 20, 20);')
win.setWindowIcon(QtGui.QIcon("media\\CamScope.png"))

btn1 = QtWidgets.QPushButton('Start Recording', win)
btn1.setGeometry(900,400, 150,100)
btn1.setStyleSheet("background-color:#0057FF; font-size:18px; border:2px solid black; border-radius:4px; font-family:Roboto;")
btn1.setToolTip("Start recording your webcam")
btn1.clicked.connect(capturing)

btn12 = QtWidgets.QPushButton('Record\n without background', win)
btn12.setGeometry(900,275, 150,100)
btn12.setStyleSheet("background-color:#00FB05; font-size:15px; border:2px solid black; border-radius:4px; font-family:Roboto;")
btn12.setToolTip("record your webcam without background")
btn12.clicked.connect(bgRemove)

btn13 = QtWidgets.QPushButton('Face detection', win)
btn13.setGeometry(900,150, 150,100)
btn13.setStyleSheet("background-color:#8117FF; font-size:15px; border:2px solid black; border-radius:4px; font-family:Roboto;")
btn13.setToolTip("this will show you hwo your face will look like in the front of camera")
btn13.clicked.connect(faceCM)

btn14 = QtWidgets.QPushButton('Record with hand tracking\nfor deaf-mute people', win)
btn14.setGeometry(675,400, 200,100)
btn14.setStyleSheet("background-color:#FFA500; font-size:15px; border:2px solid black; border-radius:4px; font-family:Roboto;")
btn14.setToolTip("This feature is for Deaf-Mute people\nDon't record your hand in close or far distance!")
btn14.clicked.connect(ASL)

btn2 = QtWidgets.QPushButton('Exit', win)
btn2.setStyleSheet("background-color:rgb(255, 100, 0); font-size:18px; border:2px solid black; border-radius:4px; ")
btn2.setGeometry(0,0, 100,50)
btn2.setToolTip("Quit the program")
btn2.setIcon(QtGui.QIcon("media\\exit-logout-png.png"))
btn2.clicked.connect(exit)

lbl = QtWidgets.QLabel("<u>CamScope</u>", win)
lbl.move(125,-10)
lbl.setStyleSheet("font-size:48px; ")

lbl0 = QtWidgets.QLabel("<b>By Khali Della3a Studio</b>", win)
lbl0.move(350, 30)

lbl011 = QtWidgets.QLabel('Click (n) To Stop The Preview And Save Your Video', win)
lbl011.move(50,120)
lbl011.setStyleSheet("font-size:15px ;")

lbl1101 = QtWidgets.QLabel('OBS virtual cam will be helpful for using these features in video call', win)
lbl1101.move(50,140)
lbl1101.setStyleSheet("font-size:15px ;")

clbl = QtWidgets.QLabel("Credits:\nDeveloping and Coding: Khali Della3a\nThis program is open source if you have payed to use it you have been scamed !", win)
clbl.move(550, 30)
clbl.setStyleSheet("font-size:14px;")

win.show()
pro.exec_()












