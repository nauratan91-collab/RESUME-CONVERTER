@echo off
title Upload to GitHub - Key Dynamics Resume Converter
color 0A
echo ======================================================================
echo    KEY DYNAMICS SOLUTIONS - UPLOAD RESUME CONVERTER TO GITHUB
echo ======================================================================
echo.
set "PATH=%LOCALAPPDATA%\Programs\Git\cmd;%LOCALAPPDATA%\Programs\Git\mingw64\bin;%PATH%"
cd /d "C:\Users\ITkey\.gemini\antigravity\scratch\resume_converter_app"

git config user.name "nauratan91-collab"
git config user.email "admin@keydynamicssolutions.com"

echo [1/2] Adding updated files to Git...
git add .
git commit -m "Update: Key Dynamics Resume to Word Converter" >nul 2>&1
git branch -M main

git remote remove origin >nul 2>&1
git remote add origin https://github.com/nauratan91-collab/RESUME-CONVERTER.git

echo.
echo [2/2] Pushing updates to: https://github.com/nauratan91-collab/RESUME-CONVERTER.git ...
echo.
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Your Resume Converter has been uploaded to GitHub successfully!
    echo View online: https://github.com/nauratan91-collab/RESUME-CONVERTER
    echo ======================================================================
) else (
    echo.
    echo [ERROR] Push failed. Check your network or GitHub permissions.
)

echo.
pause
