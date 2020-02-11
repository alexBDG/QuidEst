# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:08:21 2020

@author: Alexandre Banon
"""

import sys
from   PyQt5.QtWidgets import QApplication
import Pages.MenuView as MenuView



app = QApplication.instance() 
if not app: # sinon on crée une instance de QApplication
    app = QApplication(sys.argv)
app.setStyle('Fusion')
fen = MenuView.MenuView()
app.exec_()