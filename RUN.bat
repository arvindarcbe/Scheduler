@echo off
echo ===========================================
echo Starting Interview Scheduler
echo ===========================================
echo.

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 2: Starting Django server...
echo.
echo Server will start at:
echo   - http://scheduler.local:8000/ (custom hostname)
echo   - http://127.0.0.1:8000/ (localhost)
echo.
echo Press CTRL+C to stop the server when done.
echo.

python manage.py runserver 0.0.0.0:8000

pause

