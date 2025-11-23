# 🚀 START HERE - Quick Run Guide

## ⚠️ IMPORTANT: Activate Virtual Environment First!

You **MUST** activate the virtual environment before running the server.

---

## For PowerShell Users (Recommended)

### Method 1: Use PowerShell Script
```powershell
.\activate_venv.ps1
python manage.py runserver
```

### Method 2: Manual Activation
```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

**If you get an execution policy error**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## For Command Prompt Users

```cmd
venv\Scripts\activate.bat
python manage.py runserver
```

Or simply:
```cmd
activate_venv.bat
python manage.py runserver
```

---

## ✅ How to Know It's Activated

You should see `(venv)` at the start of your prompt:
```
(venv) PS C:\Users\aravi\OneDrive\Documents\Project\Scheduler>
```

---

## 🌐 Access the Application

Once the server is running, open your browser:
```
http://127.0.0.1:8000/
```

---

## 🛑 To Stop the Server

Press `CTRL + C` in the terminal

---

## 📝 Complete Example (PowerShell)

```powershell
# Step 1: Navigate to project (if not already there)
cd C:\Users\aravi\OneDrive\Documents\Project\Scheduler

# Step 2: Activate virtual environment
.\venv\Scripts\Activate.ps1

# Step 3: Start server
python manage.py runserver

# Step 4: Open browser to http://127.0.0.1:8000/
```

---

## ❌ Common Error Fix

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solution:** You forgot to activate the virtual environment!
- Run: `.\venv\Scripts\Activate.ps1` (PowerShell)
- Or: `venv\Scripts\activate.bat` (Command Prompt)

