@echo off
echo ===========================================
echo Setting up custom hostname: scheduler.local
echo ===========================================
echo.
echo This will add scheduler.local to your hosts file.
echo You need Administrator privileges for this.
echo.
pause

echo.
echo Adding scheduler.local to hosts file...
echo 127.0.0.1    scheduler.local >> C:\Windows\System32\drivers\etc\hosts

echo.
echo Done! You can now access the site at:
echo http://scheduler.local:8000/
echo.
pause

