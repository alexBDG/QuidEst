# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:18:34 2020

@author: Alexandre Banon
"""

import sys, os
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5           import uic

# Création d'une zone de text éditable
class CreditsView(QMainWindow):
    
    def __init__(self, parent=None):
        
        super(CreditsView, self).__init__(parent)
        if __name__ == '__main__':
            p = Path(__file__)
            path = os.path.join(str(p.parents[1]), "Pages\\CreditsForm.ui")
        else:
            path = "Pages\\CreditsForm.ui"
        p = Path(__file__)
        path = os.path.join(str(p.parents[1]), "Pages\\CreditsForm.ui")
        uic.loadUi(path,self)
        
        self.button = self.findChild(QPushButton,  "pushButton")
        self.button.clicked.connect(self.pushButton1)
        
        self.show()

    def pushButton1(self):
        self.close()

if __name__ == '__main__':
    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    fen = CreditsView()
    app.exec_()