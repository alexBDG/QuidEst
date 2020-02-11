# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:53:06 2020

@author: Alexandre Banon
"""

import sys
import cv2
from PyQt5.QtGui               import QImage, QPixmap, QIcon, QFont
from PyQt5.QtCore              import QTimer, QDir, Qt, QSize
from PyQt5.QtWidgets           import QApplication, QFileDialog
from PyQt5.QtWidgets           import QPushButton, QSlider, QStyle
from PyQt5.QtWidgets           import QWidget, QLabel, QSizePolicy
from PyQt5.QtWidgets           import QVBoxLayout, QStatusBar, QHBoxLayout


class VideoPlayer(QWidget):
    
    def __init__(self, img_path, parent=None):
        super(VideoPlayer, self).__init__(parent)
        if __name__ == '__main__':
            self.setWindowTitle("Player")
            self.setGeometry(0, 0, 640, 480)
        else:
            self.setGeometry(0, 0, parent.width(), parent.height())
            self.main = parent
        
        self.fileName = img_path
        btnSize = QSize(16, 16)
        self.videoWidget = QLabel()
        self.videoWidget.setAlignment(Qt.AlignCenter)
 
        if __name__ == '__main__':
            openButton = QPushButton()
            openButton.setToolTip("Open Video File")
            openButton.setStatusTip("Open Video File")
            openButton.setFixedHeight(24)
            openButton.setIconSize(btnSize)
            openButton.setText("Vidéo") 
            openButton.setFont(QFont("Noto Sans", 8))
            openButton.setIcon(QIcon.fromTheme("document-open"))
            openButton.clicked.connect(self.openFile)
 
        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
 
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
 
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)
 
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        if __name__ == '__main__':
            controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
 
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)
 
        self.loadFile(self.fileName)
        self.statusBar.showMessage(self.fileName)
        
        if __name__ == '__main__':
            self.setLayout(layout)
            self.show()
        else:
            self.main.setLayout(layout)
            


    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath(), "All Files *.* ;; MP4 *.mp4 ;; FLV *.flv ;; TS *.ts ;; MTS *.mts ;; AVI *.avi")
 
        if self.fileName != '':
            self.loadFile(self.fileName)
            
            
    def loadFile(self, fileName):
        self.state = "WaitingState"
        self.mediaStateChanged()
        self.cap = cv2.VideoCapture(str(fileName))
        self.frame_num = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.durationChanged()
        self.frame_count = 0
        self.statusBar.showMessage(fileName)
        
 
    def play(self):
        if self.state == "PlayingState":
            self.pause()
        elif self.state == "WaitingState":
            self.start()
        else:
            self.state = "PlayingState"
            self.mediaStateChanged()
            self.cap = cv2.VideoCapture(str(self.fileName))
            self.frame_count = 0
            
            
    def pause(self):
        self.state = "WaitingState"
        self.mediaStateChanged()
        self.timer.stop()
        
            
    def start(self):
        self.state = "PlayingState"
        self.mediaStateChanged()
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.cap.get(cv2.CAP_PROP_FPS))
        

    def nextFrameSlot(self):
        self.frame_count += 1
        self.positionChanged()
        ret, frame = self.cap.read()
        if ret:
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            img = img.rgbSwapped()
            if __name__ == '__main__':
                w, h = self.videoWidget.size().width(), self.videoWidget.size().height()
            else:
#                TODO : Gérer le problème d'agrandissement de la fenêtre
                w, h = self.size().width(), self.size().height()
            pix = QPixmap.fromImage(img.scaled(w, h, 
                                        Qt.KeepAspectRatio, 
                                        Qt.FastTransformation))
            self.videoWidget.setPixmap(pix)
        else:
            self.state = "FinishingState"
            self.mediaStateChanged()
        
        
    def mediaStateChanged(self):
        if self.state == "PlayingState":
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        elif self.state == "WaitingState":
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaStop)) 
            
            
 
    def positionChanged(self):
        self.positionSlider.setValue(self.frame_count)
        
 
    def durationChanged(self):
        self.positionSlider.setRange(0, self.frame_num)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer("..\\ODetectionCV\\output\\BOXED_TikTok.avi")
    sys.exit(app.exec_())