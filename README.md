Python Desktop Support Systray App
A lightweight, customizable Python desktop application that places a floating company logo on the user's screen. Users can click the logo to access IT support (which automatically prompts for a description, takes a screenshot, and opens a pre-filled email), quick links, and an intranet page.

This template includes two variations of the application:

Hover Version: The logo remains hidden until the user moves their mouse to the bottom-right corner of the screen.

Hotkey Version: The logo remains hidden until the user presses a specific keyboard combination (e.g., Ctrl + Shift + H).

Features
Silent Background Operation: Runs without a command prompt window.

Prompt to Describe Issue: Prevents blank support tickets by forcing the user to type their issue before taking a screenshot and opening their default email client.

System Tray Backup: Always accessible via a system tray icon.

Drag & Drop: The user can drag the logo to a different position on their screen.

Easy Deployment: Includes a PowerShell script to silently deploy the application via an RMM tool.

How to Customize
Update config.py with your company's email, URLs, and brand colors.

Replace logo.png with your company logo (recommended size: 140x140 pixels).

Customizing the Hotkey (Hotkey Version)
If you are using the Hotkey version (tray_app_hotkey.py), you can easily change the keyboard combination that shows and hides the logo.

Open tray_app_hotkey.py and look for the setup_hotkey function. Find this line:

python
keyboard.add_hotkey('ctrl+shift+h', self.toggle_visibility, suppress=False)
You can change the string inside the quotes to any valid combination supported by the keyboard module. Examples:

'ctrl+shift+h'

'windows+alt+s'

'f12'

If you use multiple keys, separate them with a + sign.

How to Build
You must build the executable on a Windows machine.

Install the requirements:

bash
pip install -r requirements.txt
Build the Hover Version:

bash
py -m PyInstaller --onefile --noconsole --name="Company_Tools_Hover" --add-data "logo.png;." tray_app_hover.py
Build the Hotkey Version:

bash
py -m PyInstaller --onefile --noconsole --name="Company_Tools_Hotkey" --add-data "logo.png;." tray_app_hotkey.py
Example RMM Deployment Script
Included in this repository is a deploy_example.ps1 script. This demonstrates how to securely download the executable from a GitHub release and launch it invisibly via an RMM tool.

Key features of the deployment script:

Installs to LOCALAPPDATA: Bypasses C:\Program Files permission errors for standard users.

Cleans up old versions: Kills the existing process before updating.

Task Scheduler Launch: Uses Register-ScheduledTask to force the .exe to open in the user's interactive desktop session, avoiding the "invisible SYSTEM session" issue common with RMM tools.

Deployment Notes (RMM)
When deploying this application via RMM (Remote Monitoring and Management) tools like ConnectWise, Datto, or Atera, keep these best practices in mind:

Run as Current User: Do not run the deployment script as SYSTEM. GUI applications launched as SYSTEM run in Session 0 and will be invisible to the user.

Install to LOCALAPPDATA: Standard users do not have write access to C:\Program Files. Install the executable to $env:LOCALAPPDATA\YourCompanyName\ to avoid permission errors.

Launch via Task Scheduler: To ensure the application appears visibly on the user's desktop during deployment, use PowerShell's Register-ScheduledTask to launch the .exe interactively in the user's session.

