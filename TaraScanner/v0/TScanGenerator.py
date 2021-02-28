import time, os, sys, tkinter, pyqrcode, io
import pandas as pd
from tkinter import filedialog as fd
import pyzbar.pyzbar as pbar

#████████████████T█A█R█A█S█E█R█A██████████T█A█R█A█S█E█R█A██████████████T█A█R█A█S█E█R█A██████████████████T█A█R█A█S█E█R█A██████████████

class QRcode():
	@staticmethod
	def read(img):
		codes = pbar.decode(img)
		if codes: return codes

	@staticmethod
	def generate(nameIn='',nameOut='',multiple=False, df=None):
		if not multiple:
			url = pyqrcode.create(nameIn)
			scale = 25
			if not '.png' in str.lower(nameOut): nameOut+=".png"
			url.png(nameOut,scale=scale)
			return nameOut
		else:
			nList = [i for i in df[df.keys()[0]]]
			os.system('mkdir GeneratedCode')
			newFolder = QRcode.getTimeStamp()
			os.chdir('GeneratedCode')
			os.system(f'mkdir {newFolder}')
			os.chdir('..')
			for n in nList:
				out = f'{n}_QR_{int(time.time())}'
				print('Generated: '+out)
				QRcode.generate(n, 'GeneratedCode/'+newFolder+'/'+out)

	@staticmethod
	def generateFromExcel():
		filename = QRcode.openFile()
		df = pd.read_excel(filename)
		QRcode.generate(multiple=True,df=df)
		return filename

	@staticmethod
	def generateFromCSV():
		filename = QRcode.openFile()
		df = pd.read_csv(filename, encoding="utf-8")
		QRcode.generate(multiple=True,df=df)
		return filename

	@staticmethod
	def openFile():
		root = tkinter.Tk()
		filename = fd.askopenfile(initialdir=os.getcwd())
		root.destroy()
		filename = str(filename).split(' ')[1].split('=')[1].split("'")[1]
		return filename

	@staticmethod
	def getTimeStamp():
		ts = time.localtime()
		hrs = ts[3] if len(str(ts[3])) > 1 else '0'+str(ts[3])
		mins = ts[4] if len(str(ts[4])) > 1 else '0'+str(ts[4])
		secs = ts[5] if len(str(ts[5])) > 1 else '0'+str(ts[5])
		date = f'{ts[2]}-{ts[1]}-{ts[0]}_at_{hrs}-{mins}-{secs}'
		return date