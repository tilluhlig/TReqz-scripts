@echo off

echo ##### BUILD #####
pyinstaller --clean treqz_utils.spec

del "dist\treqz_utils.zip"
7z a -r -aoa -tzip -m0=LZMA -myx=9 -mx=9 -mfb=256 -md=32m dist\treqz_utils.zip dist\treqz_utils
pause