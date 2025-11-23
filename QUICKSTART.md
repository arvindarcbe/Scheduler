# Quick Start Guide

## Installation Steps

1. **Create Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**:
   
   **Windows (PowerShell):**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```bash
   venv\Scripts\activate.bat
   ```
   
   Or simply run:
   ```bash
   activate_venv.bat
   ```

3. **Install Django and dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Setup Script** (Windows):
   ```bash
   setup.bat
   ```
   
   Or manually:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the Application**:
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Click "Add Interviews" to add your interview data
   - Click "View Schedule" to see the tabulated schedule

## Adding Interview Data

1. Go to the "Add Interviews" page
2. Paste your interview data in the text area
3. Click "Add Interviews" button
4. The system will automatically:
   - Parse all interview entries
   - Assign them to Panel 1 or Panel 2 (avoiding time conflicts)
   - Replace all existing interviews with the new data

## Data Format

The system accepts data in this format:
```
24th nov priyanka with Deloitte from 11am to 12pm
24th Nov Sugumar with metric from 11.30 am to 12.30 pm
25th November sowmiya with tcs from 11.00am to 12.00pm
```

**Supported formats:**
- Dates: "24th nov", "24 Nov", "24th November"
- Times: "11am", "11:30am", "11.30 am", "2pm", "2:00pm"
- Case insensitive
- Flexible spacing

## Features

- ✅ Automatic panel assignment (2 panels)
- ✅ Conflict detection (no overlapping interviews in same panel)
- ✅ Tabulated display by date
- ✅ Replace existing data when adding new entries
- ✅ Beautiful, modern UI
- ✅ Responsive design

## Admin Access

To access Django admin panel:
1. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
2. Go to: `http://127.0.0.1:8000/admin/`

