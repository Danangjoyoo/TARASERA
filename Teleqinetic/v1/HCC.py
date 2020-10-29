import cv2
import numpy as np
import math
import pyautogui as pg
import keyboard as kb
import mouse as mo
import time
from win32api import GetSystemMetrics as gsm
from tkinter import messagebox
import tkinter as tk

class detClasses():
    def __init__(self, name, cam_id):
        self.cam_id = cam_id
        self.name = name
        self.img = None
        self.fps = 0
        self.classifier = 'hcc'
        self.runObj = None

    def resize(self, scale):
        img = cv2.resize(self.img, None, fx=scale, fy=scale)
        return img

    def getFPS(self,t2,t1):
        self.fps = round((1 / (t2 - t1)), 2)
        return cv2.putText(self.img, f'FPS: {self.fps}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (10, 10, 255), 2)

    def main(self):
        pass

    def cvtCursorMap(self, cont):
        img = self.img
        scale = 0.25
        wi, hi = img.shape[1]*scale, img.shape[0]*scale
        ws, hs = gsm(0), gsm(1)
        x1, y1 = cont[0][0], cont[0][1]
        w1, h1 = cont[0][2], cont[0][3]
        xs = int((x1) * ws / wi)
        xs = ws-(xs)
        ys = int((y1) * hs / hi)
        ys = (ys)
        return xs, ys

    def pickClassifier(self, selected):
        self.classifier = selected
        if self.classifier == 'hcc':
            self.runObj = haarCC('app',self.cam_id)
        elif self.classifier == 'hsv':
            self.runObj = hsvC('app', self.cam_id)
        else:
            self.runObj = nnC('app', self.cam_id)
        return self.runObj

class haarCC(detClasses):
    def __init__(self,name, cam_id):
        super().__init__(name, cam_id)
        self.cam_id = cam_id
        self.cname = 'hcc'
        self.name = name
        self.img = None
        self.cap = None
        self.mouseL_pressed = False
        self.fist, self.palm = [], []
        self.dragStat = False
        self.x, self.y = 0, 0
        self.t_balance = 0
        self.tempVal = [[],[]]
        self.dragStat = False
        self.parameters = [[1.2, 3, 1.07, 7, 3, 0.6, 5], [0, 0, 0]]
        self.showWin = True
        self.showBorder = True
        self.fistSF, self.fistN = 1.2,3
        self.palmSF, self.palmN = 1.07,7
        self.blurSize = 3
        self.inputFrameSize = 0.6
        self.movAvgSize = 5
        self.cam_id = 0

    def detectObject(self):
        fist_cont = []
        palm_cont = []
        img = self.img
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, self.blurSize)
        fist_model = cv2.CascadeClassifier('assets/cascade/kepal.xml')
        fist_cascade = fist_model.detectMultiScale(blur, self.fistSF, self.fistN)
        palm_model = cv2.CascadeClassifier('assets/cascade/open_palm.xml')
        palm_cascade = palm_model.detectMultiScale(blur, self.palmSF, self.palmN)
        for x, y, w, h in fist_cascade:
            fist_cont.append([x, y, w, h])
        for i in enumerate(fist_cont):
            if i[0] < 2:
                x = i[1][0]
                y = i[1][1]
                w = i[1][2]
                h = i[1][3]
                if self.showBorder:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (10, 255, 10), 3)
                cv2.putText(img, f'{i[0]}', (int((x+(w/2))*0.90), int((y+(h/2))*1.1)), cv2.FONT_HERSHEY_COMPLEX, 1, (10, 255, 10), 2)
        if not fist_cont:
            for x, y, w, h in palm_cascade:
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 255, 10), 3)
                palm_cont.append([x, y, w, h])
            for i in enumerate(palm_cont):
                if i[0] < 2:
                    x = i[1][0]
                    y = i[1][1]
                    w = i[1][2]
                    h = i[1][3]
                    if self.showBorder:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (10, 10, 255), 3)
                    cv2.putText(img, f'{i[0]}', (x + 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (10, 10, 255), 2)
        return img, fist_cont, palm_cont

    def balancing(self,var,val):
        if var == 'x':
            idx = 0
        else:
            idx = 1
        self.tempVal[idx].append(val)
        if len(self.tempVal[idx]) > self.movAvgSize:
            val = np.average(self.tempVal[idx])
            self.tempVal[idx].pop(0)
        return val

    def moveCur(self, cont):
        self.x, self.y = self.cvtCursorMap(cont)
        self.x = self.balancing('x',self.x)
        self.y = self.balancing('y',self.y)
        mo.move(self.x, self.y)

    def clickCur():
        mo.click()

    def dragCur(self, cont):
        print(self.dragStat)
        if self.dragStat:
            self.moveCur(cont)
            if not self.mouseL_pressed:
                mo.press('left')
                self.mouseL_pressed = True
        else:
            mo.click('left')
            self.mouseL_pressed = False

    def getStat(self):
        if len(self.palm) > 0:
            self.dragStat = False
        elif len(self.fist) > 0:
            self.dragStat = True

    def inputParameters(self, params):
        self.parameters = params
        print(params)
        if params:
            self.cam_id = params[1][0]
            self.showWin = params[1][1]
            self.showBorder = params[1][2]

            self.fistSF = params[0][0]
            self.fistN = params[0][1]
            self.palmSF = params[0][2]
            self.palmN = params[0][3]
            self.blurSize = params[0][4]
            self.inputFrameSize = params[0][5]
            self.movAvgSize = params[0][6]

    def main(self):
        self.fist, self.palm = [],[]
        self.cap = cv2.VideoCapture(self.cam_id)
        while self.cap.isOpened():
            t1 = time.time()
            _, self.img = self.cap.read()
            try:
                self.img = self.resize(self.inputFrameSize)
                self.img, self.fist, self.palm = self.detectObject()
                self.img = self.resize(2)
                self.getStat()

                try:
                    self.moveCur(self.palm)
                except:
                    pass

                try:
                    self.dragCur(self.fist)
                except:
                    pass

                t2 = time.time()
                self.getFPS(t2,t1)
                if self.showWin:
                    cv2.imshow(self.name, self.img)
            except:
                root = tk.Tk()
                messagebox.showerror('CANNOT DETECT CAMERA',
                                     'Wrong Camera ID!\nPlease Check Your Device and Try Again!')
                root.destroy()
                break
            if cv2.waitKey(1) & 0xFF == ord('q') or kb.is_pressed('esc'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

class hsvC(detClasses):
    def __init__(self, name,cam_id):
        super().__init__(name,cam_id)
        self.cam_id = cam_id
        self.name = name
        self.cname = 'hsv'

    def main(self):
        print('NOT AVAILABLE YET')

class nnC(detClasses):
    def __init__(self,name,cam_id):
        super().__init__(name, cam_id)
        self.cam_id = cam_id
        self.name = name
        self.cname = 'cnn'

    def main(self):
        print('NOT AVAILABLE YET')

"""if __name__ == "__main__":
    anjay = detClasses('anjay',1)
    anjay = anjay.pickClassifier('hcc')
    anjay.main()"""