import sqlite3

# 1. Conecta ao "armazém" (o .db)
conn = sqlite3.connect('tabela.db')
cursor = conn.cursor()

try:
    # --- PLANTA 1: Aluno ---
    sql_aluno = """
    CREATE TABLE Aluno (
    RGM_ALUNO   INTEGER PRIMARY KEY,
    NOME_ALUNO  TEXT NOT NULL,
    SENHA       TEXT NOT NULL
    );
    """
    cursor.execute(sql_aluno)
    print("Tabela 'Aluno' criada com sucesso!")

    # --- PLANTA 2: Organizacao ---
    sql_organizacao = """
    CREATE TABLE IF NOT EXISTS Organizacao (
        CNPJ_ORG    INTEGER PRIMARY KEY,
        NOME_ORG    TEXT NOT NULL,
        SENHA       TEXT NOT NULL
    );
    """
    cursor.execute(sql_organizacao)
    print("Tabela 'Organizacao' criada com sucesso!")

    # --- PLANTA 3: Projeto (A principal) ---
    sql_projeto = """
    CREATE TABLE IF NOT EXISTS Projeto (
        ID_PROJETO INTEGER PRIMARY KEY,
        TITULO     TEXT NOT NULL,
        DESCRICAO  TEXT NOT NULL,
        RGM_ALUNO  INTEGER,
        CNPJ_ORG   INTEGER NOT NULL,

        FOREIGN KEY(RGM_ALUNO) REFERENCES Aluno(RGM_ALUNO),
        FOREIGN KEY(CNPJ_ORG) REFERENCES Organizacao(CNPJ_ORG)
    );
    """
    cursor.execute(sql_projeto)
    print("Tabela 'Projeto' criada com sucesso!")

except sqlite3.Error as e:
    # Se qualquer um dos comandos falhar, veremos o erro
    print(f"Ocorreu um erro ao criar as tabelas: {e}")

finally:
    # 4. Salva o trabalho e fecha a conexão
    conn.commit()
    conn.close()
    print("Banco de dados configurado e conexão fechada.")