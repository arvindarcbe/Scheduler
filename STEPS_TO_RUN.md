# Steps to Run the Interview Scheduler

## Step-by-Step Instructions

### Step 1: Activate Virtual Environment

**Option A - Using the batch file (Easiest):**
```bash
activate_venv.bat
```

**Option B - Manual activation (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Option C - Manual activation (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**✅ You'll know it's activated when you see `(venv)` at the start of your command prompt**

---

### Step 2: Start the Django Server

**Option A - Using the batch file:**
```bash
run_server.bat
```

**Option B - Manual command:**
```bash
python manage.py runserver
```

**✅ You'll see output like:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Step 3: Open in Browser

Open your web browser and go to:
```
http://127.0.0.1:8000/
```

---

### Step 4: Add Interview Data

1. Click on **"Add Interviews"** in the navigation
2. Paste your interview data in the text area
3. Click **"Add Interviews"** button
4. You'll be redirected to the schedule view

---

### Step 5: View Schedule

- Click on **"View Schedule"** to see the tabulated schedule
- Interviews are automatically organized by date
- Two panels are displayed side by side

---

## Quick Reference

### All-in-One Commands (PowerShell):
```powershell
# Activate and run in one go
.\venv\Scripts\Activate.ps1; python manage.py runserver
```

### Stop the Server:
- Press `CTRL + C` in the terminal

### Deactivate Virtual Environment:
```bash
deactivate
```

---

## Troubleshooting

**If you get "command not found" errors:**
- Make sure you're in the project directory: `C:\Users\aravi\OneDrive\Documents\Project\Scheduler`
- Make sure the virtual environment is activated (you should see `(venv)`)

**If the server won't start:**
- Make sure port 8000 is not in use
- Try: `python manage.py runserver 8080` (to use a different port)

**If you see migration errors:**
- Run: `python manage.py migrate`

---

## Example Workflow

```bash
# 1. Open terminal in project folder
cd C:\Users\aravi\OneDrive\Documents\Project\Scheduler

# 2. Activate virtual environment
activate_venv.bat

# 3. Start server
python manage.py runserver

# 4. Open browser to http://127.0.0.1:8000/

# 5. Add your interview data and view the schedule!
```

