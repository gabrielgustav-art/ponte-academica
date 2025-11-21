import sqlite3
import os

NOME_BANCO = "tabela.db"

# Remove banco antigo para recriar do zero
if os.path.exists(NOME_BANCO):
    os.remove(NOME_BANCO)
    print(f"Banco de dados '{NOME_BANCO}' antigo removido para recriação.")

# Cria nova conexão
conn = sqlite3.connect(NOME_BANCO)
cursor = conn.cursor()

try:
    # === TABELA ALUNO =====================================
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

    # === TABELA ORGANIZAÇÃO ================================
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

    # === TABELA PROJETO ====================================
    sql_projeto = """
    CREATE TABLE Projeto (
        ID_PROJETO          INTEGER PRIMARY KEY,
        TITULO              TEXT NOT NULL,
        DESCRICAO           TEXT NOT NULL,
        CNPJ_ORG            INTEGER NOT NULL,
        DATA_CRIACAO        TEXT NOT NULL,
        ULTIMA_ATUALIZACAO  TEXT,

        FOREIGN KEY(CNPJ_ORG) REFERENCES Organizacao(CNPJ_ORG)
    );
    """
    cursor.execute(sql_projeto)
    print("Tabela 'Projeto' criada com sucesso!")

    # === TABELA CANDIDATURA ================================
    sql_candidatura = """
    CREATE TABLE Candidatura (
        ID_CANDIDATURA     INTEGER PRIMARY KEY,
        ID_PROJETO         INTEGER NOT NULL,
        RGM_ALUNO          INTEGER NOT NULL,
        DATA_CANDIDATURA   TEXT NOT NULL,

        FOREIGN KEY(ID_PROJETO) REFERENCES Projeto(ID_PROJETO),
        FOREIGN KEY(RGM_ALUNO) REFERENCES Aluno(RGM_ALUNO),

        UNIQUE(ID_PROJETO, RGM_ALUNO)
    );
    """
    cursor.execute(sql_candidatura)
    print("Tabela 'Candidatura' criada com sucesso!")

    # === TABELA DE MENSAGENS (CORRIGIDA) ===================
    # Agora inclui ID_REMETENTE e usa MENSAGEM em vez de TEXTO
    sql_mensagem = """
    CREATE TABLE Mensagem (
        ID_MENSAGEM   INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_PROJETO    INTEGER NOT NULL,
        REMETENTE     TEXT NOT NULL,      -- 'aluno' ou 'org'
        ID_REMETENTE  TEXT NOT NULL,      -- RGM ou CNPJ
        MENSAGEM      TEXT NOT NULL,
        DATA_ENVIO    TEXT NOT NULL,

        FOREIGN KEY(ID_PROJETO) REFERENCES Projeto(ID_PROJETO)
    );
    """
    cursor.execute(sql_mensagem)
    print("Tabela 'Mensagem' recriada com a estrutura correta!")

except sqlite3.Error as e:
    print(f"Ocorreu um erro ao criar as tabelas: {e}")

finally:
    conn.commit()
    conn.close()
    print("Banco de dados configurado e conexão fechada.")