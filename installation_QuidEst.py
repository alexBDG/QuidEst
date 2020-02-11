# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 18:54:59 2020

@author: Alexandre Banon
"""

import os, sys
from win32com.client import Dispatch
import zipfile
import tkinter as tk
from tkinter import filedialog



class Installer:
    
    def __init__(self, parent=None):    
        self.desktop   = os.path.join(os.environ["HOMEPATH"], "Desktop")
        self.documents = os.path.join(os.environ["HOMEPATH"], "Documents")
        self.downloads = os.path.join(os.environ["HOMEPATH"], "Downloads")
        self.file_path = ""
        self.version   = ""


    def zipSelector(self):
        root = tk.Tk()
        root.withdraw()
        self.file_path = filedialog.askopenfilename(initialdir = self.downloads,
                                                    title = "Choisir le document QuidEst-[version].zip")
        
        if len(self.file_path)>0:
            self.version  = os.path.basename(self.file_path).split(".")[0].split("-")[1]
        else:
            sys.exit()


    def zipExtractor(self):
        QEzip = os.path.join(self.downloads, "QuidEst-{0}.zip".format(self.version))
        with zipfile.ZipFile(QEzip, 'r') as zip_ref:
            zip_ref.extractall(self.documents)


    def iconShortcut(self):
        path      = os.path.join(self.desktop,   "QuidEst-{0}.lnk".format(self.version))
        target    = os.path.join(self.documents, "QuidEst-{0}\QuidEst-{0}.exe".format(self.version))
        wDir      = os.path.join(self.documents, "QuidEst-{0}".format(self.version))
        icon      = os.path.join(self.documents, "QuidEst-{0}\QuidEst-{0}.exe".format(self.version))

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        
        shortcut.Targetpath       = target
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation     = icon
        shortcut.save()



if __name__ == '__main__':
    installer = Installer()
    # Choisir le dossier zip
    installer.zipSelector()    
    # Extraction du fichier .zip
    installer.zipExtractor()
    # Création du raccourcis vers le Bureau
    installer.iconShortcut()
