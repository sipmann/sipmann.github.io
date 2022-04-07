Title: Monitoring MySQL restarts with PowerShell
Date: 2020-12-21 13:30
Tags: MySQL, MySQL Restart, Powershell monitoring
Category: PowerShell 
Slug: monitoring-mysql-restarts-with-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Description: Monitoring MySQL for restarts using PowerShell
Image: /images/mysql_monitoring_restart.webp


Hey folks, it's time for another PowerShell script. If you haven't seen the other ones, check the links below.

* [Monitoring MySQL replication with PowerShell](https://www.sipmann.com/en/monitoring-mysql-replication-with-powershell.html)

Well, this one it's a pretty simple script, but again, if your customer doesn't have a Zabbix server or doesn't allow you to setup one to do the monitoring, a set of scripts can be handy. We start executing some basic query `SHOW GLOBAL STATUS LIKE 'Uptime'`, with that we'll get exactly what we're looking for.

If for some reason, the command fails (watch for the "global" variable called `$lastExitCode`), we send an e-mail telling you about that connection problem.

And then, we get to the part where we parse the value, this one is pretty similar to the parse we did on the first post about using PowerShell to monitor MySQL. But we basically look for the Value line, split it by space and then parse the second position to an integer. And then all we have to do is check if the uptime is lower than our threshold, if it is we send an e-mail.

```powershell
$MailFrom = 'maurio[at]sipmann.com'
$MailTo   = 'mauricio[at]sipmann.com'
$MysqlHost = '127.0.0.1'
$MysqlUser = 'root'
$MysqlPass = '123'


$data = $(mysql -h $MysqlHost -u $MysqlUser -p"$MysqlPass" -e "SHOW GLOBAL STATUS LIKE 'Uptime' \G")

<# Unable to execute the sql Command #>
if ($lastExitCode -eq 1) {
	Send-MailMessage -To $MailTo -From $MailFrom  -Subject 'Connection problem' -bodyAsHtml "Connection problem on host ${MysqlHost}" -Credential Get-Credential -SmtpServer 'smtp.office365.com' -Port 587 -UseSsl
	exit
}

$UpTime   = [int](($data | Where-Object { $_ -match 'Value:' }) -split '\s+')[2]

<# If the uptime is lower then 20 minutes #>
if ($UpTime -lt 1200) {
    Send-MailMessage -To $MailTo -From $MailFrom -Subject "MySQL Restarted" -bodyAsHtml "MySQL host ${MysqlHost} restarted less than 20 minutes ago" -Credential Get-Credential -SmtpServer 'smtp.office365.com' -Port 587 -UseSsl
}
```

This script (and the other ones I use) is available at my GitHub [here](https://github.com/sipmann/PowerShellScripts). Keep in mind that the ones on the GitHub repo, are a little different from here.
