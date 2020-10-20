Title: Zabbix Runnion on Low Memory Mode
Date: 2020-10-20 19:00
Tags: Zabbix, Shell, Low memory, Cache
Category: Linux
Slug: zabbix-running-on-low-memory-mode
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Image: /images/zabbix_low_memory.png
Description: How to solve Zabbix Health logging *value cache woring in low memory mode* 
Lang: en

Hey folks, another Zabbix post today. This one it's about increasing the Zabbix Server Cache. It's pretty common (if you have the default settings only) get a warning about your `Zabbix value cache running on low memory mode` at your dashboard or logs.

![Zabbix Dashboard warning about the memory problem](/images/zabbix_low_memory_mode.png)
![Zabbix Dashboard cache graph 70% used](/images/zabbix_cache_filling.png)

To solve, go back to your Zabbix config file (`zabbix_server.conf`) and look for the tag *CacheSize*. Uncomment it and set to a value bigger than 8M (8M it's the default value). In my case, we set a cache of 100M. After the change, restart the service.

```ini
### Option: CacheSize
#       Size of configuration cache, in bytes.
#       Shared memory size for storing host, item and trigger data.
#
# Mandatory: no
# Range: 128K-64G
# Default:
CacheSize=100M #uncomment this line
```

![Zabbix Dashboard resolved memory problem](/images/zabbix_low_memory_solved.png)

See ya folks.
