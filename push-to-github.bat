@echo off
echo ===============================================
echo   DeltaWorld Python Bot - Push to GitHub
echo ===============================================
echo.

echo STEP 1: Add all files to Git...
git add .

echo.
echo STEP 2: Commit changes...
git commit -m "Ready for Railway deployment"

echo.
echo STEP 3: Set remote repository...
echo.
echo IMPORTANT: Create a new repository on GitHub first!
echo Go to: https://github.com/new
echo Name it: deltaworld-bot (or any name you like)
echo Make sure it's EMPTY (no README, no .gitignore)
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: deltaworld-bot): "

if "%REPO_NAME%"=="" set REPO_NAME=deltaworld-bot

echo.
echo Setting remote to: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo.
echo STEP 4: Push to GitHub...
git branch -M main
git push -u origin main

echo.
echo ===============================================
echo   SUCCESS! Bot code is now on GitHub!
echo ===============================================
echo.
echo NEXT STEPS:
echo 1. Go to https://railway.app/dashboard
echo 2. Click "New Project" - "Deploy from GitHub repo"
echo 3. Select your repository: %REPO_NAME%
echo 4. Add Environment Variables (see БЫСТРЫЙ_СТАРТ.md)
echo.
pause
