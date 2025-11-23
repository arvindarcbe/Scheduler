# Setup Custom Hostname

## Quick Setup

1. **Run the setup script** (as Administrator):
   - Right-click `setup_hostname.bat`
   - Select "Run as administrator"
   - Click "Yes" when prompted

2. **Start the server**:
   - Run `RUN.bat` or use the terminal commands

3. **Access the site**:
   - Open browser and go to: **http://scheduler.local:8000/**

## Manual Setup (Alternative)

If you prefer to set it up manually:

1. Open Notepad as Administrator:
   - Press `Windows Key`
   - Type: `notepad`
   - Right-click Notepad → "Run as administrator"

2. Open the hosts file:
   - File → Open
   - Navigate to: `C:\Windows\System32\drivers\etc\`
   - Change file type to "All Files"
   - Open `hosts`

3. Add this line at the end:
   ```
   127.0.0.1    scheduler.local
   ```

4. Save and close

5. Start the server and access: **http://scheduler.local:8000/**

## Change the Hostname

If you want a different name (e.g., `interview-scheduler.local`):

1. Edit `scheduler_project/settings.py`:
   - Change `ALLOWED_HOSTS = ['scheduler.local', ...]` to your preferred name

2. Update the hosts file with your new name

3. Restart the server

## Access URLs

After setup, you can access the site using:
- **http://scheduler.local:8000/** (custom hostname)
- **http://127.0.0.1:8000/** (localhost - still works)
- **http://localhost:8000/** (localhost - still works)

