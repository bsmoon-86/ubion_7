Set WshShell = CreateObject ("WScript.shell")
Dim strArgs
strArgs = "C:\Users\moons\Documents\GitHub\ubion_7\230411\crawlling.bat"
WshShell.Run strArgs, 0, false