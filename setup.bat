@echo off
echo Setting up Django Interview Scheduler...
echo.

echo Creating migrations...
python manage.py makemigrations
echo.

echo Running migrations...
python manage.py migrate
echo.

echo Setup complete!
echo.
echo To run the server, use: python manage.py runserver
echo To create an admin user, use: python manage.py createsuperuser
pause

