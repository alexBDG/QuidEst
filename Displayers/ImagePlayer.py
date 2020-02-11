# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:15:47 2020

@author: Alexandre Banon
"""
   
import sys
from PIL.ImageQt     import ImageQt
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QGraphicsScene
from PyQt5.QtWidgets import QToolButton, QVBoxLayout, QGraphicsView, QStatusBar
from PyQt5.QtCore    import Qt, QDir
from PyQt5.QtGui     import QPixmap, QFont

class ImagePlayer(QWidget):
    
    def __init__(self, img_path, parent=None):
        super(ImagePlayer, self).__init__(parent)
        if __name__ == '__main__':
            self.setWindowTitle("Viewer")
            self.setGeometry(0, 0, 640, 480)
            self.main = QWidget()
        else:
            self.setGeometry(0, 0, parent.width(), parent.height())
            self.main = parent
        
        self.vue = QGraphicsView() 
        self.vue.setDragMode(QGraphicsView.ScrollHandDrag)
        self.vue.wheelEvent = self.wheel_event
        
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)
        
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.vue)
        self.verticalLayout.addWidget(self.statusBar)
        
        self.setPixmapView(img_path)
        
        self.statusBar.showMessage(img_path)
            
        if __name__ == '__main__':
            self.image_btn = QToolButton() 
            self.image_btn.setText("Image") 
            self.image_btn.setObjectName("image_btn") 
            self.image_btn.clicked.connect(self.get_image)
            self.verticalLayout.addWidget(self.image_btn)
            
            self.setLayout(self.verticalLayout)
            self.show()
        else:
            self.main.setLayout(self.verticalLayout)


    def get_image(self):
        img, _p = QFileDialog.getOpenFileName(self, 
                                              "Ouvrir un fichier",
                                              QDir.homePath(),
                                              "All Files *.* ;; PNG *.png ;; JPG *.jpg ;; BMP *.bmp")
        if not img:
            with open("img.txt","w") as file:
                file.write("not img")
            return
        self.setPixmapView(img)
        
        
    def setPixmapView(self, img_path):
        self.current_image = ImageQt(img_path)
        w, h = self.size().width(), self.size().height()
        self.pixmap = QPixmap.fromImage(self.current_image.scaled(w, h, 
                                        Qt.KeepAspectRatio, 
                                        Qt.FastTransformation))
        self.view_current()
        self.statusBar.showMessage(img_path)
        
        
    def view_current(self):
        w_pix, h_pix = self.pixmap.width(), self.pixmap.height()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, w_pix, h_pix)
        self.scene.addPixmap(self.pixmap)
        self.vue.setScene(self.scene)
        

    def wheel_event(self, event):
        steps = event.angleDelta().y() / 120.0
        self.zoom(steps)
        event.accept()
        

    def zoom(self, step):
        w_pix, h_pix = self.pixmap.width(), self.pixmap.height()
        w, h = w_pix * (1 + 0.1*step), h_pix * (1 + 0.1*step)
        self.pixmap = QPixmap.fromImage(self.current_image.scaled(w, h, 
                                        Qt.KeepAspectRatio, 
                                        Qt.FastTransformation))
        self.view_current()
        
        

if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    viewer = ImagePlayer("..\\ressources\\DSC_0506.JPG")
    sys.exit(app.exec_())