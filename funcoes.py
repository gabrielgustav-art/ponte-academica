import os
import sqlite3  # Para conectar ao banco de dados
import time
import getpass  # Para pedir a senha de forma segura

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

# --- (A) Funções de CADASTRO (Já tínhamos) ---

def cadastrar_aluno():
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

    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Aluno (RGM_ALUNO, NOME_ALUNO, SENHA) VALUES (?, ?, ?)"
        cursor.execute(sql_insert, (rgm, nome, senha)) 
        conn.commit() 
        print(f"\n{VERDE}Aluno {nome} cadastrado com sucesso! {EMOJI_SUCESSO}{RESET}")
    except sqlite3.Error as e: 
        print(f"\n{VERMELHO}Erro ao cadastrar aluno: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close() 
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def cadastrar_organizacao():
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}      CADASTRAR NOVA ORGANIZAÇÃO         {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    while True:
        cnpj = input(f"{BOLD}Digite o CNPJ (apenas números): {RESET}")
        if not cnpj.isdigit(): 
            print(f"{VERMELHO}Erro: O CNPJ deve conter apenas números. {EMOJI_ALERTA}{RESET}")
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

    conn = None 
    try:
        conn = sqlite3.connect('tabela.db') 
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Organizacao (CNPJ_ORG, NOME_ORG, SENHA) VALUES (?, ?, ?)"
        cursor.execute(sql_insert, (cnpj, nome, senha)) 
        conn.commit() 
        print(f"\n{VERDE}Organização {nome} cadastrada com sucesso! {EMOJI_SUCESSO}{RESET}")
    except sqlite3.Error as e: 
        print(f"\n{VERMELHO}Erro ao cadastrar organização: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close() 
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def realizar_cadastro():
    """Exibe o menu de cadastro e chama a função correta."""
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
    else:
        print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
        input(f"{AZUL}Digite enter para voltar ao menu{RESET}")

# --- (B) Funções de LOGIN (Novas) ---

def login_aluno():
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}           LOGIN DE ALUNO                {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    rgm = input(f"{BOLD}Digite seu RGM: {RESET}")
    senha = getpass.getpass(f"{BOLD}Digite sua senha: {RESET}")
    
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        # Procura no banco um RGM E Senha que batam
        sql_select = "SELECT NOME_ALUNO FROM Aluno WHERE RGM_ALUNO = ? AND SENHA = ?"
        cursor.execute(sql_select, (rgm, senha))
        
        resultado = cursor.fetchone() # Pega o primeiro resultado (ou None)
        
        if resultado:
            nome_aluno = resultado[0] # Pega o nome (que está na posição 0 do resultado)
            print(f"\n{VERDE}Login bem-sucedido! Bem-vindo(a), {nome_aluno}! {EMOJI_SUCESSO}{RESET}")
            time.sleep(2)
            menu_aluno(nome_aluno) # Entra no menu interno do aluno
        else:
            print(f"\n{VERMELHO}RGM ou Senha incorretos. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao fazer login: {e} {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
    finally:
        if conn:
            conn.close()

def login_organizacao():
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         LOGIN DA ORGANIZAÇÃO            {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    cnpj = input(f"{BOLD}Digite seu CNPJ: {RESET}")
    senha = getpass.getpass(f"{BOLD}Digite sua senha: {RESET}")
    
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
            menu_organizacao(nome_org) # Entra no menu interno da organização
        else:
            print(f"\n{VERMELHO}CNPJ ou Senha incorretos. {EMOJI_ALERTA}{RESET}")
            input(f"\n{AZUL}Digite enter para voltar...{RESET}")
            
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao fazer login: {e} {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
    finally:
        if conn:
            conn.close()

def realizar_login():
    """Exibe o menu de login e chama a função correta."""
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
    else:
        print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
        input(f"{AZUL}Digite enter para voltar...{RESET}")

# --- (C) Funções dos MENUS INTERNOS (Depois do Login) ---

def menu_aluno(nome_aluno):
    """Menu que o aluno vê após logar."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}           PAINEL DO ALUNO               {RESET}")
        print(f"Bem-vindo(a), {nome_aluno}!")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        print(f"{CIANO}1 - Listar Projetos Disponíveis{RESET}")
        print(f"{CIANO}2 - Me candidatar a um Projeto{RESET}")
        print(f"{CIANO}3 - Ver minhas candidaturas{RESET}")
        print(f"{VERMELHO}0 - Logout (Sair){RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        opt = input(f"{BOLD}Escolha uma opção: {RESET}")
        
        if opt == '1':
            print("Função LISTAR PROJETOS não implementada.")
            input(f"{AZUL}Digite enter para voltar...{RESET}")
        elif opt == '2':
            print("Função CANDIDATAR não implementada.")
            input(f"{AZUL}Digite enter para voltar...{RESET}")
        elif opt == '3':
            print("Função VER CANDIDATURAS não implementada.")
            input(f"{AZUL}Digite enter para voltar...{RESET}")
        elif opt == '0':
            print(f"Fazendo logout, até logo {nome_aluno}!")
            time.sleep(2)
            break # Quebra o loop do 'menu_aluno' e volta para o 'main.py'
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar...{RESET}")

def menu_organizacao(nome_org):
    """Menu que a organização vê após logar."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}         PAINEL DA ORGANIZAÇÃO           {RESET}")
        print(f"Bem-vinda, {nome_org}!")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        # Estas opções vêm do seu documento original!
        print(f"{CIANO}1 - Cadastrar Novo Projeto{RESET}")
        print(f"{CIANO}2 - Listar Meus Projetos{RESET}")
        print(f"{CIANO}3 - Atualizar Projeto{RESET}")
        print(f"{CIANO}4 - Excluir Projeto{RESET}")
        print(f"{VERMELHO}0 - Logout (Sair){RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        opt = input(f"{BOLD}Escolha uma opção: {RESET}")
        
        if opt == '1':
            cadastrar_projeto(nome_org) # Chama a função de cadastrar projeto
        elif opt == '2':
            print("Função LISTAR PROJETOS não implementada.")
            input(f"{AZUL}Digite enter para voltar...{RESET}")
        elif opt == '3':
            print("Função ATUALIZAR PROJETO não implementada.")
            input(f"{AZUL}Digite enter para voltar...{RESET}")
        elif opt == '4':
            print("Função EXCLUIR PROJETO não implementada.")
            input(f"{AZUL}Digite enter para voltar...{RESET}")
        elif opt == '0':
            print(f"Fazendo logout, até logo {nome_org}!")
            time.sleep(2)
            break # Quebra o loop do 'menu_organizacao' e volta para o 'main.py'
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar...{RESET}")

def cadastrar_projeto(nome_org):
    """Função para a organização logada cadastrar um projeto."""
    # (Esta é uma função 'placeholder' para o menu interno)
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}       CADASTRAR NOVO PROJETO            {RESET}")
    print(f"Organização: {nome_org}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    titulo = input(f"{BOLD}Digite o Título do projeto: {RESET}")
    descricao = input(f"{BOLD}Digite a Descrição do projeto: {RESET}")
    
    # Aqui iria o código 'INSERT INTO Projeto ...'
    
    print(f"\n{VERDE}Projeto '{titulo}' cadastrado com sucesso! {EMOJI_SUCESSO}{RESET}")
    print(f"{AMARELO}NOTA: A conexão com o banco de dados ainda não foi implementada aqui.{RESET}")
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")