Title: Removing user from SQL Server database
Date: 2019-09-06 07:00
Tags: SQLServer, User, database principal
Category: SQL Server
Slug: removing-user-from-sql-server-database
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com

Your customer urge you to drop a user from the MsSQL Server database, but you stuck with the following related error:

```mssql
Error: 15138 The database principal owns a schema in the database, and cannot be dropped.
```

If you don't have access to the SSMS to see which schema or objects the user owns, the following SQL should do the job.

```mssql
USE [DATABASENAME]
GO
 -- get's the user id
select DATABASE_PRINCIPAL_ID('username')

select so.name Objeto, su.name Owner
from sys.schemas so
inner join sysusers su on so.principal_id = su.uid
where su.name = 'username'

select so.name Objeto, su.name Owner, so.xtype Tipo
from sys.sysobjects so
inner join sysusers su on so.uid = su.uid
where su.name = 'username'
```

Once you have the objects/schemas owned by the user, you can change them with the following SQL (schema change sample):

```mssql
USE [DATABASENAME]
GO
ALTER AUTHORIZATION ON SCHEMA::[db_datareader] TO [dbo] -- new owner username
ALTER AUTHORIZATION ON SCHEMA::[db_datawriter] TO [dbo]
GO
```

Then you're ready to drop the user `DROP USER [username]`
