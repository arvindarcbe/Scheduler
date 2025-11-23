# PowerShell script to activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green

# Check if venv exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To start the server, run: python manage.py runserver" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
}

