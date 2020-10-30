Title: How to set columns on select using Entity Framework
Date: 2020-10-28 19:00
Tags: DotNet, DotNet Core, Entity Framework, EF Core, Specify columns
Category: .NET 
Slug: select_specific_fields_with_efcore
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: en
Description: Did you know how much data you get back with your EF select? Learn how to specify which fields you would get back.
Image: /images/efcore_select_fields.png

So, you use Entity Framework Core, and you usually code your selects like the following, maybe you are getting too much data.

```c#
var products = Products
	.Where(p => p.UnitsInStock > 0)
	.OrderBy(p => p.ProductName)
	.ToList()
```

Running the query above, on my table, you'll get the following output, take a look at how many columns you are getting back from your database.

![Screenshot with every single column](/images/ef_core_allcolumns.png)

In my case, I only care about the Title, PublishedData, and a small description. So to get back only these fields, we have a few options. In the first one, we'll set the fields and return them as a dynamic object, the second one, is to give the .NET a class to use. 

```c#
var products = Products

	.Select(p => new {p.ProductID, p.ProductName, p.UnitsInStock, p.UnitPrice})
    //.Select(p => new ProductDTO {p.ProductID, p.ProductName, p.UnitsInStock, p.UnitPrice})

	.Where(p => p.UnitsInStock > 0)
	.OrderBy(p => p.ProductName)
	.ToList()
```

![Screenshot with fewer columns and also fewer data size](/images/ef_core_less_columns.png)
