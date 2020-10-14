Title: Monitoring MySQL Replication Status with PowerShell
Date: 2020-10-15 19:00
Tags: MySQL, MySQL Replication, PowerShell, Powershell mail
Category: Azure 
Slug: monitoring-mysql-replication-with-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Description: Monitoring a MySQL replication with PowerShell, sending e-mails and even more to warn you about the replica state.
Image: /images/mysql_monitorin_powershell.png

I've been migration some bash scripts that I have to PowerShell, and it's time to migrate a script that monitors the replication of a MySQL database. The credit for the original script goes to [Paweł](https://handyman.dulare.com/mysql-replication-status-alerts-with-bash-script/). It's a simple script where I seek a few tags/fields that we get from `SHOW SLAVE STATUS\G` command, the fields are. `Slave_IO_Running`, `Slave_SQL_Running`, and `Seconds_Behind_Master`. I still need to figure out the proper way to store/read variables like usernames and passwords, if you have any tips, feel free to even make a pull request ([here](https://github.com/sipmann/PowerShellScripts)) at the git where I'll store some scripts.

```powershell
<#
   Variables definition
#>
$MaxSeconds = 120  # Max seconds behind master allowed
$MysqlUser  = 'root'
$MysqlPass  = ''

$MailTo     = 'mauricio@sipmann.com'
$MailFrom   = 'mauricio@sipmann.com'


$data = $(mysql -u $MysqlUser -p"$MysqlPass" -e 'SHOW SLAVE STATUS \G')

#Debug data
#$data = Get-Content 'c:\temp\sampleresult.txt'

<# Parse the data #>
$IORunning   = (($data | Where-Object { $_ -match 'Slave_IO_Running:' }) -split '\s+')[2]
$SQLRunning  = (($data | Where-Object { $_ -match 'Slave_SQL_Running:' }) -split '\s+')[2]
$LastErrNo   = (($data | Where-Object { $_ -match 'Last_Errno' }) -split '\s+')[2]
$SecondsBh   = [int](($data | Where-Object { $_ -match 'Seconds_Behind_Master' }) -split '\s+')[2]

If ($IORunning -Eq 'No' -Or $SQLRunning -Eq 'No' -Or $SecondsBh -gt $MaxSeconds) {
	$MailBody = '<h1>Problema na replicação</h1><br>'
	
	$MailBody += '    IO Running: ' + ($IORunning)  + '<br>'
	$MailBody += '   SQL Running: ' + ($SQLRunning) + '<br>'
	$MailBody += 'Seconds Behind: ' + ($SecondsBh) + '<br>'
	$MailBody += '   Last Err No: ' + ($LastErrNo) + '<br>'
	
	<# Send e-mail, maybe some telegram message here too #>
	Send-MailMessage -To $MailTo -From $MailFrom  -Subject 'Problemas na replicação' -bodyAsHtml $MailBody -Credential (Get-Credential) -SmtpServer 'smtp.office365.com' -Port 587 -UseSsl
} Else {
    Write-Host "Up and running"
}
```