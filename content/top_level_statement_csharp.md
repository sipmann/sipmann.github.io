Title: Top Level Statement in C# 9
Date: 2020-07-29 19:00
Tags: C#, Dotnet Core, DotNetm .net
Category: .NET
Slug: top_level_statement_csharp_9
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Image: /images/csharp_toplevel.png
Description: 
Draft: true

Hey folks, I'm acomming along to tell you a few things about the new feature of C# 9. Every time you wan't to start a new project, you allways have the same Main File, with the same structure. At the next version of C# (version 9) we'll have a new feature called `Top Level Statement`. With that, we'll be able to code our app without any namespace/class/public void static main structure. Take a look at the code bellow.


```c#
using System;

Console.WriteLine("Hello World!");
```


It looks pretty simple, but with this, you can play arround with your code, and even code a simple/tiny Web Api. 