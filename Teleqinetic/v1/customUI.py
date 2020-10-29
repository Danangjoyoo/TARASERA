import pygame as pg
import random as rd

class background():
    def __init__(self):
        pg.init()

    def getInitImage(self):
        img = pg.image.load('assets//init/init1.png')
        return img

    def getLoadingImage(self):
        img = [pg.image.load('assets/init/load1.png'),
               pg.image.load('assets/init/load2.png'),
               pg.image.load('assets/init/load3.png'),
               pg.image.load('assets/init/load4.png'),
               pg.image.load('assets/init/load5.png'),
               pg.image.load('assets/init/load6.png'),
               pg.image.load('assets/init/load7.png'),
               pg.image.load('assets/init/load8.png'),
               pg.image.load('assets/init/load9.png'),
               pg.image.load('assets/init/load10.png')]
        return img

    def getQuotesImage(self):
        img = [pg.image.load('assets/init/quo1.png'),
               pg.image.load('assets/init/quo2.png'),
               pg.image.load('assets/init/quo3.png'),
               pg.image.load('assets/init/quo4.png')]
        return img

    def getLogoImage(self):
        img = pg.image.load('assets/init/logo1.png')
        return img

    def getMainImage(self):
        img = pg.image.load('assets/main/main3.png')
        return img

    def getStartButton(self):
        img = [pg.image.load('assets/main/start1.png'),
               pg.image.load('assets/main/start2.png')]
        return img

    def getSettingButton(self):
        img = [pg.image.load('assets/main/setting1.png'),
               pg.image.load('assets/main/setting2.png')]
        return img

class runMain(background):
    def __init__(self):
        super().__init__()
        self.scr_w = 500
        self.scr_h = 500
        self.xi = 0
        self.yi = 0
        self.xm = 0
        self.ym = 0
        self.screen = pg.display.set_mode((self.scr_w, self.scr_h), pg.DOUBLEBUF)
        self.caption = pg.display.set_caption('TeleQinetic')
        self.clock = pg.time.Clock()
        self.run = True
        self.tglobal = 0

        self.runInitScreen = True
        self.initImage = self.getInitImage()
        self.loadingPack = self.getLoadingImage()
        self.logoImage = self.getLogoImage(); pg.display.set_icon(self.logoImage)
        self.quotesPack = self.getQuotesImage()
        self.quotesPackIdx = rd.choice([0,1,2,3])
        self.t1 = 0
        self.tload = 0
        self.tload_increment = True
        self.swipeInit = False
        self.tswipe = 0

        self.runMainScreen = False
        self.mainImage = self.getMainImage()
        self.settingImage = self.getSettingButton()
        self.setCollide = False
        self.setClick = False
        self.setBlit = None
        self.setIdx = 0
        self.startImage = self.getStartButton()
        self.startCollide = False
        self.startClick = False
        self.startBlit = None
        self.startIdx = 0

    def initialize(self,*args):
        while self.run:
            self.clock.tick(60)
            self.drawAll()
            for i in args:
                i()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
        pg.quit()

    # INIT SCREEN METHODS

    def drawInit(self):
        self.screen.blit(self.initImage, (0,0-self.yi))

    def drawLoading(self):
        self.tload_crementing()
        if self.tload_increment:
            if self.tload > 26:
                self.tload_increment = False
        else:
            if self.tload < 3:
                self.tload_increment = True
        x,y = self.tload_randomOrigin(225,410-self.yi)
        self.screen.blit(self.loadingPack[self.tload // 3], (x,y))

    def tload_randomOrigin(self,xin,yin):
        x = xin + rd.choice([-10,-5,0,5,10])
        y = yin + rd.choice([-10,-5,0,5,10])
        return x,y

    def tload_crementing(self):
        if self.tload_increment:
            self.tload += 1
        else:
            self.tload -= 1

    def swipeUpInitScreen(self):
        if self.swipeInit:
            if self.tswipe < 200:
                self.yi += 20
                self.tswipe += 1
            else:
                self.swipeInit = False
                self.runInitScreen = False

    # MAIN SCREEN METHODS
    def drawQuotes(self):
        if self.t1 > 30:
            pic = self.quotesPack[self.quotesPackIdx]
            w = pic.get_rect()[2]
            self.screen.blit(pic,(int(250-w/2),210))
        self.t1 += 1

        if self.t1 > 400:
            self.t1 = 0
            self.quotesPackIdx = rd.choice([0, 1, 2, 3])

    def drawMain(self):
        self.screen.blit(self.mainImage, (0,0))
        w_start = self.startImage[0].get_rect()[2]
        h_start = self.startImage[0].get_rect()[3]
        self.startBlit = self.screen.blit(self.startImage[self.startIdx], (int(245-(w_start/2)),int(340-(h_start/2))))
        self.setBlit = self.screen.blit(self.settingImage[self.setIdx], (int(248-(w_start/2)),int(270-(h_start/2))))
        if self.startBlit.collidepoint(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]):
            self.startIdx = 1
            if pg.mouse.get_pressed()[0]:
                self.startClick = True
            else:
                self.startClick = False
        else:
            self.startIdx = 0
            self.startClick = False
        if self.setBlit.collidepoint(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]):
            self.setIdx = 1
            if pg.mouse.get_pressed()[0]:
                self.setClick = True
            else:
                self.setClick = False
        else:
            self.setIdx = 0
            self.setClick = False

    def drawAll(self):
        if self.runMainScreen:
            self.drawMain()
            self.drawQuotes()
        if self.runInitScreen:
            self.tglobal += 1
            self.drawInit()
            self.drawLoading()
            if self.tglobal > 70:
                self.runMainScreen = True
                self.swipeInit = True
        self.swipeUpInitScreen()
        pg.display.update()

    # GET VALUE FROM UI
    def getSetClick(self):
        return self.setClick

    def getStartClick(self):
        return self.startClick
