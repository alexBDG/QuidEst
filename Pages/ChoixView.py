# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 23:14:42 2020

@author: Alexandre Banon
"""

import os, sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox
from PyQt5.QtWidgets import QLabel, QPushButton, QProgressBar, QSlider
from PyQt5.QtWidgets import QTabWidget, QWidget, QStyle
from PyQt5           import uic
from PyQt5.QtCore    import QDir

if __name__ == '__main__':
    module_path = os.getcwd() + "\\.."
    if not module_path in sys.path:
        sys.path.append(module_path)
from ODetectionCV.YoloCocoImage import YoloCocoImage
from ODetectionCV.YoloCocoVideo import YoloCocoVideo
from Displayers.VideoPlayer     import VideoPlayer
from Displayers.ImagePlayer     import ImagePlayer

# Création d'une zone de text éditable
class ChoixView(QMainWindow):
    
    def __init__(self, parent=None):
        
        super(ChoixView, self).__init__(parent)
        self.img_list = ["bmp","dib",
                         "jpeg","jpg","jpe","JPG",
                         "jp2",
                         "png",
                         "pbm","pgm","ppm",
                         "sr","ras",
                         "tiff","tif"]
        self.video_list = ["avi","mp4"]
        self.yolo    = None
        self.player = None
        self.player2 = None
        self.player5 = None
        self.player6 = None
        
        if __name__ == '__main__':
            p = Path(__file__)
            path = os.path.join(str(p.parents[1]), "Pages\\ChoixForm.ui")
            self.img_path = os.path.join(str(p.parents[1]), "ressources\\DSC_0506.JPG")
            self.img_folder = os.path.join(str(p.parents[1]), "ressources")
        else:
            path = "Pages\\ChoixForm.ui"
            self.img_path = "ressources\\DSC_0506.JPG"
            self.img_folder = "ressources"
            
        uic.loadUi(path,self)

        self.label1   = self.findChild(QLabel,       "label")
        self.label2   = self.findChild(QLabel,       "label_2")        
        self.button1  = self.findChild(QPushButton,  "pushButton")
        self.button2  = self.findChild(QPushButton,  "pushButton_2")
        self.progress = self.findChild(QProgressBar, "progressBar")
        self.slider1  = self.findChild(QSlider,      "horizontalSlider")
        self.slider2  = self.findChild(QSlider,      "horizontalSlider_2")
        self.label5   = self.findChild(QLabel,       "label_5")
        self.label6   = self.findChild(QLabel,       "label_6")
        self.tab      = self.findChild(QTabWidget,   "tabWidget")
        self.subtab   = self.findChild(QWidget,      "tab")
        self.subtab2  = self.findChild(QWidget,      "tab_2")
        self.subtab5  = self.findChild(QWidget,      "tab_5")
        self.subtab6  = self.findChild(QWidget,      "tab_6")

        (self.player, self.player5) = self.activeImage(self.img_path, 
                                                       self.subtab, self.subtab5,
                                                       self.player, self.player5)
        
        self.button1.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        
        self.progress.hide()
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.tab.removeTab(2)
        self.tab.removeTab(2)
        
        self.button1.clicked.connect(self.pushBoutton1)
        self.button2.clicked.connect(self.pushBoutton2)
        self.slider1.valueChanged.connect(lambda:self.valueChange(self.slider1, self.label5))
        self.slider2.valueChanged.connect(lambda:self.valueChange(self.slider2, self.label6))
        
        self.show()
        

    def pushBoutton1(self):
        filters = "All Files (*.*) ;; PNG File (*.png) ;; JPG File (*.JPG) ;; MP4 File (*.mp4) ;; AVI File (*.avi)"
        file_path, _ = QFileDialog.getOpenFileName(self, 
                                                   "Ouvrir un fichier",
                                                   QDir.homePath(),
                                                   filters)
        file_format = os.path.basename(file_path).split(".")[1]

        if os.path.isfile(str(file_path)):
            self.img_path = file_path
        else:
            QMessageBox.critical(self,
                                 "Erreur",
                                 "Le fichier choisis n'en est pas un !")

        self.tab.removeTab(0)
        self.tab.removeTab(0)
        
        if file_format in self.video_list:
            self.tab.addTab(self.subtab5, "Entrée-V")
            self.tab.addTab(self.subtab6, "Sortie-V")
            self.progress.show()
            try:
                self.button2.clicked.connect(self.updateBar)
            except TypeError:
                pass
            for el in [self.slider1, self.slider2]:
                try:
                    el.valueChanged.connect(self.updateBar)
                except TypeError:
                    pass
                
        elif file_format in self.img_list:
            self.tab.addTab(self.subtab,  "Entrée-I")
            self.tab.addTab(self.subtab2, "Sortie-I")
            self.progress.hide()
            try:
                self.button2.clicked.disconnect(self.updateBar)
            except TypeError:
                pass
            for el in [self.slider1, self.slider2]:
                try:
                    el.valueChanged.disconnect(self.updateBar)
                except TypeError:
                    pass
            
        else:
            QMessageBox.warning(self,
                                "Attention",
                                "Cette extention de fichier n'est pas reconnue.")
            
        (self.player, self.player5) = self.activeImage(self.img_path, 
                                                       self.subtab, self.subtab5,
                                                       self.player, self.player5)
            
            
    def pushBoutton2(self):
        print("Lancement du calcul ...")
        file_format = os.path.basename(self.img_path).split(".")[1]
        if __name__ == '__main__':
            yolo_path   = module_path + "\\ODetectionCV\\yolo-coco"
            output_path = module_path + "\\ODetectionCV\\output"

        else:
            yolo_path   = "yolo-coco"
            output_path = "ressources"
        
        if file_format in self.img_list:
            self.yolo = YoloCocoImage(arg_image      = self.img_path,
                                      arg_yolo       = yolo_path,
                                      arg_confidence = float(self.label5.text()),
                                      arg_threshold  = float(self.label6.text()),
                                      arg_output     = output_path)
            
        elif file_format in self.video_list:
            self.yolo = YoloCocoVideo(arg_video      = self.img_path,
                                      arg_yolo       = yolo_path,
                                      arg_confidence = float(self.label5.text()),
                                      arg_threshold  = float(self.label6.text()),
                                      arg_output     = output_path)
            duration = (self.yolo.elap*self.yolo.total)
            QMessageBox.information(self,
                                    "Estimation",
                                    "Le calcul devrait durer : {0} mn {1} s".format(int(duration/60.),round(duration%60)))
            # loop over frames from the video file stream
            grabbed = False
            while not grabbed:
                self.progress.setValue(100.*self.yolo.ide/(self.yolo.total-1))
                grabbed = self.yolo.LaunchOnVideo(arg_confidence = float(self.label5.text()),
                                                  arg_threshold  = float(self.label6.text()))
            
        (self.player2, self.player6) = self.activeImage(self.yolo.output_file, 
                                                        self.subtab2, self.subtab6,
                                                        self.player2, self.player6)
        

    def activeImage(self, img_path, subtabI, subtabV, playerI, playerV):
        file_format = os.path.basename(self.img_path).split(".")[1]
        print(img_path)
        if file_format in self.img_list:
            if playerI != None:
                playerI.setPixmapView(img_path)
            else:
                playerI = ImagePlayer(img_path, subtabI)
            
        elif file_format in self.video_list:
            if playerV != None:
                playerV.loadFile(img_path)
            else:
                playerV = VideoPlayer(img_path, subtabV)
        
        return (playerI, playerV)


    def updateBar(self):
        self.progress.setValue(0)


    def valueChange(self, slider, label):
        value = slider.value()/10.
        label.setText(str(value))
    


if __name__ == '__main__':
    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    fen = ChoixView()
    app.exec_()