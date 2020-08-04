Title: Zabbix Server Out of Memory log
Date: 2020-02-27 19:00
Tags: Zabbix, Shell, Out of memory, Crash
Category: Linux
Slug: zabbix-server-out-of-memory-crash
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: Zabbix Server caindo com avisos de falta de memória
Lang: pt
Status: Draft

Você tem um servidor Zabbix crashando e observando o arquivo de log `/var/log/zabbix/zabbix_server.log` você localiza a seguinte mensagem referênciando falta de memória?

```shell
__mem_malloc: skipped 0 asked 24 skip_min 18446744073709551615 skip_max 0
[file:dbconfig.c,line:94] __zbx_mem_realloc(): out of memory (requested 16 bytes)
[file:dbconfig.c,line:94] __zbx_mem_realloc(): please increase CacheSize configuration parameter
```

Apesar da simples solução para o erro, isso acaba sendo um problema comum em servidores que tem uma certa quantidade de itens sendo monitorados (servidores, switches, firewalls, bancos, etc...). Para resolver o problema, va até o ser arquivo `zabbix_server.conf` e procure pela propriedade `CacheSize` e sete o seu valor para uma quantidade maior. O seu valor default deve ser algo como 8M. Em clientes que tenham algo como 4 servidores, 7 firewalls/appliances, e algumas outras coisas (bancos, apps), 32M deve resolver o problema, mas você pode setar até algo como 8G (ressalto que mais nem sempre é melhor).

Até breve.
