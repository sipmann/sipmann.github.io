Title: Removendo um usuário de uma base SQL Server
Date: 2019-09-06 07:00
Modified: 2020-10-21 18:40
Tags: SQLServer, User, The database principal owns a schema
Category: SQL Server
Slug: removing-user-from-sql-server-database
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: Você esta tentando remover um usuário do banco, mas ele é dono de um schema, primeiro verifique quais schemas ele controla, então escolha o novo dono para os mesmos e rode o ALTER AUTHORIZATION
Lang: pt

O seu cliente lhe pede com urgência para *dropar* um usuário da sua base MsSQL Server, mas você trava com o seguinte aviso de erro:

```mssql
Error: 15138 The database principal owns a schema in the database, and cannot be dropped.
```

Se você não possui (ou no momento não consegue acesso) ao SSMS (SQL Server Management Studio) para verificar quais schemas ou objetos o usuário é "dono", a seguinte SQL vai resolver o problema.

```mssql
USE [DATABASENAME]
GO

select so.name Objeto, su.name Owner
from sys.schemas so
inner join sysusers su on so.principal_id = su.uid
where su.name = 'username'

select so.name Objeto, su.name Owner, so.xtype Tipo
from sys.sysobjects so
inner join sysusers su on so.uid = su.uid
where su.name = 'username'
```

Assim que você tiver os objetos/schemas que o usuário é dono, você pode alterar os mesmos com a seguinte SQL (exemplo de troca de schema):

```mssql
USE [DATABASENAME]
GO
ALTER AUTHORIZATION ON SCHEMA::[db_datareader] TO [dbo] -- username do novo dono
ALTER AUTHORIZATION ON SCHEMA::[db_datawriter] TO [dbo]
GO
```

Então, você pode dropar o usuário `DROP USER [username]`.
