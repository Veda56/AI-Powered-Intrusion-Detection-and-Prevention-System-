@echo off
chcp 65001
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AATIS Security System.lnk'); $Shortcut.TargetPath = 'C:\Users\vedag\OneDrive\Desktop\AATIS-Security-System ( Final) - Copy\run_as_admin.bat'; $Shortcut.WorkingDirectory = 'C:\Users\vedag\OneDrive\Desktop\AATIS-Security-System ( Final) - Copy'; $Shortcut.Save()"
echo AATIS will now start automatically with Windows!
pause