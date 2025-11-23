@echo off
echo ===========================================
echo Pushing to GitHub
echo ===========================================
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "

echo.
echo Adding remote repository...
git remote add origin https://github.com/%GITHUB_USERNAME%/Scheduler.git

echo.
echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo Done! Your code is now on GitHub.
echo Repository: https://github.com/%GITHUB_USERNAME%/Scheduler
echo.
pause

