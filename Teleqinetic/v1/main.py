import customUI as cui
import settingUI as sui
import HCC


HCCparameters = [[1.2, 3, 1.07, 7, 3, 0.6, 5], [0, 0, 0]]

def openSettingsQT(obj):
    global HCCparameters, warningCamID
    if obj.setClick:
        sui.run()
    HCCparameters = sui.getParameters()

def startCursorControl(camObj, windowObj):
    global HCCparameters
    camObj = camObj.pickClassifier('hcc')
    camObj.inputParameters(HCCparameters)
    if windowObj.startClick:
        camObj.main()

if __name__ == '__main__':
    main = cui.runMain()
    cam = HCC.detClasses('cam',1)
    main.initialize(lambda : openSettingsQT(main),
                    lambda: startCursorControl(cam, main))