import os, sys
import shutil
import tkinter as tk
from tkinter import messagebox as mbox

root = tk.Tk()
root.overrideredirect()
root.withdraw()

try:
	deleteStat = mbox.askyesno(title='Uninstall TeleQinetic v1.25', message='Are you sure want to uninstall TeleQinetic?')

	if deleteStat:
		dir = os.getcwd()
		filelist = os.listdir(dir)

		for i in filelist:
			if i != 'uninstall001.exe' or i != 'README FOR COMPLETE UNINSTALL.txt':
				try:
					os.remove(i)
				except:
					pass

		shutil.rmtree(dir)
	else:
		sys.exit()
except:
	pass

mbox.showinfo(title='Complete Uninstall Guide', message='After Uninstalled, the directory still remains unempty\nJust delete the remaining files manually\nThis app is not registered to the system registry so it will free of dump files')
root.destroy()