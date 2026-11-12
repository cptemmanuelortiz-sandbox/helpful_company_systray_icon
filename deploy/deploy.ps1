# deploy_example.ps1
# This script is designed to be run via an RMM tool (like Atera, Datto, ConnectWise) 
# Set the RMM script execution context to "Run as Current User".

# ============================================================
# CONFIGURATION - UPDATE THESE WITH YOUR INFO
# ============================================================
$ReleaseUrl = "YOUR_GITHUB_RELEASE_URL_HERE" 
$InstallPath = "$env:LOCALAPPDATA\YourCompanyName\CompanyTools"
$ExeName = "Company_Tools_Hotkey.exe"
$ProcessName = "Company_Tools_Hotkey" # Do not include .exe
# ============================================================

# 1. Create folder
New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
$ExePath = Join-Path $InstallPath $ExeName

# 2. Download the executable
Write-Host "Downloading $ExeName from GitHub..." -ForegroundColor Yellow
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $ReleaseUrl -OutFile $ExePath -UseBasicParsing -ErrorAction Stop
    Write-Host "✅ Download successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ Download failed: $_" -ForegroundColor Red
    exit 1
}

# 3. Stop any currently running instances
Write-Host "Stopping existing instances..." -ForegroundColor Yellow
Stop-Process -Name $ProcessName -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 4. Add to startup registry (So it runs next time they log in)
$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $RegPath -Name "Company_Tools_Hotkey" -Value $ExePath -Force
Write-Host "✅ Added to startup registry" -ForegroundColor Green

# 5. Start the app visibly on the desktop using Task Scheduler
Write-Host "Starting application on the user's desktop..." -ForegroundColor Yellow
try {
    $TaskName = "Start_Company_Tools_Now"
    $Action = New-ScheduledTaskAction -Execute $ExePath
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
    
    # Create the task, run it, and immediately delete it
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Principal $Principal -Force | Out-Null
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 3
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    
    Write-Host "✅ Application launched!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not launch via Task Scheduler: $_" -ForegroundColor Yellow
}

Write-Host "✅ Deployment complete!" -ForegroundColor Green
