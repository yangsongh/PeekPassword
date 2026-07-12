@echo off

:: 解除文件占用
taskkill /im PeekPassword.exe /f >nul 2>&1

pyinstaller --distpath build --workpath %PYINSTALLER_CACHE_DIR% --noconfirm PeekPassword.spec
