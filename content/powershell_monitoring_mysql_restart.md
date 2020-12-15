Title: Monitoring MySQL restarts with PowerShell
Date: 2020-12-14 19:00
Tags: MySQL, MySQL Restart, Powershell monitoring
Category: PowerShell 
Slug: monitoring-mysql-restarts-with-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com

Lang: en
Description: Monitoring MySQL for restarts using PowerShell
Image: /images/mysql_monitorin_powershell.png

Hey folks, it's time for another PowerShell script. If you haven't seen the other ones, check the links bellow.

* [Monitoring MySQL replication with PowerShell](https://www.sipmann.com/en/monitoring-mysql-replication-with-powershell.html)

Well, this one it's a pretty simple script, but again, if your customer don't have a Zabbix server or don't allow you to setup a Zabbix Server to do the monitoring, a set of scripts can be handy. We start executing some basic query `SHOW GLOBAL STATUS LIKE 'Uptime'`, with that we'll get exactly what we're looking for.

If, for some reason, the command fails (watch for the "global" variable called `$lastExitCode`), we send and e-mail telling about that connection problem.

And then, we get to the part where we parse the value, this one is pretty similar to the parse we did on the first post about using PowerShell to monitor MySQL. But we basically first look for the Value line, split it by space and then parse the second position to integer. And then all we have to do is check if the uptime is lower then our threshold, if it is we send an e-mail.

```powershell
$data = $(mysql -h $MysqlHost -u $MysqlUser -p"$MysqlPass" -e "SHOW GLOBAL STATUS LIKE 'Uptime' \G")

<# Unable to execute the sql Command #>
if ($lastExitCode -eq 1) {
	Send-MailMessage -To $MailTo -From $MailFrom  -Subject 'Connection problem' -bodyAsHtml "Connection problem on host ${$MysqlHost}" -Credential $MailCred -SmtpServer 'smtp.office365.com' -Port 587 -UseSsl
	exit
}

$UpTime   = [int](($data | Where-Object { $_ -match 'Value:' }) -split '\s+')[2]

<# If the uptime is lower then 20 minutes #>
if ($UpTime -lt 1200) {
    Send-MailMessage -To $MailTo -From $MailFrom -Subject "MySQL Restarted" -bodyAsHtml "MySQL host ${MysqlHost} restarted in less than 20 minutes" -Credential $MailCred -SmtpServer 'smtp.office365.com' -Port 587 -UseSsl
}
```
