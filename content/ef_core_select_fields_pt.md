Title: Como definir as colunas no select utilizando Entity Framework
Date: 2020-10-28 19:00
Tags: DotNet, DotNet Core, Entity Framework, EF Core, Specify columns
Category: .NET 
Slug: select_specific_fields_with_efcore
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Lang: pt
Description: Você sabe quantos dados você está pegando com o seu select no EF? Aprenda como especificar quais campos você vai selecionar utilizando Entity Framework Core.
Image: /images/efcore_select_fields.png

Então, você utiliza Entity Framework Core e geralmente faz o seu selecto da seguinte forma, talvez você está retornando muitos dados.

```c#
var products = Products
	.Where(p => p.UnitsInStock > 0)
	.OrderBy(p => p.ProductName)
	.ToList()
```

Rodando a query acima, em uma base de testes você obtem o seguinte resultado, veja quantas colunas estão retornando da sua base de dados.

![Print com todas as colunas](/images/ef_core_allcolumns.png)

No meu caso, eu só pretendo ter de volta as colunas Title, PublishedData e uma pequena descrição. Então para selecionar apenas estes campos, nós temos algumas opções. Na primeira, nós vamos definir os campos e retornar um objeto do tipo Dynamic. A segunda forma, é dar ao .NET o objeto a ser retornado, pode ser por exêmplo um DTO.

```c#
var products = Products

	.Select(p => new {p.ProductID, p.ProductName, p.UnitsInStock, p.UnitPrice})
    //.Select(p => new ProductDTO {p.ProductID, p.ProductName, p.UnitsInStock, p.UnitPrice})

	.Where(p => p.UnitsInStock > 0)
	.OrderBy(p => p.ProductName)
	.ToList()
```

![Print com menos colunas e também menor quantidade de dados](/images/ef_core_less_columns.png)
