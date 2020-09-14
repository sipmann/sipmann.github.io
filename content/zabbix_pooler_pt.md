Title: Zabbix poller processes more than 75%
Date: 2020-07-02 19:00
Tags: Zabbix, Shell, Zabbix Poller, Poller proccess
Category: Linux
Slug: zabbix-poller-processes-more-than-75
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Description: Processo de poller do Zabbix com mais de 75%

Este é o terceiro post sobre configurações para o Zabbix. Todas as alterações que eu sugiro nestes posts, são baseadas em um servidor com 50+ hosts. Outro problema que pode ocorrer em seu servidor, é o poller de informações ficar sobrecarregado pela quantidade de servidores que ele precisa pegar carga de informações juntamente com os servidores que não respondem a requisição. Abaixo duas imagens onde você pode ver o log e um gráfico onde aparecem os percentuais de uso dos poller. 

![Dashboard log sobre o processo do poller](/images/zabbix_pooler.png)

![Gráfico mostrando o percentual de utilização de cada coletor](/images/zabbix_pooler_3.png)

Para resolver o problema acima, vamos voltar ao arquivo de configuração `zabbix_server.conf` e localizar duas variáveis, `StartPollers` e `StartPollersUnreachable`. Aumente o valor delas conforme necessário. Não existe um número mágico, você deve verificar o que melhor funciona para você. Mas tenha em mente que `StartPollersUnreachable` é responsável por aqueles hosts que não respondem ou não são localizados e irão segurar a thread do poller por mais tempo, causando uma fila e um maior processamento/tempo de atualização.

```ini
### Option: StartPollers
#       Number of pre-forked instances of pollers.
#
# Mandatory: no
# Range: 0-1000
# Default:
StartPollers=20

#...

### Option: StartPollersUnreachable
#       Number of pre-forked instances of pollers for unreachable hosts (including IPMI and Java).
#       At least one poller for unreachable hosts must be running if regular, IPMI or Java pollers
#       are started.
#
# Mandatory: no
# Range: 0-1000
# Default:
StartPollersUnreachable=5
```

Depois da alteração, reinicie o serviço e espere alguns momentos e veja o seu dashboard novamente. Abaixo o efeito que a troca teve em um dos servidores que acompanho.

![Gráfico mostrando os novos percentuais de utilização dos processos após as alterações](/images/zabbix_pooler_4.png)

