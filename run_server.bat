@echo off
echo Starting Django development server...
call venv\Scripts\activate.bat
python manage.py runserver
pause

