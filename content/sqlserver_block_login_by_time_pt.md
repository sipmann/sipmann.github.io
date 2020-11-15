Title: Bloqueando um usuário do SQL Server baseado em uma tabela de horários
Date: 2019-11-14 07:00
Tags: SQLServer, User, Time Schedule blocking
Category: SQL Server
Slug: blocking-user-on-sql-server-based-on-schedule
Author: Maurício Camargo Sipmann
Email: sipmann@gmail.com
Description: Como bloquear um usuáriodo SQL Server baseando-se em uma tabela de horários utilizando o SQL Server Agent.
Lang: pt

Ok, algum tempo atrás, eu postei sobre como você pode impor limites às conexões do SQL Server utilizando o [Resource Governor](https://www.sipmann.com/limiting-connection-resources-sql-server.html#.X6Cz8IhKhPY). Mas, e se você não pode utilizar ele? Você sempre pode bloquear logins usando uma trigger, mas eu não gosto da ideia de ter um select rodando a cada login. Então, eu cheguei a esta solução, utilizando uma stored procedure, uma tabela e o Agent.

A ideia principal é armazenar o horário em que um usuário deve ser bloqueado pelo Agent. Abaixo você pode ver a criação da tabela:

```mssql
CREATE TABLE dbo.HorariosBloqueio (
	Id INT NOT NULL,
	LoginName NVARCHAR(100) NOT NULL,
	HrInicio TIME NOT NULL, /* horário de inicio do bloqueio */
	HrTermino TIME NOT NULL, /*horário de termino */
	Bloqueado INT DEFAULT 0, /* 0 = desbloqueado, 1 = bloqueado */
	PRIMARY KEY (Id)
);
GO

/* regra para Não bloquear o usuário SA */
ALTER TABLE dbo.HorariosBloqueio
	ADD CONSTRAINT chk_users CHECK (LoginName not in ('sa'));

ALTER TABLE dbo.HorariosBloqueio
	ADD CONSTRAINT chk_hora_final_maior CHECK (HrTermino > HrInicio);

ALTER TABLE dbo.HorariosBloqueio
	ADD CONSTRAINT chk_status_bloqueio CHECK (Bloqueado in (0, 1));

CREATE SEQUENCE dbo.seq_HorariosBloqueio START WITH 1 INCREMENT BY 1;
GO
```

Depois de criar a tabela, vamos verificar a procedure que vai fazer todo o trabalho de habilitar/desabilitar os usuários. Fique ciente que, nesta procedure, eu defini o nome do banco onde a tabela está armazenada. Você pode substituir o nome `DBATOOLS` pelo o nome da sua base.

```mssql
IF OBJECT_ID('dbo.sp_ValidarLogin') IS NULL
  EXEC ('CREATE PROCEDURE dbo.sp_ValidarLogin AS RETURN 0;');
GO

CREATE OR ALTER PROC dbo.sp_ValidarLogin
AS BEGIN
	DECLARE @LoginName AS NVARCHAR(100);
	DECLARE @Momento AS TIME;
	SET @Momento = CAST(GETDATE() AS TIME);
	
	/* Bloqueia os que ainda não estiverem bloqueados de acordo com a hora atual */
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

	
	/* Libera quem estava bloqueado */
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

Certo, então agora tudo que temos que fazer é definir o job no Agent para rodar a procedure de minuto em minuto. Novamente, a ideia principal é chamar a procedure quando um usuário deve ser bloqueado e quando deve ser desbloqueado.

```mssql

	-- Vai bloquear o usuário protheus das 10 AM até 15 PM
	INSERT INTO dbo.HorariosBloqueio (Id, LoginName, HrInicio, HrTermino) VALUES (NEXT VALUE FOR seq_HorariosBloqueio, 'protheus', '10:00:00', '15:00:00');

```