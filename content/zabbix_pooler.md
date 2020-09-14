Title: Zabbix poller processes more than 75%
Date: 2020-07-02 19:00
Tags: Zabbix, Shell, Zabbix Poller, Poller proccess
Category: Linux
Slug: zabbix-poller-processes-more-than-75
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Description: Zabbix poller proccess more than 75%

Hey folks, this is the third post about tweaking the Zabbix configurations. All changes that I've suggested here were based on a Zabbix Server with 50+ hosts. Another thing that can happen to your server, it's the poller get overwhelmed by the amount of servers that need to be polled plus the ones that are not responding. Bellow two images where you can see the log and the graphic where you can see the usage percent. 

![Dashboard log about the poller processes](/images/zabbix_pooler.png)

![Graph showing the utilization percent of each collector](/images/zabbix_pooler_3.png)

To solve, let's go back to the `zabbix_server.conf` file and find two variables, `StartPollers` and `StartPollersUnreachable`. Increase them as needed. There's no magic number, you must see what works for you. But keep in mind that the `StartPollersUnreachable` is responsible for that host that can't be "reached"  (of course) and will hold your poller more time.

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

After the change, restart the server and wait a few moments and take a look again at your dashboard. Bellow the effect that I've got.

![Graph showing the new utilization percent of the processes after the changes](/images/zabbix_pooler_4.png)

