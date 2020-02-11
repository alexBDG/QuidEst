# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:53:06 2020

@author: Alexandre Banon
"""

import sys
import cv2
from PyQt5.QtGui               import QImage, QPixmap, QIcon, QFont
from PyQt5.QtCore              import QTimer, QDir, Qt, QUrl, QSize
from PyQt5.QtWidgets           import QApplication, QFileDialog, QMainWindow
from PyQt5.QtWidgets           import QPushButton, QAction, QSlider, QStyle
from PyQt5.QtWidgets           import QWidget, QLabel, QFormLayout
from PyQt5.QtWidgets           import QVBoxLayout, QStatusBar, QHBoxLayout


class VideoCapture(QWidget):
    
    def __init__(self, filename, parent):
        super(QWidget, self).__init__()
        self.cap = cv2.VideoCapture(str(filename))
        self.video_frame = QLabel()
        self.frame_num = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        parent.layout.addWidget(self.video_frame)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img.rgbSwapped())
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.cap.get(cv2.CAP_PROP_FPS))

    def pause(self):
        self.timer.stop()


class VideoDisplayWidget(QWidget):
    def __init__(self,parent):
        super(VideoDisplayWidget, self).__init__(parent)

        self.layout = QFormLayout(self)

        self.startButton = QPushButton('Start', parent)
        self.startButton.clicked.connect(parent.startCapture)
        self.startButton.setFixedWidth(50)
        self.pauseButton = QPushButton('Pause', parent)
        self.pauseButton.setFixedWidth(50)
        self.layout.addRow(self.startButton, self.pauseButton)

        self.setLayout(self.layout)


class ControlWindow(QMainWindow):
    def __init__(self):
        super(ControlWindow, self).__init__()
        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle("PyTrack")

        self.capture = None

        self.videoFileName = None

        self.isVideoFileLoaded = False

        self.openVideoFile = QAction("&Open Video File", self)
        self.openVideoFile.setShortcut("Ctrl+Shift+V")
        self.openVideoFile.setStatusTip('Open .h264 File')
        self.openVideoFile.triggered.connect(self.loadVideoFile)

        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openVideoFile)

        self.videoDisplayWidget = VideoDisplayWidget(self)
        self.setCentralWidget(self.videoDisplayWidget)

    def startCapture(self):
        if not self.capture and self.isVideoFileLoaded:
            self.capture = VideoCapture(self.videoFileName, self.videoDisplayWidget)
            self.videoDisplayWidget.pauseButton.clicked.connect(self.capture.pause)
        self.capture.start()
        
    def loadVideoFile(self):
        try:
            self.videoFileName, _ = QFileDialog.getOpenFileName(self, 'Select .h264 Video File')
            self.isVideoFileLoaded = True
        except:
            print("Please select a .h264 file")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    sys.exit(app.exec_())
            