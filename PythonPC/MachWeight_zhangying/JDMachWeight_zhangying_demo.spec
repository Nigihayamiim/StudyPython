# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['JDMachWeight_zhangying_demo.py'],
             pathex=['C:\\Users\\WaitingForTheName\\PycharmProjects\\StudyPython\\PythonPC\\MachWeight_zhangying'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='JDMachWeight_zhangying_demo',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='1.ico')
