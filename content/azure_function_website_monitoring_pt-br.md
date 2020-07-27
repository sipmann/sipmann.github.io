Title: Monitorando a disponibilidade de um Website com Azure Functions
Date: 2020-06-22 19:00
Tags: Azure, Azure Devops, C#, Dotnet Core, DotNet, Monitor Website
Category: Azure
Slug: monitoring-website-heath-with-azure-functions
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Image: /images/azure_monitoring.png
Description: Monitorando a disponibilidade de um website com Azure Functions e CSharp.
Lang: pt

Algumas vezes você se depara com a necessidade de monitorar a disponibilidade de um website ou mudanças em seu conteúdo. É claro que temos diversas opções disponíveis no mercado, mas para fins de curiosidade, vamos programar o nosso próprio e ver o que podemos fazer. Primeiramente, tudo que você ver aqui, você pode utilizar o [tier gratuito](https://azure.microsoft.com/free/) da Azure.

A ideia principal da nossa aplicação vai ser monitorar a disponibilidade do website (status code). Para criar um projeto de Azure Function, siga os passos abaixo.

![Passos para criar um projeto Azure Functions](/images/azure_functions.gif)

Depois de criar o projeto, você vai ter alguns arquivos. Abra o arquivo principal (`HttpCheck.cs` no meu caso) e começe a programar. O arquivo principal terá uma função chamada `Run` e você pode progamar nela o seu request. Eu criei um método `async` para fazer as requisições e printar a saída diretamente no console. O código completo pode ser visto abaixo.

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
            // URL a verificar a saúde
            var urls = new[]{"https://www.sipmann.com", "https://www.canezecanez.com.br"};
		
            // Starta cada request e aguarda todos de uma vez só
            Task.WaitAll(urls.Select(url => GetTask(url, log)).ToArray());
            log.LogInformation($"Finalizou a fila");
        }
    }
}
```

Agora você pode melhorar a função e talvez enviar alguns alertas. Como por exêmplo mensagens no Telegram quando um dos sites ficar off (status code 404).