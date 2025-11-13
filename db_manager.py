import sqlite3
#from datetime import datetime

# --- Funções Auxiliares de Validação (Banco) ---

def checar_se_existe_db(tabela, coluna, valor):
    """Verifica se um valor já existe em uma tabela. Retorna True se existir."""
    conn = None
    existe = False
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql = f"SELECT 1 FROM {tabela} WHERE {coluna} = ?"
        cursor.execute(sql, (valor,))
        if cursor.fetchone(): 
            existe = True
    except sqlite3.Error as e:
        print(f"Erro ao checar dados no DB: {e}")
    finally:
        if conn:
            conn.close()
    return existe

def checar_candidatura_duplicada_db(id_projeto, rgm_aluno):
    """Verifica se este aluno já se candidatou a este projeto."""
    conn = None
    existe = False
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql = "SELECT 1 FROM Candidatura WHERE ID_PROJETO = ? AND RGM_ALUNO = ?"
        cursor.execute(sql, (id_projeto, rgm_aluno))
        if cursor.fetchone(): 
            existe = True
    except sqlite3.Error as e:
        print(f"Erro ao checar candidatura no DB: {e}")
    finally:
        if conn:
            conn.close()
    return existe

# --- (A) Funções de CADASTRO (Banco) ---

def cadastrar_aluno_db(rgm, nome, senha, data):
    """(C) Insere um novo aluno no banco."""
    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Aluno (RGM_ALUNO, NOME_ALUNO, SENHA, DATA_CADASTRO) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (rgm, nome, senha, data)) 
        conn.commit() 
        return True, None
    except sqlite3.Error as e: 
        return False, str(e)
    finally:
        if conn:
            conn.close() 

def cadastrar_organizacao_db(cnpj, nome, senha, data):
    """(C) Insere uma nova organização no banco."""
    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Organizacao (CNPJ_ORG, NOME_ORG, SENHA, DATA_CADASTRO) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (cnpj, nome, senha, data)) 
        conn.commit() 
        return True, None
    except sqlite3.Error as e: 
        return False, str(e)
    finally:
        if conn:
            conn.close() 

def cadastrar_projeto_db(titulo, descricao, cnpj_org, data):
    """(C) Insere um novo projeto no banco."""
    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Projeto (TITULO, DESCRICAO, CNPJ_ORG, DATA_CRIACAO) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (titulo, descricao, cnpj_org, data))
        conn.commit() 
        return True, None
    except sqlite3.Error as e: 
        return False, str(e)
    finally:
        if conn:
            conn.close() 

def candidatar_a_projeto_db(id_projeto, rgm_aluno, data):
    """(C) Insere uma nova candidatura no banco."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Candidatura (ID_PROJETO, RGM_ALUNO, DATA_CANDIDATURA) VALUES (?, ?, ?)"
        cursor.execute(sql_insert, (id_projeto, rgm_aluno, data))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "ID de projeto não encontrado ou candidatura duplicada."
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        if conn:
            conn.close()

# --- (B) Funções de LOGIN (Banco) ---

def login_aluno_db(rgm, senha):
    """Verifica RGM e Senha no banco. Retorna o nome do aluno ou None."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_select = "SELECT NOME_ALUNO FROM Aluno WHERE RGM_ALUNO = ? AND SENHA = ?"
        cursor.execute(sql_select, (rgm, senha))
        resultado = cursor.fetchone() 
        if resultado:
            return resultado[0] 
        else:
            return None 
    except sqlite3.Error as e:
        print(f"Erro ao fazer login (Aluno DB): {e}")
        return None
    finally:
        if conn:
            conn.close()

def login_organizacao_db(cnpj, senha):
    """Verifica CNPJ e Senha no banco. Retorna o nome da organização ou None."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_select = "SELECT NOME_ORG FROM Organizacao WHERE CNPJ_ORG = ? AND SENHA = ?"
        cursor.execute(sql_select, (cnpj, senha))
        resultado = cursor.fetchone() 
        if resultado:
            return resultado[0] 
        else:
            return None 
    except sqlite3.Error as e:
        print(f"Erro ao fazer login (Org DB): {e}")
        return None
    finally:
        if conn:
            conn.close()

# --- (D/E) Funções de LEITURA (Banco) ---

def listar_projetos_org_db(cnpj_org):
    """(R) Busca a lista de projetos de uma organização."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql = """
            SELECT P.ID_PROJETO, P.TITULO, 
                   (SELECT COUNT(*) FROM Candidatura C WHERE C.ID_PROJETO = P.ID_PROJETO) AS Candidatos,
                   P.DATA_CRIACAO
            FROM Projeto AS P
            WHERE P.CNPJ_ORG = ?
        """
        cursor.execute(sql, (cnpj_org,))
        return cursor.fetchall(), None
    except sqlite3.Error as e:
        return [], str(e)
    finally:
        if conn:
            conn.close()

def listar_candidatos_db(id_projeto):
    """(R) Busca a lista de candidatos de um projeto."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_candidatos = """
            SELECT A.RGM_ALUNO, A.NOME_ALUNO, C.DATA_CANDIDATURA
            FROM Candidatura AS C
            JOIN Aluno AS A ON C.RGM_ALUNO = A.RGM_ALUNO
            WHERE C.ID_PROJETO = ?
        """
        cursor.execute(sql_candidatos, (id_projeto,))
        return cursor.fetchall(), None
    except sqlite3.Error as e:
        return [], str(e)
    finally:
        if conn:
            conn.close()

def get_projeto_detalhes_db(id_projeto, cnpj_org):
    """(R) Busca os detalhes de um projeto específico."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_projeto = "SELECT TITULO, DESCRICAO, DATA_CRIACAO FROM Projeto WHERE ID_PROJETO = ? AND CNPJ_ORG = ?"
        cursor.execute(sql_projeto, (id_projeto, cnpj_org))
        return cursor.fetchone(), None
    except sqlite3.Error as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()

def get_projeto_detalhes_publico_db(id_projeto):
    """(R) Busca os detalhes públicos de um projeto (para alunos)."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql = """
            SELECT P.TITULO, P.DESCRICAO, O.NOME_ORG, P.DATA_CRIACAO
            FROM Projeto AS P
            JOIN Organizacao AS O ON P.CNPJ_ORG = O.CNPJ_ORG
            WHERE P.ID_PROJETO = ?
        """
        cursor.execute(sql, (id_projeto,))
        return cursor.fetchone(), None
    except sqlite3.Error as e:
        return None, str(e)
    finally:
        if conn:
            conn.close()

def listar_projetos_disponiveis_db(rgm_aluno):
    """(R) Busca projetos que o aluno ainda não se candidatou."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql = """
            SELECT P.ID_PROJETO, P.TITULO, O.NOME_ORG AS ORGANIZACAO, P.DATA_CRIACAO
            FROM Projeto AS P
            JOIN Organizacao AS O ON P.CNPJ_ORG = O.CNPJ_ORG
            WHERE NOT EXISTS (
                SELECT 1 FROM Candidatura C 
                WHERE C.ID_PROJETO = P.ID_PROJETO AND C.RGM_ALUNO = ?
            )
        """
        cursor.execute(sql, (rgm_aluno,))
        return cursor.fetchall(), None
    except sqlite3.Error as e:
        return [], str(e)
    finally:
        if conn:
            conn.close()

def ver_minhas_candidaturas_db(rgm_aluno):
    """(R) Busca os projetos aos quais o aluno se candidatou."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql = """
            SELECT P.ID_PROJETO, P.TITULO, O.NOME_ORG AS ORGANIZACAO, C.DATA_CANDIDATURA
            FROM Projeto AS P
            JOIN Organizacao AS O ON P.CNPJ_ORG = O.CNPJ_ORG
            JOIN Candidatura AS C ON P.ID_PROJETO = C.ID_PROJETO
            WHERE C.RGM_ALUNO = ?
        """
        cursor.execute(sql, (rgm_aluno,))
        return cursor.fetchall(), None
    except sqlite3.Error as e:
        return [], str(e)
    finally:
        if conn:
            conn.close()

# --- (F) Funções de ATUALIZAÇÃO e EXCLUSÃO (Banco) ---

def atualizar_projeto_db(novo_titulo, nova_descricao, id_projeto, cnpj_org):
    """(U) Atualiza um projeto no banco."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_update = """
            UPDATE Projeto 
            SET 
                TITULO = CASE WHEN ? = '' THEN TITULO ELSE ? END,
                DESCRICAO = CASE WHEN ? = '' THEN DESCRICAO ELSE ? END
            WHERE ID_PROJETO = ? AND CNPJ_ORG = ? 
        """
        cursor.execute(sql_update, (novo_titulo, novo_titulo, nova_descricao, nova_descricao, id_projeto, cnpj_org))
        
        if cursor.rowcount == 0:
            return False, "Nenhum projeto encontrado com este ID ou permissão negada."
        else:
            conn.commit()
            return True, None
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        if conn:
            conn.close()

def excluir_projeto_db(id_projeto, cnpj_org):
    """(D) Exclui um projeto e suas candidaturas."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        
        sql_delete_candidaturas = "DELETE FROM Candidatura WHERE ID_PROJETO = ?"
        cursor.execute(sql_delete_candidaturas, (id_projeto,))

        sql_delete_projeto = "DELETE FROM Projeto WHERE ID_PROJETO = ? AND CNPJ_ORG = ?"
        cursor.execute(sql_delete_projeto, (id_projeto, cnpj_org))
        
        if cursor.rowcount == 0:
            return False, "Nenhum projeto encontrado com este ID ou permissão negada."
        else:
            conn.commit()
            return True, None
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        if conn:
            conn.close()

def remover_candidatura_db(id_projeto, rgm_aluno):
    """(D) Remove uma candidatura específica do banco."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_delete = "DELETE FROM Candidatura WHERE ID_PROJETO = ? AND RGM_ALUNO = ?"
        cursor.execute(sql_delete, (id_projeto, rgm_aluno))
        
        if cursor.rowcount == 0:
            return False, "Candidatura não encontrada ou ID de projeto inválido."
        else:
            conn.commit()
            return True, None
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        if conn:
            conn.close()

# --- (G) Funções de RELATÓRIO (Banco) ---

def relatorio_pesquisa_db(cnpj_org, filtro, termo=None):
    """(R) Busca o relatório filtrado no banco."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        sql_base = """
            SELECT P.ID_PROJETO, P.TITULO, 
                   (SELECT COUNT(*) FROM Candidatura C WHERE C.ID_PROJETO = P.ID_PROJETO) AS Candidatos,
                   P.DATA_CRIACAO
            FROM Projeto AS P
            WHERE P.CNPJ_ORG = ?
        """
        params = [cnpj_org]
        
        if filtro == '1': # Título
            sql_base += " AND P.TITULO LIKE ?"
            params.append(f"%{termo}%")
        elif filtro == '2': # Em Andamento
            sql_base += " AND (SELECT COUNT(*) FROM Candidatura C WHERE C.ID_PROJETO = P.ID_PROJETO) > 0"
        elif filtro == '3': # Disponível
            sql_base += " AND (SELECT COUNT(*) FROM Candidatura C WHERE C.ID_PROJETO = P.ID_PROJETO) = 0"

        cursor.execute(sql_base, tuple(params))
        return cursor.fetchall(), None
    except sqlite3.Error as e:
        return [], str(e)
    finally:
        if conn:
            conn.close()