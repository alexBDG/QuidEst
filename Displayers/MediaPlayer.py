# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 09:27:57 2020

@author: Alexandre Banon
"""
   
import sys
import cv2
from PyQt5.QtGui               import QIcon, QFont
from PyQt5.QtCore              import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia        import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets           import QApplication, QFileDialog, QHBoxLayout
from PyQt5.QtWidgets           import QPushButton, QSlider, QStyle
from PyQt5.QtWidgets           import QVBoxLayout, QWidget, QStatusBar
import PyQt5.QtNetwork
 
class VideoPlayer(QWidget):
 
    def __init__(self, img_path, parent=None):
        super(VideoPlayer, self).__init__(parent)
        if __name__ == '__main__':
            self.setWindowTitle("Player")
            self.setGeometry(0, 0, 640, 480)
        else:
            self.setGeometry(0, 0, parent.width(), parent.height())
            self.main = parent
 
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()
 
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
        self.positionSlider.sliderMoved.connect(self.setPosition)
 
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
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)
 
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")
        
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(img_path)))
        self.statusBar.showMessage(img_path)
        
        if __name__ == '__main__':
            self.setLayout(layout)
            self.show()
        else:
            self.main.setLayout(layout)
            

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "All Files *.* ;; MP4 *.mp4 ;; FLV *.flv ;; TS *.ts ;; MTS *.mts ;; AVI *.avi")
 
        if fileName != '':
            self.loadFile(fileName)
            
    def loadFile(self, fileName):
        self.mediaPlayer.setMedia(cv2.VideoCapture(fileName))
#        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.playButton.setEnabled(True)
        self.statusBar.showMessage(fileName)
        self.play()
 
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer("..\\ODetectionCV\\output\\BOXED_TikTok.avi")
    sys.exit(app.exec_())