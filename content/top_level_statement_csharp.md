Title: Top Level Statement in C# 9
Date: 2020-07-29 19:00
Tags: C#, Dotnet Core, DotNet, .net
Category: .NET
Slug: top_level_statement_csharp_9
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Image: /images/csharp_toplevel.png
Image_width: 1365
Image_height: 768
Description: Top Level Statement in C# 9, a new feature

Hey folks, I'm coming along to tell you a few things about the new feature of C# 9. Every time you want to start a new project, you always have the same Main File, with the same structure. At the next version of C# (version 9), we'll have a new feature called `Top Level Statement`. With that, we'll be able to code our app without any namespace/class/public void static main structure. Take a look at the code below.


```c#
using System;

Console.WriteLine("Hello World!");
```

It looks pretty simple, but with this, you can play around with your code, and even code a simple/tiny Web API. To start playing with the new features, firstly download the [.net 5 SDK](https://dotnet.microsoft.com/download/dotnet/5.0) and change your `.csproj` file to target the .net 5 and language preview like bellow.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net5.0</TargetFramework>
    <LangVersion>preview</LangVersion>
  </PropertyGroup>
</Project>
```

And you're ready to play with the awesome features available in the preview. Let's code a way to get the image of the day from NASA API and print the Picture of the Day. No awesome code here, it's really a way to show how simple a simple call could be. After here, why not save the image in a file? Maybe send the file over telegram?

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

That's it for today folks. Keep an eye open for the awesome features C# 9 will bring to us, there's plenty more features already available.