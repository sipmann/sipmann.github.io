Title: Zabbix Server Out of Memory
Date: 2020-02-27 19:00
Tags: Zabbix, Shell, Out of memory, Crash
Category: Linux
Slug: zabbix-server-out-of-memory-crash
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: Zabbix Server crashing with an out of memory message
Lang: en

Do you have a crashing Zabbix Server and looking through the log `/var/log/zabbix/zabbix_server.log` you see the following out of memory message?

```shell
__mem_malloc: skipped 0 asked 24 skip_min 18446744073709551615 skip_max 0
[file:dbconfig.c,line:94] __zbx_mem_realloc(): out of memory (requested 16 bytes)
[file:dbconfig.c,line:94] __zbx_mem_realloc(): please increase CacheSize configuration parameter
```

Besides the clear solution to the error, that's a common issue on servers that have a few monitoring items on it (servers, switches, firewalls, databases, etc...). To solve, go to your zabbix_server.conf and look for the CacheSize property and set it to a higher value. Its default should be 8M. At a customer that has somewhere between 4 servers, 7 firewalls/appliances, and a few other things, a 32M did the job, but you can set up to 8G.

See ya folks.
