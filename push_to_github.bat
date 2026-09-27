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

echo [1/3] Adding all project files to Git...
git add .
git commit -m "Key Dynamics Solutions Resume to Word Converter with Header Logo" >nul 2>&1
git branch -M main

set "DEFAULT_REPO=https://github.com/nauratan91-collab/resume-converter.git"

echo.
echo Default Target Repository:
echo %DEFAULT_REPO%
echo.
set /p REPO_CHOICE="Press ENTER to use default, or paste your GitHub Repo URL: "
if "%REPO_CHOICE%"=="" set "REPO_CHOICE=%DEFAULT_REPO%"

git remote remove origin >nul 2>&1
git remote add origin %REPO_CHOICE%

echo.
echo [2/3] Connecting and Pushing to: %REPO_CHOICE% ...
echo.
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Your Resume Converter has been uploaded to GitHub successfully!
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo [IMPORTANT STEP REQUIRED]
    echo Agar 'Repository not found' aaya hai, iska matlab GitHub par abhi 
    echo ye naya repository create nahi hua hai.
    echo.
    echo Bas ye 2 simple steps kijiye:
    echo 1. Browser me link kholiye: https://github.com/new
    echo 2. Repository Name me likhiye: resume-converter
    echo 3. Neeche green button 'Create repository' par click kijiye.
    echo 4. Uske baad is file ko dobara run kijiye!
    echo ======================================================================
)

echo.
pause
