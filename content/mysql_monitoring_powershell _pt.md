Title: Monitorando status de replicação do MySQL com PowerShell
Date: 2020-10-14 19:00
Tags: MySQL, MySQL Replication, PowerShell, Powershell mail
Category: PowerShell 
Slug: monitoring-mysql-replication-with-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Description: Monitorando uma replicação MySql com PowerShell, enviando e-mails e muito mais, lhe avisando sobre o estado da replicação.
Image: /images/mysql_monitorin_powershell.webp

Tenho migrado alguns scripts bash que tenho para PowerShell, e chegou a vez de migrar um script de monitoramento de replicação do MySQL. Fica como crédito o script original do [Paweł](https://handyman.dulare.com/mysql-replication-status-alerts-with-bash-script/). É um script bem simples onde eu verifico algumas tags resultantes do `SHOW SLAVE STATUS\G`, são elas. `Slave_IO_Running`, `Slave_SQL_Running` e `Seconds_Behind_Master`. Ainda preciso verificar formas mais corretas de armazenar/carregar as variáveis como usuários e senha, se tiver alguma dica, fique à vontade para inclusive fazer um pull request ([aqui](https://github.com/sipmann/PowerShellScripts)) no repositório onde vou armazenar alguns dos meus scripts.

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