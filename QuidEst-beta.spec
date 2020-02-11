# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\alspe\\Documents\\Python Scripts\\ObjectDetection-beta'],
             binaries=[],
             datas=[('ressources/DSC_0506.JPG', 'ressources'), ('Pages/*.ui', 'Pages'), ('ODetectionCV/yolo-coco/*', 'yolo-coco'), ('plugins/platforms/*.dll', 'platforms'), ('plugins/imageformats/*.dll', 'imageformats'), ('plugins/mediaservice/*.dll', 'mediaservice'), ('plugins/resources/*', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='QuidEst-beta',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='ressources\\icon_001.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='QuidEst-beta')
