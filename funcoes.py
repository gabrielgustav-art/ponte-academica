import os
import sqlite3  # Para conectar ao banco de dados
import time
import getpass  # Para pedir a senha de forma segura

# --- Tabela de Cores (Códigos ANSI) ---
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
CIANO = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'
EMOJI_SUCESSO = "✅"
EMOJI_ALERTA = "⚠️"


# --- Fim da Tabela ---

def limpar_tela():
    """Limpa o console, funciona em Windows, Mac e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')


# --- Funções Auxiliares de Validação ---

def is_alpha_space(s):
    """Verifica se a string contém apenas letras e espaços."""
    # Retorna Falso se a string estiver vazia ou tiver algo que não seja letra/espaço
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
        # Usamos f-string de forma segura, pois os nomes da tabela e coluna vêm de nós,
        # e não do usuário. O valor do usuário é passado com '?'
        sql = f"SELECT 1 FROM {tabela} WHERE {coluna} = ?"
        cursor.execute(sql, (valor,))
        if cursor.fetchone():  # Se encontrar algo, fetchone() não será Nulo
            existe = True
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao checar dados: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
    return existe


# --- Função de Cadastro de Aluno ---
def cadastrar_aluno():
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}        CADASTRAR NOVO ALUNO             {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")

    # 1. Pedir e Validar o RGM
    while True:
        rgm = input(f"{BOLD}Digite o RGM (apenas números): {RESET}")
        if not rgm.isdigit():  # Regra 1: Apenas números
            print(f"{VERMELHO}Erro: O RGM deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            continue
        if checar_se_existe('Aluno', 'RGM_ALUNO', rgm):  # Regra 2: Único
            print(f"{VERMELHO}Erro: Este RGM já está cadastrado. {EMOJI_ALERTA}{RESET}")
            continue
        break  # Se passou nas duas checagens, sai do loop

    # 2. Pedir e Validar o Nome
    while True:
        nome = input(f"{BOLD}Digite o Nome Completo: {RESET}")
        if is_alpha_space(nome):  # Regra: Apenas letras e espaços
            break
        else:
            print(f"{VERMELHO}Erro: O Nome deve conter apenas letras e espaços. {EMOJI_ALERTA}{RESET}")

    # 3. Pedir e Validar a Senha
    while True:
        # Usa getpass para ocultar a senha
        senha = getpass.getpass(f"{BOLD}Digite uma senha (6 a 8 caracteres): {RESET}")
        if 6 <= len(senha) <= 8:  # Regra: Tamanho
            break
        else:
            print(f"{VERMELHO}Erro: A senha deve ter entre 6 e 8 caracteres. {EMOJI_ALERTA}{RESET}")

    # 4. Conectar e Salvar
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Aluno (RGM_ALUNO, NOME_ALUNO, SENHA) VALUES (?, ?, ?)"
        cursor.execute(sql_insert, (rgm, nome, senha))  # Envia os 3 valores
        conn.commit()
        print(f"\n{VERDE}Aluno {nome} cadastrado com sucesso! {EMOJI_SUCESSO}{RESET}")
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao cadastrar aluno: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")


# --- Função de Cadastro de Organização ---
def cadastrar_organizacao():
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}      CADASTRAR NOVA ORGANIZAÇÃO         {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")

    # 1. Pedir e Validar o CNPJ
    while True:
        cnpj = input(f"{BOLD}Digite o CNPJ (apenas números): {RESET}")
        if not cnpj.isdigit():  # Regra 1: Apenas números
            print(f"{VERMELHO}Erro: O CNPJ deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            continue
        if checar_se_existe('Organizacao', 'CNPJ_ORG', cnpj):  # Regra 2: Único
            print(f"{VERMELHO}Erro: Este CNPJ já está cadastrado. {EMOJI_ALERTA}{RESET}")
            continue
        break

        # 2. Pedir e Validar o Nome
    while True:
        nome = input(f"{BOLD}Digite o Nome da Organização: {RESET}")
        if is_alpha_space(nome):  # Regra: Apenas letras e espaços
            break
        else:
            print(f"{VERMELHO}Erro: O Nome deve conter apenas letras e espaços. {EMOJI_ALERTA}{RESET}")

    # 3. Pedir e Validar a Senha
    while True:
        senha = getpass.getpass(f"{BOLD}Digite uma senha (6 a 8 caracteres): {RESET}")
        if 6 <= len(senha) <= 8:  # Regra: Tamanho
            break
        else:
            print(f"{VERMELHO}Erro: A senha deve ter entre 6 e 8 caracteres. {EMOJI_ALERTA}{RESET}")

    # 4. Conectar e Salvar
    conn = None
    try:
        conn = sqlite3.connect('tabela.db')
        cursor = conn.cursor()
        sql_insert = "INSERT INTO Organizacao (CNPJ_ORG, NOME_ORG, SENHA) VALUES (?, ?, ?)"
        cursor.execute(sql_insert, (cnpj, nome, senha))  # Envia os 3 valores
        conn.commit()
        print(f"\n{VERDE}Organização {nome} cadastrada com sucesso! {EMOJI_SUCESSO}{RESET}")
    except sqlite3.Error as e:
        print(f"\n{VERMELHO}Erro ao cadastrar organização: {e} {EMOJI_ALERTA}{RESET}")
    finally:
        if conn:
            conn.close()
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")


# --- Função de Menu de Cadastro ---
def realizar_cadastro():
    """Exibe o menu de cadastro e chama a função correta."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         PORTAL DE CADASTRO              {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{CIANO}1 - Cadastrar como Aluno{RESET}")
    print(f"{CIANO}2 - Cadastrar como Organização{RESET}")  # <-- Agora funciona
    print(f"{VERMELHO}0 - Voltar ao menu anterior{RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")

    tipo = input(f"{BOLD}Escolha uma opção: {RESET}")

    if tipo == '1':
        cadastrar_aluno()
    elif tipo == '2':
        cadastrar_organizacao()  # <-- Chama a nova função de cadastro
    elif tipo == '0':
        print("Voltando ao menu principal...")
        time.sleep(1)
    else:
        print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
        input(f"{AZUL}Digite enter para voltar ao menu{RESET}")