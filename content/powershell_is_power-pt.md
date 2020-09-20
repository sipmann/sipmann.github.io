Title: O poder do PowerShell
Date: 2020-09-21 19:00
Tags: Azure, PowerShell, Script, GetChild-Item, Remove-Item, Stop-Proccess
Category: Azure
Slug: the-power-of-powershell
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Status: draft
Image: /images/powershell.png
Lang: pt

Como um usuário linux por muito tempo, eu automatizei algumas tarefas com scripts bash e fiquei longe do PowerShell... Voltei a utilizar Windows alguns anos atrás e ainda assim, não dei uma chance ao PS. Mas porque não? Eu fiz alguns scripts para automatizar algumas tarefas em um servidor Protheus.

Eu acabei achando os scripts PS de fácil leitura e entendimento. Abaixo, nós temos um script para remover arquivos filtrando pela sua extensão (ou sem extensão alguma no caso do script em questão).

```powershell
Get-ChildItem "C:\TOTVS\protheus_data\system" -File -Filter *. | Move-Item -Force -Destination { 
    <# Diretório ao qual os arquivos vão ser movidos. Você pode utilizar formatos de data para nomear os diretórios #>
    <# LastWriteTime é a propriedade do arquivo corrent #>
    $dir = "C:\bad_files\{0:yyyy\\MM\\dd}" -f $_.LastWriteTime
	$null = mkdir $dir -Force 
	"$dir\$($_.Name)"
}
```

Você já precisou remover arquivos baseado no conteúdo de outro arquivo? Abaixo um script onde eu leio um arquivo que contem os nomes de arquivos que eu desejo remover. 

```powershell
foreach($line in Get-Content .\Desktop\bad_files.txt) {
    if (Test-Path('\\x.y.z.a\c$\TOTVS\protheus_data\xmls\'+$line+'.xml')) {
        Remove-Item('\\x.y.z.a\c$\TOTVS\protheus_data\xmls\'+$line+'.xml')
    } else {
        echo $line + ' - File not found'
    }
}
```

E um script bonus para parar e iniciar serviços (se você gerencia um servidor Protheus, você sabe o porque eu faço isto).

```powershell
$servicesNames = 'app_main',
	'app_worker1',
	'app_worker2',
	'app_worker3',
	'app_worker4',
	'app_worker5'

Write-host "Parando Serviços"
Write-host "--------------------------"

foreach ($srv in $servicesNames) {
	Write-host "Parando: " + $srv
    $SrvPID = (get-wmiobject win32_service | where { $_.name -eq $srv}).processID
    Write-host "PID: " + $SrvPID
    
    <# Força a parada caso o serviço esteja travado #>
    Stop-Process $ServicePID -Force
    Write-host "PDI " + $SrvPID + " parado"
}


Write-host "Inicializando Serviços"
Write-host "--------------------------"

foreach ($srv in $servicesNames) {
	Write-host "Inicializando: " + $srv
    Start-Service $srv
}
```

Você tem algum script de automação? Compartilhe conosco :)