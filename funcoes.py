import os
import sqlite3
import time
import getpass
from datetime import datetime
from tabulate import tabulate 

# --- Tabela de Cores (Códigos ANSI) ---
VERMELHO = '\033[91m'
VERDE    = '\033[92m'
AMARELO  = '\033[93m'
AZUL     = '\033[94m'
CIANO    = '\033[96m'
BOLD     = '\033[1m'
RESET    = '\033[0m'
EMOJI_SUCESSO = "✅"
EMOJI_ALERTA  = "⚠️"
# --- Fim da Tabela ---

def limpar_tela():
    """Limpa o console, funciona em Windows, Mac e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Funções Auxiliares de Validação ---

def is_alpha_space(s):
    """Verifica se a string contém apenas letras e espaços."""
    if not s:
        return False
    return all(c.isalpha() or c.isspace() for c in s)

def checar_se_existe(tabela, coluna, valor):
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
        print(f"\n{VERMELHO}Erro ao checar dados: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
    return existe

def checar_candidatura_duplicada(id_projeto, rgm_aluno):
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
        print(f"\n{VERMELHO}Erro ao checar dados: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
    return existe

# --- (A) Funções de CADASTRO ---

def cadastrar_aluno():
    """Coleta dados e cadastra um novo aluno no banco."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}        CADASTRAR NOVO ALUNO             {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    while True:
        rgm = input(f"{BOLD}Digite o RGM (apenas números): {RESET}")
        if not rgm.isdigit(): 
            print(f"{VERMELHO}Erro: O RGM deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            continue
        if checar_se_existe('Aluno', 'RGM_ALUNO', rgm): 
            print(f"{VERMELHO}Erro: Este RGM já está cadastrado. {EMOJI_ALERTA}{RESET}")
            continue
        break 

    while True:
        nome = input(f"{BOLD}Digite o Nome Completo: {RESET}")
        if is_alpha_space(nome): 
            break
        else:
            print(f"{VERMELHO}Erro: O Nome deve conter apenas letras e espaços. {EMOJI_ALERTA}{RESET}")

    while True:
        senha = getpass.getpass(f"{BOLD}Digite uma senha (6 a 8 caracteres): {RESET}")
        if 6 <= len(senha) <= 8: 
            break
        else:
            print(f"{VERMELHO}Erro: A senha deve ter entre 6 e 8 caracteres. {EMOJI_ALERTA}{RESET}")

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Aluno (RGM_ALUNO, NOME_ALUNO, SENHA, DATA_CADASTRO) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (rgm, nome, senha, agora)) 
        conn.commit() 
        print(f"\n{VERDE}Aluno {nome} cadastrado com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    except sqlite3.Error as e: 
        print(f"\n{VERMELHO}Erro ao cadastrar aluno: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close() 
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def cadastrar_organizacao():
    """Coleta dados e cadastra uma nova organização no banco."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}      CADASTRAR NOVA ORGANIZAÇÃO         {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    while True:
        cnpj = input(f"{BOLD}Digite o CNPJ (apenas 14 números): {RESET}")
        if not cnpj.isdigit(): 
            print(f"{VERMELHO}Erro: O CNPJ deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            continue
        if len(cnpj) != 14:
            print(f"{VERMELHO}Erro: O CNPJ deve ter exatamente 14 dígitos. {EMOJI_ALERTA}{RESET}")
            continue
        if checar_se_existe('Organizacao', 'CNPJ_ORG', cnpj): 
            print(f"{VERMELHO}Erro: Este CNPJ já está cadastrado. {EMOJI_ALERTA}{RESET}")
            continue
        break 

    while True:
        nome = input(f"{BOLD}Digite o Nome da Organização: {RESET}")
        if is_alpha_space(nome): 
            break
        else:
            print(f"{VERMELHO}Erro: O Nome deve conter apenas letras e espaços. {EMOJI_ALERTA}{RESET}")

    while True:
        senha = getpass.getpass(f"{BOLD}Digite uma senha (6 a 8 caracteres): {RESET}")
        if 6 <= len(senha) <= 8: 
            break
        else:
            print(f"{VERMELHO}Erro: A senha deve ter entre 6 e 8 caracteres. {EMOJI_ALERTA}{RESET}")

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Organizacao (CNPJ_ORG, NOME_ORG, SENHA, DATA_CADASTRO) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (cnpj, nome, senha, agora)) 
        conn.commit() 
        print(f"\n{VERDE}Organização {nome} cadastrada com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    except sqlite3.Error as e: 
        print(f"\n{VERMELHO}Erro ao cadastrar organização: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close() 
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def realizar_cadastro():
    """Exibe o menu de cadastro (Aluno ou Organização)."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}         PORTAL DE CADASTRO              {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{CIANO}1 - Cadastrar como Aluno{RESET}")
        print(f"{CIANO}2 - Cadastrar como Organização{RESET}")
        print(f"{VERMELHO}0 - Voltar ao menu anterior{RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        tipo = input(f"{BOLD}Escolha uma opção: {RESET}") 
        
        if tipo == '1':
            cadastrar_aluno() 
        elif tipo == '2':
            cadastrar_organizacao() 
        elif tipo == '0':
            print("Voltando ao menu principal...")
            time.sleep(1) 
            break 
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar ao menu{RESET}")

# --- (B) Funções de LOGIN ---

def login_aluno():
    """Realiza o login do aluno, validando RGM e Senha separadamente."""
    rgm = "" 
    while True: 
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}           LOGIN DE ALUNO                {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        rgm = input(f"{BOLD}Digite seu RGM (ou 0 para Voltar): {RESET}")
        
        if rgm == '0':
            print("Voltando ao menu anterior...")
            time.sleep(1)
            return 

        if not rgm.isdigit(): 
            print(f"{VERMELHO}Erro: O RGM deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para tentar novamente...{RESET}")
            continue
        
        if not checar_se_existe('Aluno', 'RGM_ALUNO', rgm):
            print(f"{VERMELHO}Erro: RGM não cadastrado. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para tentar novamente...{RESET}")
            continue
        break 

    while True:
        senha = getpass.getpass(f"{BOLD}Digite sua senha (ou 0 para Voltar): {RESET}")
        
        if senha == '0':
            print("Voltando...")
            time.sleep(1)
            break 
            
        conn = None
        try:
            conn = sqlite3.connect('tabela.db')
            cursor = conn.cursor()
            sql_select = "SELECT NOME_ALUNO FROM Aluno WHERE RGM_ALUNO = ? AND SENHA = ?"
            cursor.execute(sql_select, (rgm, senha))
            resultado = cursor.fetchone() 
            
            if resultado:
                nome_aluno = resultado[0] 
                print(f"\n{VERDE}Login bem-sucedido! Bem-vindo(a), {nome_aluno}! {EMOJI_SUCESSO}{RESET}")
                time.sleep(2)
                menu_aluno(rgm, nome_aluno)
                return 
            else:
                print(f"\n{VERMELHO}Senha incorreta. {EMOJI_ALERTA}{RESET}")
                
        except sqlite3.Error as e:
            print(f"\n{VERMELHO}Erro ao fazer login: {e} {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        finally:
            if conn:
                conn.close()
    
    login_aluno() 

def login_organizacao():
    """Realiza o login da organização, validando CNPJ e Senha separadamente."""
    cnpj = "" 
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}         LOGIN DA ORGANIZAÇÃO            {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        cnpj = input(f"{BOLD}Digite seu CNPJ (ou 0 para Voltar): {RESET}")
        
        if cnpj == '0':
            print("Voltando ao menu anterior...")
            time.sleep(1)
            return 

        if not cnpj.isdigit():
            print(f"{VERMELHO}Erro: O CNPJ deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para tentar novamente...{RESET}")
            continue 
            
        if len(cnpj) != 14:
            print(f"{VERMELHO}Erro: O CNPJ deve ter exatamente 14 dígitos. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para tentar novamente...{RESET}")
            continue 
        
        if not checar_se_existe('Organizacao', 'CNPJ_ORG', cnpj):
            print(f"{VERMELHO}Erro: CNPJ não cadastrado. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para tentar novamente...{RESET}")
            continue
        break 
        
    while True:
        senha = getpass.getpass(f"{BOLD}Digite sua senha (ou 0 para Voltar): {RESET}")
        
        if senha == '0':
            print("Voltando...")
            time.sleep(1)
            break 
        
        conn = None
        try:
            conn = sqlite3.connect('tabela.db')
            cursor = conn.cursor()
            sql_select = "SELECT NOME_ORG FROM Organizacao WHERE CNPJ_ORG = ? AND SENHA = ?"
            cursor.execute(sql_select, (cnpj, senha))
            
            resultado = cursor.fetchone() 
            
            if resultado:
                nome_org = resultado[0] 
                print(f"\n{VERDE}Login bem-sucedido! Bem-vinda, {nome_org}! {EMOJI_SUCESSO}{RESET}")
                time.sleep(2)
                menu_organizacao(cnpj, nome_org) 
                return 
            else:
                print(f"\n{VERMELHO}Senha incorreta. {EMOJI_ALERTA}{RESET}")
                
        except sqlite3.Error as e:
            print(f"\n{VERMELHO}Erro ao fazer login: {e} {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        finally:
            if conn:
                conn.close()

    login_organizacao() 

def realizar_login():
    """Exibe o menu de login (Aluno ou Organização)."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}           PORTAL DE LOGIN               {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{CIANO}1 - Login como Aluno{RESET}")
        print(f"{CIANO}2 - Login como Organização{RESET}")
        print(f"{VERMELHO}0 - Voltar ao menu anterior{RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        tipo = input(f"{BOLD}Escolha uma opção: {RESET}") 
        
        if tipo == '1':
            login_aluno() 
        elif tipo == '2':
            login_organizacao() 
        elif tipo == '0':
            print("Voltando ao menu principal...")
            time.sleep(1) 
            break 
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar ao menu{RESET}")

# --- (C) Funções dos MENUS INTERNOS ---

def menu_aluno(rgm_aluno, nome_aluno):
    """Menu que o aluno vê após logar."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}           PAINEL DO ALUNO               {RESET}")
        print(f"Bem-vindo(a), {nome_aluno} (RGM: {rgm_aluno})!")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        print(f"{CIANO}1 - Listar Projetos Disponíveis{RESET}")
        print(f"{CIANO}2 - Me candidatar a um Projeto{RESET}")
        print(f"{CIANO}3 - Ver minhas candidaturas{RESET}")
        print(f"{VERMELHO}0 - Logout (Sair){RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        opt = input(f"{BOLD}Escolha uma opção: {RESET}")
        
        if opt == '1':
            listar_projetos_disponiveis(rgm_aluno) # ATUALIZADO
        elif opt == '2':
            candidatar_a_projeto(rgm_aluno) # ATUALIZADO
        elif opt == '3':
            ver_minhas_candidaturas(rgm_aluno) # ATUALIZADO
        elif opt == '0':
            print(f"Fazendo logout, até logo {nome_aluno}!")
            time.sleep(2)
            break 
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar...{RESET}")

def menu_organizacao(cnpj_org, nome_org):
    """Menu que a organização vê após logar."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}         PAINEL DA ORGANIZAÇÃO           {RESET}")
        print(f"Bem-vinda, {nome_org} (CNPJ: {cnpj_org})")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        print(f"{CIANO}1 - Cadastrar Novo Projeto{RESET}")
        print(f"{CIANO}2 - Listar Meus Projetos (Ver Detalhes){RESET}")
        print(f"{CIANO}3 - Atualizar Projeto{RESET}")
        print(f"{CIANO}4 - Excluir Projeto{RESET}")
        print(f"{VERMELHO}0 - Logout (Sair){RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        opt = input(f"{BOLD}Escolha uma opção: {RESET}")
        
        if opt == '1':
            cadastrar_projeto(cnpj_org, nome_org) 
        elif opt == '2':
            listar_meus_projetos(cnpj_org, nome_org) 
        elif opt == '3':
            atualizar_projeto(cnpj_org, nome_org) 
        elif opt == '4':
            excluir_projeto(cnpj_org, nome_org) 
        elif opt == '0':
            print(f"Fazendo logout, até logo {nome_org}!")
            time.sleep(2)
            break 
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar ao menu{RESET}")

def cadastrar_projeto(cnpj_org, nome_org):
    """(C) Função para a organização logada cadastrar um projeto."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}       CADASTRAR NOVO PROJETO            {RESET}")
    print(f"Organização: {nome_org}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    while True:
        titulo = input(f"{BOLD}Digite o Título do projeto: {RESET}")
        if titulo.strip():
            break
        else:
            print(f"{VERMELHO}Erro: O Título não pode ser vazio. {EMOJI_ALERTA}{RESET}")

    while True:
        descricao = input(f"{BOLD}Digite a Descrição do projeto (máx 250 caracteres): {RESET}")
        if not descricao.strip():
            print(f"{VERMELHO}Erro: A Descrição não pode ser vazia. {EMOJI_ALERTA}{RESET}")
            continue
        if len(descricao) > 250:
            print(f"{VERMELHO}Erro: A Descrição ultrapassou 250 caracteres. ({len(descricao)}) {EMOJI_ALERTA}{RESET}")
            continue
        break

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        
        # O RGM_ALUNO foi removido desta tabela
        sql_insert = "INSERT INTO Projeto (TITULO, DESCRICAO, CNPJ_ORG, DATA_CRIACAO) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_insert, (titulo, descricao, cnpj_org, agora))
        
        conn.commit() 
        print(f"\n{VERDE}Projeto '{titulo}' cadastrado com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    
    except sqlite3.Error as e: 
        print(f"\n{VERMELHO}Erro ao cadastrar projeto: {e} {EMOJI_ALERTA}{RESET}")
    
    finally:
        if conn:
            conn.close() 
    
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

# --- (D) Funções de CRUD da Organização (R, U, D) ---

def _mostrar_projetos_org(cursor, cnpj_org):
    """Função auxiliar que busca e exibe a tabela de projetos."""
    # Este SQL agora usa um COUNT da nova tabela Candidatura
    sql = """
        SELECT 
            P.ID_PROJETO, 
            P.TITULO, 
            (SELECT COUNT(*) FROM Candidatura C WHERE C.ID_PROJETO = P.ID_PROJETO) AS Candidatos,
            P.DATA_CRIACAO
        FROM Projeto AS P
        WHERE P.CNPJ_ORG = ?
    """
    cursor.execute(sql, (cnpj_org,))
    resultados = cursor.fetchall() 

    if not resultados:
        print(f"\n{AMARELO}Você ainda não cadastrou nenhum projeto. {EMOJI_ALERTA}{RESET}")
        return False 
    else:
        headers = [f"{BOLD}ID PROJETO{RESET}", 
                   f"{BOLD}TÍTULO{RESET}", 
                   f"{BOLD}Nº DE CANDIDATOS{RESET}", 
                   f"{BOLD}DATA CRIAÇÃO{RESET}"]
        
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
        return True 

def _mostrar_detalhes_projeto_org(cursor, id_projeto, cnpj_org):
    """Mostra os detalhes completos de um projeto e a lista de candidatos."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}        DETALHES DO PROJETO ID {id_projeto}        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    # 1. Busca os detalhes do projeto
    sql_projeto = "SELECT TITULO, DESCRICAO, DATA_CRIACAO FROM Projeto WHERE ID_PROJETO = ? AND CNPJ_ORG = ?"
    cursor.execute(sql_projeto, (id_projeto, cnpj_org))
    projeto = cursor.fetchone() 

    if not projeto:
        print(f"\n{VERMELHO}Projeto ID {id_projeto} não encontrado ou não pertence à sua organização. {EMOJI_ALERTA}{RESET}")
        return

    titulo, desc, data_c = projeto
    print(f"\n{BOLD}ID:{RESET}         {id_projeto}")
    print(f"{BOLD}Título:{RESET}     {titulo}")
    print(f"{BOLD}Data Criação:{RESET} {data_c}")
    print(f"\n{BOLD}Descrição Completa:{RESET}\n {desc}")
    print(f"\n{BOLD}{AZUL}--- CANDIDATOS ---{RESET}")

    # 2. Busca a lista de candidatos para este projeto
    sql_candidatos = """
        SELECT A.RGM_ALUNO, A.NOME_ALUNO, C.DATA_CANDIDATURA
        FROM Candidatura AS C
        JOIN Aluno AS A ON C.RGM_ALUNO = A.RGM_ALUNO
        WHERE C.ID_PROJETO = ?
    """
    cursor.execute(sql_candidatos, (id_projeto,))
    candidatos = cursor.fetchall() # Pega a "lista de listas"

    if not candidatos:
        print(f"{AMARELO}Este projeto ainda não tem candidatos.{RESET}")
    else:
        headers = [f"{BOLD}RGM ALUNO{RESET}", f"{BOLD}NOME{RESET}", f"{BOLD}DATA CANDIDATURA{RESET}"]
        print(tabulate(candidatos, headers=headers, tablefmt="fancy_grid"))
        
    print(f"\n{BOLD}{AZUL}========================================={RESET}")


def listar_meus_projetos(cnpj_org, nome_org):
    """(R) Lista projetos e permite ver detalhes de um ID específico."""
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        while True: 
            limpar_tela()
            print(f"{BOLD}{AZUL}========================================={RESET}")
            print(f"{BOLD}{AZUL}          MEUS PROJETOS ({nome_org})        {RESET}")
            print(f"{BOLD}{AZUL}========================================={RESET}")

            if not _mostrar_projetos_org(cursor, cnpj_org):
                break 

            print(f"\n{CIANO}--- Opções ---{RESET}")
            id_proj = input(f"{BOLD}Digite o ID do projeto para ver detalhes (ou 0 para voltar): {RESET}")

            if id_proj == '0':
                break 
            
            if not id_proj.isdigit():
                print(f"\n{VERMELHO}ID inválido. Deve ser um número. {EMOJI_ALERTA}{RESET}")
                time.sleep(2)
                continue 

            _mostrar_detalhes_projeto_org(cursor, id_proj, cnpj_org)
            input(f"\n{AZUL}Pressione Enter para voltar à lista de projetos...{RESET}")
            
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao listar projetos: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
            
    if 'conn' not in locals() or not conn:
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")


def atualizar_projeto(cnpj_org, nome_org):
    """(U) Atualiza o título e a descrição de um projeto."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         ATUALIZAR PROJETO ({nome_org})        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        if not _mostrar_projetos_org(cursor, cnpj_org):
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            return 

        print(f"\n{AMARELO}Qual projeto você deseja atualizar?{RESET}")
        id_projeto = input(f"{BOLD}Digite o ID do Projeto (ou 0 para cancelar): {RESET}")
        
        if id_projeto == '0':
            return
        if not id_projeto.isdigit():
            print(f"\n{VERMELHO}ID inválido. Deve ser um número. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            return

        print(f"\n{CIANO}Deixe em branco para manter a informação atual.{RESET}")
        novo_titulo = input(f"{BOLD}Novo Título: {RESET}")
        nova_descricao = input(f"{BOLD}Nova Descrição (máx 250): {RESET}")
        
        sql_update = """
            UPDATE Projeto 
            SET 
                TITULO = CASE WHEN ? = '' THEN TITULO ELSE ? END,
                DESCRICAO = CASE WHEN ? = '' THEN DESCRICAO ELSE ? END
            WHERE ID_PROJETO = ? AND CNPJ_ORG = ? 
        """
        cursor.execute(sql_update, (novo_titulo, novo_titulo, nova_descricao, nova_descricao, id_projeto, cnpj_org))
        
        if cursor.rowcount == 0:
            print(f"\n{VERMELHO}Nenhum projeto encontrado com este ID ou você não tem permissão. {EMOJI_ALERTA}{RESET}")
        else:
            conn.commit()
            print(f"\n{VERDE}Projeto ID {id_projeto} atualizado com sucesso! {EMOJI_SUCESSO}{RESET}")

    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao atualizar projeto: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def excluir_projeto(cnpj_org, nome_org):
    """(D) Exclui um projeto."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}          EXCLUIR PROJETO ({nome_org})         {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        if not _mostrar_projetos_org(cursor, cnpj_org):
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            return 

        print(f"\n{VERMELHO}{BOLD}Qual projeto você deseja EXCLUIR?{RESET}")
        id_projeto = input(f"{BOLD}Digite o ID do Projeto (ou 0 para cancelar): {RESET}")
        
        if id_projeto == '0':
            return
        if not id_projeto.isdigit():
            print(f"\n{VERMELHO}ID inválido. Deve ser um número. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            return
            
        confirmacao = input(f"\n{AMARELO}Tem certeza que deseja excluir o projeto ID {id_projeto}? {VERMELHO}{BOLD}(S/N): {RESET}").upper()
        
        if confirmacao == 'S':
            sql_delete = "DELETE FROM Projeto WHERE ID_PROJETO = ? AND CNPJ_ORG = ?"
            cursor.execute(sql_delete, (id_projeto, cnpj_org))
            
            if cursor.rowcount == 0:
                print(f"\n{VERMELHO}Nenhum projeto encontrado com este ID ou você não tem permissão. {EMOJI_ALERTA}{RESET}")
            else:
                conn.commit()
                print(f"\n{VERDE}Projeto ID {id_projeto} excluído com sucesso! {EMOJI_SUCESSO}{RESET}")
        else:
            print(f"\n{CIANO}Exclusão cancelada.{RESET}")

    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao excluir projeto: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

# --- (E) Funções de CRUD do Aluno ---

def listar_projetos_disponiveis(rgm_aluno):
    """(R) Lista todos os projetos aos quais o aluno AINDA NÃO se candidatou."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         PROJETOS DISPONÍVEIS            {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        # Este SQL complexo busca projetos (P) e junta o nome da organização (O),
        # mas APENAS se o ID do projeto NÃO ESTIVER na lista de candidaturas
        # deste aluno (sub-query com 'NOT EXISTS').
        sql = """
            SELECT 
                P.ID_PROJETO, 
                P.TITULO, 
                O.NOME_ORG AS ORGANIZACAO,
                P.DATA_CRIACAO
            FROM Projeto AS P
            JOIN Organizacao AS O ON P.CNPJ_ORG = O.CNPJ_ORG
            WHERE NOT EXISTS (
                SELECT 1 FROM Candidatura C 
                WHERE C.ID_PROJETO = P.ID_PROJETO AND C.RGM_ALUNO = ?
            )
        """
        cursor.execute(sql, (rgm_aluno,))
        resultados = cursor.fetchall() 

        if not resultados:
            print(f"\n{AMARELO}Não há novos projetos disponíveis para você no momento. {EMOJI_ALERTA}{RESET}")
        else:
            headers = [f"{BOLD}ID PROJETO{RESET}", 
                       f"{BOLD}TÍTULO{RESET}", 
                       f"{BOLD}ORGANIZAÇÃO{RESET}", 
                       f"{BOLD}DATA CRIAÇÃO{RESET}"]
            
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
            
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao listar projetos: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def candidatar_a_projeto(rgm_aluno):
    """(C) Permite ao aluno se candidatar (INSERT) a um projeto."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}       CANDIDATAR-SE A UM PROJETO        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        # 1. Mostra a lista de projetos disponíveis (aos quais ele não se candidatou)
        sql_disponiveis = """
            SELECT P.ID_PROJETO, P.TITULO, O.NOME_ORG
            FROM Projeto AS P
            JOIN Organizacao AS O ON P.CNPJ_ORG = O.CNPJ_ORG
            WHERE NOT EXISTS (
                SELECT 1 FROM Candidatura C 
                WHERE C.ID_PROJETO = P.ID_PROJETO AND C.RGM_ALUNO = ?
            )
        """
        cursor.execute(sql_disponiveis, (rgm_aluno,))
        resultados = cursor.fetchall()

        if not resultados:
            print(f"\n{AMARELO}Não há novos projetos disponíveis para você no momento. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            return

        headers = [f"{BOLD}ID PROJETO{RESET}", f"{BOLD}TÍTULO{RESET}", f"{BOLD}ORGANIZAÇÃO{RESET}"]
        print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))

        # 2. Pergunta qual ID
        print(f"\n{AMARELO}A qual projeto você deseja se candidatar?{RESET}")
        id_projeto = input(f"{BOLD}Digite o ID do Projeto (ou 0 para cancelar): {RESET}")
        
        if id_projeto == '0':
            return
        if not id_projeto.isdigit():
            print(f"\n{VERMELHO}ID inválido. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            return
            
        # 3. Executa o INSERT na tabela Candidatura
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_insert = "INSERT INTO Candidatura (ID_PROJETO, RGM_ALUNO, DATA_CANDIDATURA) VALUES (?, ?, ?)"
        
        # Usamos um try/except interno para pegar IDs de projeto inválidos
        try:
            cursor.execute(sql_insert, (id_projeto, rgm_aluno, agora))
            conn.commit()
            print(f"\n{VERDE}Candidatura ao projeto ID {id_projeto} realizada com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
        except sqlite3.IntegrityError:
            # Isso acontece se o ID do projeto não existir (falha na Foreign Key)
            print(f"\n{VERMELHO}Erro: Projeto com ID {id_projeto} não foi encontrado. {EMOJI_ALERTA}{RESET}")

    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao se candidatar: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def ver_minhas_candidaturas(rgm_aluno):
    """(R) Lista os projetos aos quais o aluno logado se candidatou."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         MINHAS CANDIDATURAS             {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        
        # Busca os projetos (P) e a organização (O)
        # com base na tabela de Candidatura (C)
        sql = """
            SELECT 
                P.ID_PROJETO, 
                P.TITULO, 
                O.NOME_ORG AS ORGANIZACAO,
                C.DATA_CANDIDATURA
            FROM Projeto AS P
            JOIN Organizacao AS O ON P.CNPJ_ORG = O.CNPJ_ORG
            JOIN Candidatura AS C ON P.ID_PROJETO = C.ID_PROJETO
            WHERE C.RGM_ALUNO = ?
        """
        cursor.execute(sql, (rgm_aluno,))
        resultados = cursor.fetchall() 

        if not resultados:
            print(f"\n{AMARELO}Você ainda não se candidatou a nenhum projeto. {EMOJI_ALERTA}{RESET}")
        else:
            headers = [f"{BOLD}ID PROJETO{RESET}", 
                       f"{BOLD}TÍTULO{RESET}", 
                       f"{BOLD}ORGANIZAÇÃO{RESET}", 
                       f"{BOLD}DATA CANDIDATURA{RESET}"]
            
            print(tabulate(resultados, headers=headers, tablefmt="fancy_grid"))
            
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao listar suas candidaturas: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")