import os
import funcoes as fc  # <-- MUDANÇA 1: Imports no topo
import time

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


# --- Loop Principal (igual ao Crud_Dict_V0.py) ---
while True:
    limpar_tela()

    # 2. Mostra o novo menu de entrada
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}      BEM-VINDO À PONTE ACADÊMICA      {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    time.sleep(1)

    print(f"{CIANO}1 - Login{RESET}")
    print(f"{CIANO}2 - Cadastrar{RESET}")
    print(f"{VERMELHO}0 - Sair{RESET}")

    print(f"{BOLD}{AZUL}========================================={RESET}")

    # 3. Captura a opção
    opt = input(f"{BOLD}Entre com a opção desejada: {RESET}")

    limpar_tela()

    if opt == "1":
        # fc.Login_Func() # (Função de fazer login)
        print("Login: ")
        input(f"{AZUL}Digite enter para voltar ao menu{RESET}")

    elif opt == "2":
        # <-- MUDANÇA 2: Chamamos a função do outro arquivo
        fc.realizar_cadastro()

    elif opt == "0":
        print(f"Saindo do sistema... {EMOJI_SUCESSO}")
        break

    else:
        print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
        input(f"{AZUL}Digite enter para voltar ao menu{RESET}")