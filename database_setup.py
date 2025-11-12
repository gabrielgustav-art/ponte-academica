import sqlite3
import os

NOME_BANCO = "tabela.db"

if os.path.exists(NOME_BANCO):
    os.remove(NOME_BANCO)
    print(f"Banco de dados '{NOME_BANCO}' antigo removido para recriação.")

conn = sqlite3.connect(NOME_BANCO)
cursor = conn.cursor()

try:
    # --- PLANTA 1: Aluno (Sem mudanças) ---
    sql_aluno = """
    CREATE TABLE Aluno (
        RGM_ALUNO     INTEGER PRIMARY KEY,
        NOME_ALUNO    TEXT NOT NULL,
        SENHA         TEXT NOT NULL,
        DATA_CADASTRO TEXT NOT NULL
    );
    """
    cursor.execute(sql_aluno)
    print("Tabela 'Aluno' criada com sucesso!")

    # --- PLANTA 2: Organizacao (Sem mudanças) ---
    sql_organizacao = """
    CREATE TABLE Organizacao (
        CNPJ_ORG      INTEGER PRIMARY KEY,
        NOME_ORG      TEXT NOT NULL,
        SENHA         TEXT NOT NULL,
        DATA_CADASTRO TEXT NOT NULL
    );
    """
    cursor.execute(sql_organizacao)
    print("Tabela 'Organizacao' criada com sucesso!")

    # --- PLANTA 3: Projeto (Atualizada) ---
    # A coluna RGM_ALUNO foi REMOVIDA daqui
    sql_projeto = """
    CREATE TABLE Projeto (
        ID_PROJETO    INTEGER PRIMARY KEY,
        TITULO        TEXT NOT NULL,
        DESCRICAO     TEXT NOT NULL,
        CNPJ_ORG      INTEGER NOT NULL,
        DATA_CRIACAO  TEXT NOT NULL,

        FOREIGN KEY(CNPJ_ORG) REFERENCES Organizacao(CNPJ_ORG)
    );
    """
    cursor.execute(sql_projeto)
    print("Tabela 'Projeto' (sem RGM) criada com sucesso!")

    # --- PLANTA 4: Candidatura (NOVA TABELA) ---
    # Esta tabela faz a ligação N:M entre Alunos e Projetos
    sql_candidatura = """
    CREATE TABLE Candidatura (
        ID_CANDIDATURA   INTEGER PRIMARY KEY,
        ID_PROJETO       INTEGER NOT NULL,
        RGM_ALUNO        INTEGER NOT NULL,
        DATA_CANDIDATURA TEXT NOT NULL,
        
        FOREIGN KEY(ID_PROJETO) REFERENCES Projeto(ID_PROJETO) ON DELETE CASCADE,
        FOREIGN KEY(RGM_ALUNO) REFERENCES Aluno(RGM_ALUNO) ON DELETE CASCADE
    );
    """
    cursor.execute(sql_candidatura)
    print("Tabela 'Candidatura' (N:M) criada com sucesso!")


except sqlite3.Error as e:
    print(f"Ocorreu um erro ao criar as tabelas: {e}")

finally:
    conn.commit()
    conn.close()
    print("Banco de dados configurado e conexão fechada.")