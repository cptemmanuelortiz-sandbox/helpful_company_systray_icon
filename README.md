# Python Desktop Support Systray App

A lightweight, customizable Python desktop application that places a floating company logo on the user's screen. Users can click the logo to access IT support (which automatically prompts for a description, takes a screenshot, and opens a pre-filled email), quick links, and an intranet page.

This template includes **two variations** of the application:
1. **Hover Version:** The logo remains hidden until the user moves their mouse to the bottom-right corner of the screen.
2. **Hotkey Version:** The logo remains hidden until the user presses a specific keyboard combination (`Alt + M + R + N + Y`).

## Features
- **Silent Background Operation:** Runs without a command prompt window.
- **Prompt to Describe Issue:** Prevents blank support tickets by forcing the user to type their issue before taking a screenshot and opening their default email client.
- **System Tray Backup:** Always accessible via a system tray icon.
- **Drag & Drop:** The user can drag the logo to a different position on their screen.
- **Easy Deployment:** Includes a PowerShell script to silently deploy the application via an RMM tool.

## How to Customize
1. Update `config.py` with your company's email, URLs, and brand colors.
2. Replace `logo.png` with your company logo (recommended size: 140x140 pixels).

## How to Build
You must build the executable on a Windows machine.

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
