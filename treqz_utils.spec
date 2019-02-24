# -*- mode: python -*-
import os

block_cipher = None

added_files = []

a = Analysis(['main.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter', '_bz2', '_ctypes', '_lzma', '_hashlib', 'qt5', 'matplotlib', '_sqlite3', 'babel', 'alabaster', 'sqlalchemy', 'gevent', 'sqlite', 'sphinx', 'docutils', 'numpy', '_multiprocessing', '_decimal', '_ssl', '_socket', 'win32ui', 'win32api', 'win32trace', 'win32wnet'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
		  
excludeBinaries = ['mkl','libopenblas', 'api-ms', 'shell', 'select', 'pythoncom36', 'ucrtbase']
excludeScripts = ['_multiprocessing', '_pkgres', 'comgenpy']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
                break
        if flag != 1:
            outlist.append(item)
    return outlist

def print_elements(input):
    if len(input) == 0:
	    print('no elements')
    else:
        for item in input:
            name, _, type = item
            print(name+" "+type)

a.binaries = remove_from_list(a.binaries, excludeBinaries)
a.scripts = remove_from_list(a.scripts, excludeScripts)

print("#### BINARIES ####")
print_elements(a.binaries)

print("#### SCRIPTS ####")
print_elements(a.scripts)

print("#### ZIPFILES ####")
print_elements(a.zipfiles)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='treqz_utils',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='treqz_utils')