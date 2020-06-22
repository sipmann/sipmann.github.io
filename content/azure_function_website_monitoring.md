Title: Monitoring a Website heath with Azure Functions
Date: 2020-06-22 19:00
Tags: Azure, Azure Devops, C#, Dotnet Core, DotNet, Monitor Website
Category: Azure
Slug: monitoring-website-heath-with-azure-functions
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Image: /images/azure_monitoring.png
Description: Monitoring website health with azure functions and csharp.

Sometimes you get your self in need to monitor a website's health or it's content for changes. Of course, there's plenty of options out there, but for the sake of curiosity, let's code our own to see what we can do. First things first. Everything you'll see here, you can achieve with the [free tier](https://azure.microsoft.com/free/) of azure.

The main idea of our app will be to monitor website health (status code). To create a new Azure Function Project, follow the steps below.

![Steps to create a azure function project](/images/azure_functions.gif)

After creating the project, you'll have a few files. Open your main file and start coding. The main file will have a function called `Run`  and you can code your request method. I've created an `async` method to make the request and log the output at the console. The full code you can see below.

```c#
using System;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;

namespace Sipmann.CheckMySite
{
    public static class HttpCheck
    {

        private static async Task GetTask(string url, ILogger log)
        {
            var request = new HttpRequestMessage(HttpMethod.Get, url);

            var client = new HttpClient();
            var response = await client.SendAsync(request);

            if (response.IsSuccessStatusCode)
            {
                log.LogInformation($"URL ${url} esta OK");
            }
            else
            {
                log.LogInformation($"URL ${url} não esta OK");
            }
        }

        [FunctionName("HttpCheck")]
        public static void Run([TimerTrigger("0 */5 * * * *")]TimerInfo myTimer, ILogger log)
        {
            var urls = new[]{"https://www.sipmann.com", "https://www.canezecanez.com.br"};
		
            // Start every request and wait for them all to complete
            Task.WaitAll(urls.Select(url => GetTask(url, log)).ToArray());
            log.LogInformation($"Finalizou a fila");
        }
    }
}
```

Now you can enhance the function and maybe send some alerts like a Telegram message when one of your sites went down.