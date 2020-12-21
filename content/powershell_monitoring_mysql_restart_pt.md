Title: Monitorando restarts do MySQL com PowerShell
Date: 2020-12-21 13:30
Tags: MySQL, MySQL Restart, Powershell monitoring
Category: PowerShell 
Slug: monitoring-mysql-restarts-with-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Description: Monitorando restarts do MySQL com PowerShell
Image: /images/mysql_monitorin_powershell.png

Bom, chegou a hora para mais um script PowerShell. Se você ainda não viu os outros, de uma olhada no link abaixo.

* [Monitorando status de replicação do MySQL com PowerShell](https://www.sipmann.com/pt/monitoring-mysql-replication-with-powershell.html)

Este aqui é um script bem simples, mas novamente, se seu cliente não possui um servidor Zabbix ou não permite que você configure um para realizar este monitoramento, um conjunto de scripts pode ser bem útil. Primeiramente nós executamos uma query báscia `SHOW GLOBAL STATUS LIKE 'Uptime'`, com ela nós conseguimos capturar exatamente o que nós estamos procurando.

Se por alguma razão o comando falhar (verificamos atravez da variábel global `$lastExitCode`), nós mandamos um e-mail lhe avisando sobre o problema ocorrido.

E então, nós chegamos à parte onde fazemos o parse do valor obtido, esta parte é bem similar ao parse que codificamos no primeiro post sobre monitoramento utilizando PowerShell. Nós basicamentes procuramos pela linha contendo `Value`, separamos por espaço e então parseamos a segunda posição em um inteiro. Então tudo que precisamos fazer é verificar se o valor parseado é menor que o nosso threshold, se for menor, nós mandamos um e-mail.

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

Este script (e os outros que eu utilizo) estão disponíveis no meu GitHub [aqui](https://github.com/sipmann/PowerShellScripts). Tenha em mente que os scripts localizados no GitHub, são um pouco diferentes do que exibido aqui. Espero que tenha achado útil.
