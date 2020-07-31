Title: Top Level Statement no C# 9
Date: 2020-07-29 19:00
Tags: C#, Dotnet Core, DotNetm .net
Category: .NET
Slug: top_level_statement_csharp_9
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Image: /images/csharp_toplevel.png
Description: Top Level Statement no C# 9, uma nova feature

Olá pessoal, venho hoje falar sobre uma novidade que estará disponível na versão 9 do C#. Toda vez que você deseja criar um novo projeto, você sempre tem o mesmo arquivo Main, com a mesma estrutura. Na próxima versão do C# (versão 9), nós teremos uma nova funcionalidade chamada `Top Level Statement`. Com isto, poderemos programar a nossa aplicação sem toda aquela estrutura de `namespace/class/public void static main`. Veja o código abaixo.


```c#
using System;

Console.WriteLine("Hello World!");
```

Parece muito simples, não é? Com isto, você pode brincar com seu código e até mesmo programar uma pequena WEB API. Para começar a brincar com estas novas *features*, primeiramente faça o download do preview do [.net 5 SDK](https://dotnet.microsoft.com/download/dotnet/5.0) e modifique o seu arquivo `.csproj` para apontar o framework para `.net5.0` e a versão de preview da linguagem. Abaixo como uma aplicação de console deve ficar.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net5.0</TargetFramework>
    <LangVersion>preview</LangVersion>
  </PropertyGroup>
</Project>
```

E assim você está pronto para brincar com as novas funcionalidades que estão disponíveis na versão preview. Vamos programar uma aplicação simples que faz uma requisição na API da NASA e printe a Imagem do Dia no console. Não é nenhum código mirabolante, é simplesmente para exemplificar o quão simples uma simples chamada de API pode ser. Feito isto, porque não salvar a imagem como um arquivo? Ou então enviar essa imagem via telegram?

```c#
using System;
using System.Net.Http;
using System.Text.Json;

var API = "https://api.nasa.gov/planetary/apod?hd=true&api_key=DEMO_KEY";
var cli = new HttpClient();

var response = await cli.GetAsync(API);
var data = JsonSerializer.Deserialize<NasaApi>(await response.Content.ReadAsStringAsync());

Console.WriteLine(data.Url);
```

Por hoje é isso. Fique de olho nas novas features que o C# 9 vai nos trazer. Já temos várias disponíveis hoje para testar, esta é apenas uma delas.