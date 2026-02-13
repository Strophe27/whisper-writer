$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\Strophe\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\WhisperWriter.lnk")
$Shortcut.TargetPath = "python"
$Shortcut.Arguments = "D:\Users\Strophe\Documents\°IA\STT\Wihisper-Writer\whisper-writer\run.py"
$Shortcut.WorkingDirectory = "D:\Users\Strophe\Documents\°IA\STT\Wihisper-Writer\whisper-writer"
$Shortcut.IconLocation = "D:\Users\Strophe\Documents\°IA\STT\Wihisper-Writer\whisper-writer\assets\ww-logo.ico"
$Shortcut.Description = "WhisperWriter - Speech to Text Application"
$Shortcut.Save() 