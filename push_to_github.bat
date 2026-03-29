@echo off
REM push_to_github.bat - Script to push HydroMind to GitHub

echo.
echo ========================================
echo   HydroMind - GitHub Push Script
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo [*] Initializing Git repository...
    git init
    echo [+] Git initialized
) else (
    echo [+] Git repository already initialized
)

REM Add remote
echo.
echo [*] Setting remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/trashcoder23/Hydromind.git
echo [+] Remote configured

REM Stage all files
echo.
echo [*] Staging files...
git add .

REM Show status
echo.
echo [*] Git Status:
git status --short

REM Commit
echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Initial commit - HydroMind IoT System

echo.
echo [*] Committing changes...
git commit -m "%commit_msg%"

REM Push
echo.
echo [*] Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ========================================
echo [+] Successfully pushed to GitHub!
echo [+] Repository: https://github.com/trashcoder23/Hydromind
echo ========================================
echo.
echo WARNING: Make sure you've removed sensitive data:
echo   - Firebase credentials
echo   - Service account keys  
echo   - API keys
echo.
pause
