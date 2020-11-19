import pygame as pg
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os


class button():
    def __init__(self, pic1, pic2, x, y, NumBut, Separator):
        self.pic1 = pic1
        self.pic2 = pic2
        self.x = x
        self.y = y
        self.numBut = NumBut
        self.sep = Separator
        self.ss = False
        self.clickArea = False
        self.teks = False
        if self.sep == 1:
            self.ss = True
        self.t = 0

    def draw(self):
        global opendir, saved_name
        self.clickArea = False
        self.kotak = win.blit(self.pic1, (self.x, self.y))
        mX, mY = pg.mouse.get_pos()
        if self.kotak.collidepoint(mX,mY):
            self.kotak = win.blit(self.pic2, (self.x, self.y))
            self.clickArea = True

        separs = [separ1, separ2, separ3, separ4]
        if self.sep and self.clickArea and pg.mouse.get_pressed()[0]:
            self.ss = True
            for i in separs:
                if not self.sep == i.sep:
                    i.ss = False

        global splitter
        for i in separs:
            if i.ss:
                if i.sep == 1:
                    splitter = '_'
                elif i.sep == 2:
                    splitter = '-'
                elif i.sep == 3:
                    splitter = '+'
                elif i.sep == 4:
                    splitter = '|'

        if self.ss:
            self.kotak = win.blit(self.pic2, (self.x, self.y))


        if self.numBut == 1:
            self.but1()
            if self.teks:
                printText(opendir, self.x - 540, self.y + 15)
        elif self.numBut == 2:
            self.but2()
            if self.teks:
                printText(f'{saved_name}.xlsx', self.x - 540, self.y + 15)
        elif self.numBut == 3:
            self.but3()

        global incorrect
        if incorrect:
            show = 0
            if self.t < 100:
                show = win.blit(warning, (200, 220))
                self.t += 1
            else:
                incorrect = False
                self.t = 0
            try:
                if self.t > 10:
                    if not show.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]:
                        incorrect = False
                        self.t = 0
            except:
                pass

    def but1(self):
        global filename, opendir, splitter
        if pg.mouse.get_pressed()[0] and self.clickArea:
            filename, opendir = getFilename(splitter)
            self.teks = True

    def but2(self):
        global saved_name, filename
        if pg.mouse.get_pressed()[0] and self.clickArea:
            saved_name = setSavedname()
            self.teks = True

    def but3(self):
        global filename, saved_name
        if pg.mouse.get_pressed()[0] and self.clickArea:
            rekap(filename, saved_name)


def printText(teks, x, y):
    new_teks = ''
    if len(teks) > 60:
        for i in range(20):
            new_teks += teks[i]
        new_teks += '......'
        for i in range(30):
            new_teks += teks[i+(len(teks)-30)]
    else:
        new_teks = teks
    teksInput = pg.font.SysFont('calibri', 20, True).render(new_teks,1,(0,0,0))
    win.blit(teksInput, (x,y))

def getFilename(splitter):
    global incorrect
    root = tk.Tk()
    root.update()
    filenames, dir = [], ''
    try:
        dir = filedialog.askdirectory(title='Select Folder')
        printText(dir, 50, 200)
        filelist = os.listdir(dir)
        filenames = [[]]
        t = 0
        for file in enumerate(filelist):
            a = file[1].split('.')
            filenames[0].append(a[0])
            b = a[0].split(splitter)
            if t == 0:
                for i in range(len(b)+1):
                    filenames.append([])
            if len(b) == len(filenames) - 2:
                for i in enumerate(b):
                        filenames[i[0]+1].append(i[1])
            else:
                for i in range(len(filenames)-2):
                    filenames[i + 1].append('???')
            data_length = len(filenames)
            try:
                filenames[data_length-1].append(a[-1])
            except:
                pass
            t += 1
        root.destroy()
    except:
        incorrect = True
        root.destroy()
    return filenames, dir

def setSavedname():
    global incorrect
    root = tk.Tk()
    root.update()
    saved_name = ''
    try:
        saved_name = filedialog.asksaveasfilename(title='Save As',filetypes=(('Excel','*.xlsx'),('All','*.*')))
        root.destroy()
    except:
        incorrect = True
        root.destroy()
    return saved_name

def rekap(list, name):
    global incorrect, succeed
    try:
        data = pd.DataFrame(list).T
        data.to_excel(f'{name}.xlsx')
        succeed = True
    except:
        incorrect = True

pg.init()
pg.display.set_caption('TARALISTER')
icon = pg.image.load('assets/tl.png')
pg.display.set_icon(icon)
win = pg.display.set_mode((800,640))
run = True
introSession = True
incorrect = False
succeed = False
ts = 0
filename, data, saved_name, opendir, splitter = '',[],'', '', ''
bg2 = pg.image.load('assets/bg2.png')
but1 = pg.image.load('assets/but11.png').convert_alpha()
but2 = pg.image.load('assets/but21.png').convert_alpha()
but3 = pg.image.load('assets/but31.png').convert_alpha()
fbut1 = pg.image.load('assets/fbut1.png').convert_alpha()
fbut2 = pg.image.load('assets/fbut2.png').convert_alpha()
fbut3 = pg.image.load('assets/fbut3.png').convert_alpha()
warning = pg.image.load('assets/warning.png').convert_alpha()

button1 = button(fbut1, but1, 712, 316,1, 0)
button2 = button(fbut2, but2, 712, 466,2, 0)
button3 = button(fbut3, but3, 260, 571,3,0)

sep1 = pg.image.load('assets/sep1.png').convert_alpha()
sep2 = pg.image.load('assets/sep2.png').convert_alpha()
sep3 = pg.image.load('assets/sep3.png').convert_alpha()
sep4 = pg.image.load('assets/sep4.png').convert_alpha()
fsep1 = pg.image.load('assets/fsep1.png').convert_alpha()
fsep2 = pg.image.load('assets/fsep2.png').convert_alpha()
fsep3 = pg.image.load('assets/fsep3.png').convert_alpha()
fsep4 = pg.image.load('assets/fsep4.png').convert_alpha()

separ1 = button(fsep1, sep1, 168, 390, 0, 1)
separ2 = button(fsep2, sep2, 288, 390, 0, 2)
separ3 = button(fsep3, sep3, 408, 390, 0, 3)
separ4 = button(fsep4, sep4, 528, 390, 0, 4)

intropic = pg.image.load('assets/intro.png')
ix = 0
iy = 0
it = 0
done = pg.image.load('assets/done.png')

while run:
    #print(pg.mouse.get_pos())
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    if introSession:
        if it > 100:
            if iy >= -640:
                iy -= 15
            else:
                introSession = False
        win.blit(intropic, (ix, iy))
        it += 1
    else:
        win.blit(bg2, (0,0))
        button1.draw()
        button2.draw()
        button3.draw()
        separ1.draw()
        separ2.draw()
        separ3.draw()
        separ4.draw()

    if succeed:
        if ts < 65:
            ts += 1
            win.blit(done, (200,220))
        else:
            ts = 0
            succeed = False

    pg.display.update()

pg.quit()