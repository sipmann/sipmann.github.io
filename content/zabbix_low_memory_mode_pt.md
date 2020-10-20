Title: Zabbix Runnion on Low Memory Mode
Date: 2020-10-20 19:00
Tags: Zabbix, Shell, Low memory, Cache
Category: Linux
Slug: zabbix-running-on-low-memory-mode
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Image: /images/zabbix_low_memory.png
Description: Como resolver o Zabbix alertando sobre *value cache woring in low memory mode* 
Lang: pt
Status: draft

Olá pessoal! Trago hoje outro post sobre Zabbix. Este é sobre aumentar o cache do seu Zabbix Server. É perfeitamente comum (se você roda com as configurações padrões) receber avisos sobre `Zabbix value cache running on low memory mode` no seu dashboard ou arquivos de log.

![Zabbix Dashboard alertando sobre problemas de memória](/images/zabbix_low_memory_mode.png)
![Zabbix Dashboard cache gráfico com 70% utilizado](/images/zabbix_cache_filling.png)

Para resolver, abra o seu arquivo de configuração (`zabbix_server.conf`) e procure pela tag *CacheSize*. Descomente a linha e defina um valor maior que 8M (8M é o valor padrão). No meu caso, nós configuramos um cache de 100M. Depois da troca, reinicie o serviço para que o mesmo tome efeito.

```ini
### Option: CacheSize
#       Size of configuration cache, in bytes.
#       Shared memory size for storing host, item and trigger data.
#
# Mandatory: no
# Range: 128K-64G
# Default:
CacheSize=100M #Descomente esta linha
```

![Zabbix Dashboard resolved memory problem](/images/zabbix_low_memory_solved.png)

Até breve.
