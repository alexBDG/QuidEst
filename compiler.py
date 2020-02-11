# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:09:28 2020

@author: Alexandre Banon
"""


import os

version = os.path.basename(os.getcwd()).split("-")[1]

os.system('pyinstaller'                                             +
          ' --icon=ressources/icon_001.ico'                         +
          ' --name QuidEst-' + version                              +
#          ' --onefile'                                            +
          ' --noconsole'                                            +
          ' --noconfirm'                                            +
#          ' --log-level=DEBUG'                                      +
          ' --add-data="ressources/DSC_0506.JPG;ressources"'        +
          ' --add-data="Pages/*.ui;Pages"'                          +
          ' --add-data="ODetectionCV/yolo-coco/*;yolo-coco"'        +
#          ' --add-data="ODetectionCV/videos/TikTok.mp4;ressources"' +
          ' --add-data="plugins/platforms/*.dll;platforms"'         +
          ' --add-data="plugins/imageformats/*.dll;imageformats"'   +
          ' --add-data="plugins/mediaservice/*.dll;mediaservice"'   +
          ' --add-data="plugins/resources/*;resources"'   +
          ' main.py')