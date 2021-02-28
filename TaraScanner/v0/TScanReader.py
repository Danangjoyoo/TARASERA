import cv2, time, os, sys, winsound, threading
import pandas as pd
import numpy as np
from TScanGenerator import QRcode

#████████████████T█A█R█A█S█E█R█A██████████T█A█R█A█S█E█R█A██████████████T█A█R█A█S█E█R█A██████████████████T█A█R█A█S█E█R█A██████████████#██████████████████████████████████████████████████████████████████████████████████████████████████████████████

class Scanner():
	def __init__(self):
		self.cap = None
		self.frame = None
		self.prevData = None
		self.dataAdded = False
		self.notAdded = False
		self.camID = 0
		self.connectDatabase = True
		self.cameraStat = False
		self.cameraThread = None
		self.updateMonitor = None

	def setCamID(self, ID):
		self.camID = ID

	def connect2Dbase(self, stat=True):
		self.connectDatabase = stat

	def activateCamera(self):
		self.cameraStat = True

	def deactivateCamera(self):
		self.cameraStat = False

	def run(self):
		self.cameraThread = threading.Thread(target=self.__main())
		self.cameraThread.start()

	def __main(self):
		try:
			self.activateCamera()
			self.cap = cv2.VideoCapture(self.camID)
			self.beepWarn()
			while self.cap.isOpened() and self.cameraStat:
				_, self.frame = self.cap.read()
				if self.connectDatabase: self.countLocal()
				if self.dataAdded:
					winsound.Beep(1000,300)
					winsound.Beep(300,300)
					self.dataAdded = False
				codes = QRcode.read(self.frame)
				if codes:
					for code in codes:
						pts = np.array([code.polygon],np.int32)
						pts = pts.reshape(-1,1,2)
						cv2.polylines(self.frame,[pts],True,[255,0,255],2)
						data = str((code.data), 'UTF-8')
						x = code.rect.left
						y = code.rect.top
						if self.connectDatabase:						
							if self.checkLocal(data,'Name'): 
								self.setLocal(data)								
								self.screenText(data, (x,y-5), 0.5, (20,230,20))
							else: 
								self.screenText(data, (x,y-5), 0.5, (20,20,240))
						else:
							self.screenText(data, (x,y-5), 0.5, (20,230,20))
				cv2.imshow('Tarascanner',self.frame)
				if cv2.waitKey(1) & 0xFF == ord('q'): break
			self.cap.release()
			cv2.destroyAllWindows()
		except Exception as e:
			self.deactivateCamera()
			self.addNotification(print,e)

	def setLocal(self, data):
		ts = time.localtime()
		hrs = ts[3] if len(str(ts[3])) > 1 else '0'+str(ts[3])
		mins = ts[4] if len(str(ts[4])) > 1 else '0'+str(ts[4])
		secs = ts[5] if len(str(ts[5])) > 1 else '0'+str(ts[5])
		date = f'{hrs}:{mins}:{secs} {ts[2]}/{ts[1]}/{ts[0]}'
		df = pd.read_csv('Database/localDatabase.csv')
		noPack = df.pop('No')
		tsPack = [i for i in df.pop('TimeStamp')]
		namePack = [str(i) for i in df.pop('Name')]
		tsPack[namePack.index(data)] = date
		keys = ['No','TimeStamp','Name']; datas = []
		for i in range(len(noPack)): 
			datas.append([noPack[i], tsPack[i], namePack[i]])
			try:
				bool(df.keys())
				for key in df.keys(): datas[len(datas)-1].append(df[key][i])
			except: pass
		pd.DataFrame(datas,columns=keys+[key for key in df.keys()]).to_csv('Database/localDatabase.csv',index=False)
		self.updateMonitor()

	def checkLocal(self, data, localVar):
		df = pd.read_csv('Database/localDatabase.csv')
		local = [str(i) for i in df[localVar]]
		ts = [str(i) for i in df['TimeStamp']]
		if data in local:
			if ts[local.index(data)] == 'nan':
				print(f'{data} TimeStamp Added!')
				self.screenText(f'Recorded!',pos=(200,80),color=(20,230,20))
				self.dataAdded = True
				return True
			else:
				print(f'{data} Already Submitted!')
				self.screenText(f'Data Already Submitted!',color=(50,10,230))
				self.notAdded = True
				return False
		else:
			print(f'{data} is not Exist in Database')
			self.screenText(f'QR Code is not Registered',color=(50,10,230))
			self.notAdded = True
			return False

	def countLocal(self):
		df = pd.read_csv('Database/localDatabase.csv')
		count =  0
		for ts in df['TimeStamp']: count += 1 if str(ts) != 'nan' else 0
		self.screenText(f'Total Registered: {count}', (20,20), 0.5, (0,0,0), 2)

	def resetLocal(self):
		df = pd.read_csv('Database/localDatabase.csv')
		noPack = df.pop('No')
		tsPack = [np.nan for i in df.pop('TimeStamp')]
		namePack = [i for i in df.pop('Name')]
		keys = ['No','TimeStamp','Name']; datas = []
		for i in range(len(noPack)):
			datas.append([noPack[i], tsPack[i], namePack[i]])
			try:
				bool(df.keys())
				for key in df.keys(): datas[len(datas)-1].append(df[key][i])
			except: pass
		pd.DataFrame(datas,columns=keys+[key for key in df.keys()]).to_csv('Database/localDatabase.csv',index=False)
		self.addNotification(print,'Reset Done')

	def addNotification(self,*args):
		if args:
			args = list(args)
			if len(args) == 1: 
				func = args.pop(0); func()
			else:
				func = args.pop(0); func(*args)

	def screenText(self, text='', pos=(110,80), fontSize=1, color=(0,0,0), thick=2):
		cv2.putText(self.frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX,fontSize,color,thick)

	def beepWarn(self,init=True):
		if init:
			thread1 = threading.Thread(target=self.beepWarn, args=(False,))
			thread1.start()
		else:
			while self.cap.isOpened() and self.cameraStat:
				if self.notAdded: 
					winsound.Beep(2000,700)
					self.notAdded = False