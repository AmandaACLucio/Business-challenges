/* Criando tabela */

CREATE TABLE [aluno]
( 
	[Cd_Aluno]          integer  IDENTITY  NOT NULL ,
	[Nu_DRE]			integer  NULL,
	[Nm_Curso]          char(180)  NULL,
	[Nm_Nome]			char(180)  NULL,
	[Nm_Genero]			char(180)  NULL,
	[Dt_Nascimento]		date  NULL,
	[Al_Altura]			float NULL,
	[Ps_Peso]			float NULL,
	[Nu_CRA]			float NULL,
	[Nu_Créditos]		integer NULL,
	[Vl_Renda]			float NULL
)
go

/* Incluindo alunos */
INSERT INTO [dbo].[aluno] 
(
	[Nu_DRE],
	[Nm_Curso],
	[Nm_Nome],
	[Nm_Genero],
	[Dt_Nascimento],
	[Al_Altura],
	[Ps_Peso],
	[Nu_CRA],
	[Nu_Créditos],		
	[Vl_Renda])
	
VALUES (
	11533, /* DRE */
	'Engenharia', /*Curso */
	'Amanda Lucio', /* Nome */
	'Feminino', /* Genero */
	'2020-06-25', /* Data de nascimento */
	1.6,/* altura */
	60, /* peso */
	10, /* CRA */
	28, /* Creditos Obtidos */
	1	/* Renda */
)

/* Deletando */
DELETE FROM aluno WHERE Nu_DRE='11533';

/* Quantos alunos são mulheres */
SELECT Count(Cd_Aluno) FROM aluno WHERE Nm_Genero='Feminino';

/* Média Curso de Engenharia */
SELECT AVG(Nu_CRA) FROM aluno WHERE Nm_Curso='Engenharia';

/* Desvio Padrão */
SELECT STDEVP(Vl_Renda) FROM aluno;  
GO  