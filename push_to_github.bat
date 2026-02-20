@echo off
REM VIVA Project - Fully Automated GitHub Push Script
SET REPO_URL=https://github.com/AHAD2911/AI-Powered-Survey-Platform
SET GIT_EMAIL=sheikhsahab2911@gmail.com
SET GIT_NAME=AHAD2911

echo Setting your identity...
git config --local user.email "%GIT_EMAIL%"
git config --local user.name "%GIT_NAME%"

echo Initializing Git (if not done)...
if not exist .git (
    git init
)

echo Adding all project files...
git add .

echo Creating initial commit...
git commit -m "Initial commit: AI-Powered Survey Platform with Analysis"

echo Setting up remote origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo ============================================================
echo FINAL STEP: PUSHING TO GITHUB
echo Note: A login window from GitHub may appear. 
echo Please sign in if prompted to complete the upload.
echo ============================================================
echo.

git branch -M main
git push -u origin main --force

echo.
echo All done! Your project is now on GitHub.
pause
