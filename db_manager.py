import sqlite3
import os
from datetime import datetime

NOME_BANCO = "tabela.db"

def get_conn():
    conn = sqlite3.connect(NOME_BANCO)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria as tabelas caso o banco ainda não exista."""
    first_time = not os.path.exists(NOME_BANCO)
    conn = get_conn()
    cur = conn.cursor()

    # Cria tabelas (IF NOT EXISTS) — não apaga DB existente
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Aluno (
        RGM_ALUNO     INTEGER PRIMARY KEY,
        NOME_ALUNO    TEXT NOT NULL,
        SENHA         TEXT NOT NULL,
        DATA_CADASTRO TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Organizacao (
        CNPJ_ORG      INTEGER PRIMARY KEY,
        NOME_ORG      TEXT NOT NULL,
        SENHA         TEXT NOT NULL,
        DATA_CADASTRO TEXT NOT NULL
    );
    """)

    # Agora com ULTIMA_ATUALIZACAO
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Projeto (
        ID_PROJETO          INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO              TEXT NOT NULL,
        DESCRICAO           TEXT NOT NULL,
        CNPJ_ORG            INTEGER NOT NULL,
        DATA_CRIACAO        TEXT NOT NULL,
        ULTIMA_ATUALIZACAO  TEXT NOT NULL,
        FOREIGN KEY(CNPJ_ORG) REFERENCES Organizacao(CNPJ_ORG)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Candidatura (
        ID_CANDIDATURA     INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_PROJETO         INTEGER NOT NULL,
        RGM_ALUNO          INTEGER NOT NULL,
        DATA_CANDIDATURA   TEXT NOT NULL,
        FOREIGN KEY(ID_PROJETO) REFERENCES Projeto(ID_PROJETO),
        FOREIGN KEY(RGM_ALUNO) REFERENCES Aluno(RGM_ALUNO),
        UNIQUE(ID_PROJETO, RGM_ALUNO)
    );
    """)

    # Tabela para mensagens do chat interno
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Mensagem (
        ID_MENSAGEM     INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_PROJETO      INTEGER NOT NULL,
        REMETENTE       TEXT NOT NULL,  -- 'aluno' ou 'org'
        ID_REMETENTE    TEXT NOT NULL,  -- RGM ou CNPJ (string)
        MENSAGEM        TEXT NOT NULL,
        DATA_ENVIO      TEXT NOT NULL,
        FOREIGN KEY(ID_PROJETO) REFERENCES Projeto(ID_PROJETO)
    );
    """)

    conn.commit()
    conn.close()
    if first_time:
        print("Banco criado e tabelas inicializadas.")
    else:
        print("Banco encontrado — verificação de tabelas concluída.")

# --------------------------
# Funções de acesso usadas pelo app
# --------------------------

def login_aluno_db(rgm, senha):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT NOME_ALUNO FROM Aluno WHERE RGM_ALUNO=? AND SENHA=?", (rgm, senha))
    row = cur.fetchone()
    conn.close()
    return row["NOME_ALUNO"] if row else None

def login_organizacao_db(cnpj, senha):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT NOME_ORG FROM Organizacao WHERE CNPJ_ORG=? AND SENHA=?", (cnpj, senha))
    row = cur.fetchone()
    conn.close()
    return row["NOME_ORG"] if row else None

def cadastrar_aluno_db(rgm, nome, senha, data_cadastro):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO Aluno (RGM_ALUNO, NOME_ALUNO, SENHA, DATA_CADASTRO) VALUES (?, ?, ?, ?)",
                    (rgm, nome, senha, data_cadastro))
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def cadastrar_organizacao_db(cnpj, nome, senha, data_cadastro):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO Organizacao (CNPJ_ORG, NOME_ORG, SENHA, DATA_CADASTRO) VALUES (?, ?, ?, ?)",
                    (cnpj, nome, senha, data_cadastro))
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def cadastrar_projeto_db(titulo, descricao, cnpj_org, data_criacao, ultima_atualizacao):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Projeto (TITULO, DESCRICAO, CNPJ_ORG, DATA_CRIACAO, ULTIMA_ATUALIZACAO)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, descricao, cnpj_org, data_criacao, ultima_atualizacao))
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

def listar_projetos_org_db(cnpj_org):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT ID_PROJETO, TITULO, (SELECT COUNT(*) FROM Candidatura WHERE ID_PROJETO=Projeto.ID_PROJETO) AS CANDIDATOS, DATA_CRIACAO FROM Projeto WHERE CNPJ_ORG=? ORDER BY DATA_CRIACAO DESC", (cnpj_org,))
        rows = cur.fetchall()
        resultados = [(r["ID_PROJETO"], r["TITULO"], r["CANDIDATOS"], r["DATA_CRIACAO"]) for r in rows]
        conn.close()
        return resultados, None
    except Exception as e:
        return None, str(e)

def listar_projetos_disponiveis_db(rgm_aluno):
    try:
        conn = get_conn()
        cur = conn.cursor()
        # lista todos os projetos nos quais o aluno ainda não se candidatou
        cur.execute("""
            SELECT p.ID_PROJETO, p.TITULO, o.NOME_ORG AS ORGANIZACAO, p.DATA_CRIACAO
            FROM Projeto p
            JOIN Organizacao o ON p.CNPJ_ORG = o.CNPJ_ORG
            WHERE p.ID_PROJETO NOT IN (SELECT ID_PROJETO FROM Candidatura WHERE RGM_ALUNO=?)
            ORDER BY p.DATA_CRIACAO DESC
        """, (rgm_aluno,))
        rows = cur.fetchall()
        resultados = [(r["ID_PROJETO"], r["TITULO"], r["ORGANIZACAO"], r["DATA_CRIACAO"]) for r in rows]
        conn.close()
        return resultados, None
    except Exception as e:
        return None, str(e)

def get_projeto_detalhes_db(id_projeto, cnpj_org):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT TITULO, DESCRICAO, DATA_CRIACAO, ULTIMA_ATUALIZACAO FROM Projeto WHERE ID_PROJETO=? AND CNPJ_ORG=?", (id_projeto, cnpj_org))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None, None
        return (row["TITULO"], row["DESCRICAO"], row["DATA_CRIACAO"], row["ULTIMA_ATUALIZACAO"]), None
    except Exception as e:
        return None, str(e)

def get_projeto_detalhes_publico_db(id_projeto):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.TITULO, p.DESCRICAO, o.NOME_ORG, p.DATA_CRIACAO, p.ULTIMA_ATUALIZACAO
            FROM Projeto p
            JOIN Organizacao o ON p.CNPJ_ORG=o.CNPJ_ORG
            WHERE p.ID_PROJETO=?
        """, (id_projeto,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None, None
        return (row["TITULO"], row["DESCRICAO"], row["NOME_ORG"], row["DATA_CRIACAO"], row["ULTIMA_ATUALIZACAO"]), None
    except Exception as e:
        return None, str(e)

def listar_candidatos_db(id_projeto):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.RGM_ALUNO, a.NOME_ALUNO, c.DATA_CANDIDATURA
            FROM Candidatura c
            JOIN Aluno a ON c.RGM_ALUNO=a.RGM_ALUNO
            WHERE c.ID_PROJETO=?
        """, (id_projeto,))
        rows = cur.fetchall()
        resultados = [(r["RGM_ALUNO"], r["NOME_ALUNO"], r["DATA_CANDIDATURA"]) for r in rows]
        conn.close()
        return resultados, None
    except Exception as e:
        return None, str(e)

def candidatar_a_projeto_db(id_projeto, rgm_aluno, data_candidatura):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO Candidatura (ID_PROJETO, RGM_ALUNO, DATA_CANDIDATURA) VALUES (?, ?, ?)",
                    (id_projeto, rgm_aluno, data_candidatura))
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, "Já existe candidatura para este projeto." if "UNIQUE" in str(e).upper() else str(e)
    except Exception as e:
        return False, str(e)

def ver_minhas_candidaturas_db(rgm_aluno):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.ID_PROJETO, p.TITULO, o.NOME_ORG, c.DATA_CANDIDATURA
            FROM Candidatura c
            JOIN Projeto p ON c.ID_PROJETO = p.ID_PROJETO
            JOIN Organizacao o ON p.CNPJ_ORG = o.CNPJ_ORG
            WHERE c.RGM_ALUNO=?
            ORDER BY c.DATA_CANDIDATURA DESC
        """, (rgm_aluno,))
        rows = cur.fetchall()
        resultados = [(r["ID_PROJETO"], r["TITULO"], r["NOME_ORG"], r["DATA_CANDIDATURA"]) for r in rows]
        conn.close()
        return resultados, None
    except Exception as e:
        return None, str(e)

def atualizar_projeto_db(novo_titulo, nova_descricao, id_projeto, cnpj_org):
    try:
        conn = get_conn()
        cur = conn.cursor()
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # se titulo/desc vierem vazios, mantemos os atuais
        if not novo_titulo and not nova_descricao:
            return False, "Nenhum campo para atualizar."
        if novo_titulo and nova_descricao:
            cur.execute("UPDATE Projeto SET TITULO=?, DESCRICAO=?, ULTIMA_ATUALIZACAO=? WHERE ID_PROJETO=? AND CNPJ_ORG=?",
                        (novo_titulo, nova_descricao, agora, id_projeto, cnpj_org))
        elif novo_titulo:
            cur.execute("UPDATE Projeto SET TITULO=?, ULTIMA_ATUALIZACAO=? WHERE ID_PROJETO=? AND CNPJ_ORG=?",
                        (novo_titulo, agora, id_projeto, cnpj_org))
        else:
            cur.execute("UPDATE Projeto SET DESCRICAO=?, ULTIMA_ATUALIZACAO=? WHERE ID_PROJETO=? AND CNPJ_ORG=?",
                        (nova_descricao, agora, id_projeto, cnpj_org))
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

def excluir_projeto_db(id_projeto, cnpj_org):
    try:
        conn = get_conn()
        cur = conn.cursor()
        # exclui candidaturas e mensagens relacionadas antes de excluir projeto
        cur.execute("DELETE FROM Candidatura WHERE ID_PROJETO=?", (id_projeto,))
        cur.execute("DELETE FROM Mensagem WHERE ID_PROJETO=?", (id_projeto,))
        cur.execute("DELETE FROM Projeto WHERE ID_PROJETO=? AND CNPJ_ORG=?", (id_projeto, cnpj_org))
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

def relatorio_pesquisa_db(cnpj_org, filtro, termo):
    try:
        conn = get_conn()
        cur = conn.cursor()
        if filtro == '1':  # título
            cur.execute("SELECT ID_PROJETO, TITULO, (SELECT COUNT(*) FROM Candidatura WHERE ID_PROJETO=Projeto.ID_PROJETO) AS CANDIDATOS, DATA_CRIACAO FROM Projeto WHERE CNPJ_ORG=? AND TITULO LIKE ? ORDER BY DATA_CRIACAO DESC", (cnpj_org, f"%{termo}%"))
        elif filtro == '2':  # Em Andamento — por enquanto, consideramos projeto com candidatos
            cur.execute("SELECT ID_PROJETO, TITULO, (SELECT COUNT(*) FROM Candidatura WHERE ID_PROJETO=Projeto.ID_PROJETO) AS CANDIDATOS, DATA_CRIACAO FROM Projeto WHERE CNPJ_ORG=? AND (SELECT COUNT(*) FROM Candidatura WHERE ID_PROJETO=Projeto.ID_PROJETO) > 0 ORDER BY DATA_CRIACAO DESC", (cnpj_org,))
        elif filtro == '3':  # Disponível — sem candidatos
            cur.execute("SELECT ID_PROJETO, TITULO, (SELECT COUNT(*) FROM Candidatura WHERE ID_PROJETO=Projeto.ID_PROJETO) AS CANDIDATOS, DATA_CRIACAO FROM Projeto WHERE CNPJ_ORG=? AND (SELECT COUNT(*) FROM Candidatura WHERE ID_PROJETO=Projeto.ID_PROJETO) = 0 ORDER BY DATA_CRIACAO DESC", (cnpj_org,))
        else:
            return None, "Filtro inválido."
        rows = cur.fetchall()
        resultados = [(r["ID_PROJETO"], r["TITULO"], r["CANDIDATOS"], r["DATA_CRIACAO"]) for r in rows]
        conn.close()
        return resultados, None
    except Exception as e:
        return None, str(e)

def remover_candidatura_db(id_projeto, rgm_aluno):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Candidatura WHERE ID_PROJETO=? AND RGM_ALUNO=?", (id_projeto, rgm_aluno))
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# --------------------------
# Mensagens (chat interno)
# --------------------------

def enviar_mensagem_db(id_projeto, remetente, id_remetente, mensagem, data_envio):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO Mensagem (ID_PROJETO, REMETENTE, ID_REMETENTE, MENSAGEM, DATA_ENVIO) VALUES (?, ?, ?, ?, ?)",
                    (id_projeto, remetente, str(id_remetente), mensagem, data_envio))
        conn.commit()
        conn.close()
        # atualiza ULTIMA_ATUALIZACAO do projeto
        try:
            cur = get_conn().cursor()
            cur.execute("UPDATE Projeto SET ULTIMA_ATUALIZACAO=? WHERE ID_PROJETO=?", (data_envio, id_projeto))
            cur.connection.commit()
            cur.connection.close()
        except:
            pass
        return True, None
    except Exception as e:
        return False, str(e)

def listar_mensagens_db(id_projeto):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT REMETENTE, ID_REMETENTE, MENSAGEM, DATA_ENVIO FROM Mensagem WHERE ID_PROJETO=? ORDER BY DATA_ENVIO ASC", (id_projeto,))
        rows = cur.fetchall()
        resultados = [(r["REMETENTE"], r["ID_REMETENTE"], r["MENSAGEM"], r["DATA_ENVIO"]) for r in rows]
        conn.close()
        return resultados, None
    except Exception as e:
        return None, str(e)

# Inicializa DB ao importar
init_db()
