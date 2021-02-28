import os, sys
from TScanReader import Scanner
from TScanGenerator import QRcode
import TScanUI as tsui

if __name__ == '__main__':
	tsui.PopupImage.popUp('assets/init_popup.png',dur=3)
	scanner = Scanner()
	app = tsui.QtWidgets.QApplication(sys.argv)
	MainWindow = tsui.QtWidgets.QMainWindow()
	ui = tsui.Ui_MainWindow(
			runScanner=scanner.run,
			stopScanner=scanner.deactivateCamera,
			setCamID=scanner.setCamID,
			connectDbase=scanner.connect2Dbase,
			reset=scanner.resetLocal,
			encode=QRcode.generate,
			generateByCSV=QRcode.generateFromCSV,
			generateByExcel=QRcode.generateFromExcel,
		)
	scanner.updateMonitor = (lambda: ui.updateMonitor(ui))
	ui.setupUi(MainWindow)
	MainWindow.show()
	app.exec_()