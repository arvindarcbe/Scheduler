# Interview Panel Scheduler

A Django application for scheduling interview panels for candidates across two panels.

## Features

- Add single or multiple interview entries at once
- Automatic panel assignment based on time conflicts
- Tabulated display of interviews split across 2 panels
- Replace existing data when new data is added
- Beautiful and modern UI

## Installation

1. **Create and activate virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```
   
   **Windows (PowerShell):**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```bash
   venv\Scripts\activate.bat
   ```
   
   Or use the provided script:
   ```bash
   activate_venv.bat
   ```

2. **Install Django:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   Or use the setup script:
   ```bash
   setup.bat
   ```

3. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## Usage

1. **Add Interviews**: 
   - Navigate to "Add Interviews" page
   - Paste your interview data in the text area
   - Format: "Day Month Candidate with Company from StartTime to EndTime"
   - Example: "24th nov priyanka with Deloitte from 11am to 12pm"
   - Click "Add Interviews" button
   - Note: Adding new data will replace all existing interviews

2. **View Schedule**:
   - Navigate to "View Schedule" page
   - See all interviews organized by date
   - Each date shows two panels side by side
   - Interviews are automatically assigned to panels to avoid time conflicts

## Data Format

The application accepts interview data in the following format:
```
24th nov priyanka with Deloitte from 11am to 12pm
24th Nov Sugumar with metric from 11.30 am to 12.30 pm
25th November sowmiya with tcs from 11.00am to 12.00pm
```

## Panel Assignment Logic

- Interviews are automatically assigned to Panel 1 or Panel 2
- The system ensures no time conflicts within the same panel
- If both panels have conflicts, the interview is assigned to the panel with fewer interviews

## Admin Access

Access the Django admin panel at:
```
http://127.0.0.1:8000/admin/
```

