@echo off
REM ===========================
REM Build ClockGUI EXE
REM ===========================

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist LibreDotaPlus.spec del /f /q LibreDotaPlus.spec

REM Make sure PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Build the EXE
pyinstaller --onefile --windowed --name LibreDotaPlus main.py

REM Copy sounds folder next to EXE
xcopy /E /I /Y sounds dist\sounds

REM Copy default settings file if not exists
if not exist dist\event_settings.json copy event_settings.json dist\event_settings.json

echo.
echo ===========================
echo Build complete!
echo Check the dist folder for ClockGUI.exe with sounds folder
echo ===========================
pause
