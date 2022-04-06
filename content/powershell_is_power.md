Title: The power of PowerShell
Date: 2020-09-21 19:00
Tags: Azure, PowerShell, Script, GetChild-Item, Remove-Item, Stop-Proccess
Category: PowerShell
Slug: the-power-of-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Image: /images/powershell.webp
Lang: en

As a long time Linux user, I've automated a few things with bash scripts and stayed away from PowerShell... I've moved to a Windows environment a few years ago and still, haven gave a shot to PS. But why not? I've made a few scripts to automate some tasks at a Protheus server.

I found the PS scripts being easy to read and understand. Bellow, we have a script to remove files filtering their extension (or no extension at all like the following script). 

```powershell
Get-ChildItem "C:\TOTVS\protheus_data\system" -File -Filter *. | Move-Item -Force -Destination { 
    <# Diretory where the files will be moved. You can use Date formats to help name it #>
    <# LastWriteTime proprtie from the current file #>
    $dir = "C:\bad_files\{0:yyyy\\MM\\dd}" -f $_.LastWriteTime
	$null = mkdir $dir -Force 
	"$dir\$($_.Name)"
}
```

Have you ever been in the need to remove files based on other file content? Bello a script where I read a file that has the names of files that I want to remove. 

```powershell
foreach($line in Get-Content .\Desktop\bad_files.txt) {
    if (Test-Path('\\x.y.z.a\c$\TOTVS\protheus_data\xmls\'+$line+'.xml')) {
        Remove-Item('\\x.y.z.a\c$\TOTVS\protheus_data\xmls\'+$line+'.xml')
    } else {
        echo $line + ' - File not found'
    }
}
```

And a bonus script to stop/start services (if you handle some Protheus Server, you know why I do that).

```powershell
$servicesNames = 'app_main',
	'app_worker1',
	'app_worker2',
	'app_worker3',
	'app_worker4',
	'app_worker5'

Write-host "Stoping Services"
Write-host "--------------------------"

foreach ($srv in $servicesNames) {
	Write-host "Stopping: " + $srv
    $SrvPID = (get-wmiobject win32_service | where { $_.name -eq $srv}).processID
    Write-host "PID: " + $SrvPID
    
    <# Force if the proccess is stucked #>
    Stop-Process $SrvPID -Force
    Write-host "PDI " + $SrvPID + " stopped"
}


Write-host "Starting Services"
Write-host "--------------------------"

foreach ($srv in $servicesNames) {
	Write-host "Starting: " + $srv
    Start-Service $srv
}
```

Do you have any automated script? Share with us :)