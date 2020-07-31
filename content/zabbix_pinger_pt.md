Title: Zabbix ICMP pinger processes more than 75%
Date: 2020-05-25 16:00
Tags: Zabbix, icmp pinger, icmp pinger more than 75, Zabbix Server
Category: Linux
Slug: zabbix-icmp-pinger-processes-more-than-75
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: Então o seu systema de monitoramento creasceu e o seu Zabbix começou a printar Zabbix icmp pinger processes more than 75% busy no seu dashboard.
Lang: pt
Status: draft

Então o seu systema de monitoramento creasceu e o seu Zabbix começou a printar "*Zabbix icmp pinger processes more than 75% busy*" no seu dashboard.

![Dashboard do zabbix avisando sobre o erro](images/zabbix_pinger01.png)

Tudo que você tem a fazer é abrir o seu arquivo de configuração (`/etc/zabbix/zabbix_server.conf`) e localizar a tag chamada  `StartPingers`. Ela deve estar comentáda por padrão. Descomente a lina e define o seu valor para algo como 3 or 4. Deve resolver seu problema, ao menos até um próximo crescimento do seu monitoramento.

```shell

### Option: StartPingers
#       Number of pre-forked instances of ICMP pingers.
#
# Mandatory: no
# Range: 0-1000
# Default:
StartPingers=4
```

