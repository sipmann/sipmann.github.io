Title: Blocking a user on SQL Server based on a schedule
Date: 2019-09-06 07:00
Modified: 2020-11-04 18:40
Tags: SQLServer, User, Time Schedule blocking
Category: SQL Server
Slug: blocking-user-on-sql-server-based-on-schedule
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: How to block a SQL Server user based on a schedule using the SQL Server Agent and a Table that holds the user and the blocking time.
Lang: en
Status: Draft

Ok, some time ago, I've posted about how you can set limits to connections on SQL Server using the [Resource Governor](https://www.sipmann.com/limiting-connection-resources-sql-server.html#.X6Cz8IhKhPY). But what if you can't use it? You always can blog logins using a login trigger, but I don't like the idea of having selects running on every login. So I came across with a solution using a stored procedure, a table and the Agent.

The main idea is, store the time that a user must be blocked and using the Agent, disable or enable the user. Bellow you can see the table (the table is in Portuguese, but I have a few comment blocks to help you).

```mssql
CREATE TABLE dbo.HorariosBloqueio (
	Id INT NOT NULL,
	LoginName NVARCHAR(100) NOT NULL,
	HrInicio TIME NOT NULL, /* Startint block time */
	HrTermino TIME NOT NULL, /* Ending block time */
	Bloqueado INT DEFAULT 0, /* 0 = unblocked, 1 = blocked */
	PRIMARY KEY (Id)
);
GO

/* Don't block the SA user, precautions, you know */
ALTER TABLE dbo.HorariosBloqueio
	ADD CONSTRAINT chk_users CHECK (LoginName not in ('sa'));

ALTER TABLE dbo.HorariosBloqueio
	ADD CONSTRAINT chk_hora_final_maior CHECK (HrTermino > HrInicio);

ALTER TABLE dbo.HorariosBloqueio
	ADD CONSTRAINT chk_status_bloqueio CHECK (Bloqueado in (0, 1));

CREATE SEQUENCE dbo.seq_HorariosBloqueio START WITH 1 INCREMENT BY 1;
GO
```

After creating the table, let's check the procedure that will handle the enabling/disabling the users. Be aware that on the procedure, I've set the database name where the table was stored, you can change it replacing the `DBATOOLS` text to the database name where you created the table.

```mssql
IF OBJECT_ID('dbo.sp_ValidarLogin') IS NULL
  EXEC ('CREATE PROCEDURE dbo.sp_ValidarLogin AS RETURN 0;');
GO

CREATE OR ALTER PROC dbo.sp_ValidarLogin
AS BEGIN
	DECLARE @LoginName AS NVARCHAR(100);
	DECLARE @Momento AS TIME;
	SET @Momento = CAST(GETDATE() AS TIME);
	
    /* Block the ones that aren't blocked already and maches the time */
	DECLARE block_cursor CURSOR
		FOR SELECT LoginName FROM [DBATOOLS].[dbo].[HorariosBloqueio] WHERE Bloqueado = 0 AND HrInicio <= @Momento AND HrTermino >= @Momento
	OPEN block_cursor;

	FETCH NEXT FROM block_cursor INTO @LoginName

	WHILE @@FETCH_STATUS = 0
	BEGIN
		exec ('ALTER LOGIN ' + @LoginName + ' DISABLE;');

		print 'Bloqued usuario ' + @LoginName;

		FETCH NEXT FROM block_cursor INTO @LoginName
	END;

	CLOSE block_cursor;
	DEALLOCATE block_cursor;

	UPDATE [DBATOOLS].[dbo].[HorariosBloqueio] SET Bloqueado = 1 WHERE HrInicio <= @Momento AND HrTermino >= @Momento

	
	/* Enable up who was blocked */
	DECLARE unblock_cursor CURSOR
		FOR SELECT LoginName FROM [DBATOOLS].[dbo].[HorariosBloqueio] WHERE Bloqueado = 1 AND (HrInicio > @Momento OR HrTermino < @Momento)
	OPEN unblock_cursor ;

	FETCH NEXT FROM unblock_cursor  INTO @LoginName

	WHILE @@FETCH_STATUS = 0
	BEGIN
		exec ('ALTER LOGIN ' + @LoginName +' ENABLE;');

		print 'Unbloqued usuario ' + @LoginName;

		FETCH NEXT FROM unblock_cursor  INTO @LoginName
	END;

	CLOSE unblock_cursor;
	DEALLOCATE unblock_cursor;

	UPDATE [DBATOOLS].[dbo].[HorariosBloqueio] SET Bloqueado = 0 WHERE Bloqueado = 1 AND (HrInicio > @Momento OR HrTermino < @Momento)
END;
```

Ok, so now all you have to do, is schedule a job to run that stored procedure from minute to minute. Again, the main idea is tell the procedure when a user must be blocked and when it'll be unblocked. 

```mssql
    
    /* Will block the user protheus from 10 AM till 15 PM */
    INSERT INTO dbo.HorariosBloqueio (Id, LoginName, HrInicio, HrTermino) VALUES (NEXT VALUE FOR seq_HorariosBloqueio, 'protheus', '10:00:00', '15:00:00');
    
```