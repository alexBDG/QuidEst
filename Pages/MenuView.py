# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:22:30 2020

@author: Alexandre Banon
"""

import sys, os
from pathlib import Path
from PyQt5.QtWidgets   import QMainWindow, QApplication, QMessageBox
from PyQt5.QtWidgets   import QLabel, QPushButton, QRadioButton
from PyQt5             import uic
from Pages.CreditsView import CreditsView
from Pages.ChoixView   import ChoixView

# Création d'une zone de text éditable
class MenuView(QMainWindow):
    
    def __init__(self, parent=None):
        
        super(MenuView, self).__init__(parent)
        if __name__ == '__main__':
            p = Path(__file__)
            path = os.path.join(str(p.parents[1]), "Pages\\MenuForm.ui")
            self.version = os.path.dirname(os.getcwd()).split("-")[1]
        else:
            self.version = os.path.basename(os.getcwd()).split("-")[1]
            path = "Pages\\MenuForm.ui"
        uic.loadUi(path,self)
        
        self.modes    = ["Apprentissage", "Basique"]
        self.dicModes = {self.modes[0] : "learning",
                         self.modes[1] : "basic"}
        self.mode     = "learning"

        self.button1 = self.findChild(QRadioButton, "radioButton")
        self.button2 = self.findChild(QRadioButton, "radioButton_2")
        self.button3 = self.findChild(QPushButton,  "pushButton")
        self.button4 = self.findChild(QPushButton,  "pushButton_2")
        self.label   = self.findChild(QLabel,       "label_2")
        
        self.label.setText("Version " + self.version)
        
        self.button1.clicked.connect(lambda:self.pushButton1(self.button1))
        self.button2.clicked.connect(lambda:self.pushButton1(self.button2))
        self.button3.clicked.connect(self.pushButton3)
        self.button4.clicked.connect(self.pushButton4)
        
        self.show()

    def pushButton1(self, button, button_linked=None):
        if button.isChecked() == True:
            if button.text() == self.modes[0]:
                self.mode = self.dicModes[self.modes[0]]
            else:
                QMessageBox.warning(self,
                                    "Attention",
                                    "Vous ne pourrez pas bénéficier de la personnalisation.")
                self.mode = self.dicModes[self.modes[1]]
        print(self.mode)    

    def pushButton3(self):
        self.close()
        ChoixView(self)

    def pushButton4(self):
        CreditsView(self)


if __name__ == '__main__':
    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    fen = MenuView()
    app.exec_()