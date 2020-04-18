# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['DGMM_pyinstaller.py'],
             pathex=['D:\\Programs\\Non-portable\\GH Repositories\\Duck-Game-Music-Manager\\DGMM'],
             binaries=[],
             datas=[('./locales/base.pot', '/locales/'), ('locales/en/LC_MESSAGES/base.mo', 'locales/en/LC_MESSAGES/'), ('locales/en/LC_MESSAGES/base.po', 'locales/en/LC_MESSAGES/'), ('locales/ru/LC_MESSAGES/base.po', 'locales/ru/LC_MESSAGES/'), ('locales/ru/LC_MESSAGES/base.mo', 'locales/ru/LC_MESSAGES/')],
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
          name='DGMM_pyinstaller',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='..\\Images\\FluffyDuck.ico')
