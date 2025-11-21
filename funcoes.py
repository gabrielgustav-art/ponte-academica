import os
#import sqlite3
import time
import getpass
from datetime import datetime
from rich.console import Console
from rich.table import Table

import db_manager as db 

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

# Inicializa o console do rich
console = Console()

def limpar_tela():
    """Limpa o console, funciona em Windows, Mac e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Funções Auxiliares de Validação (Console) ---

def is_alpha_space(s):
    """Verifica se a string contém apenas letras e espaços."""
    if not s:
        return False
    return all(c.isalpha() or c.isspace() for c in s)

# --- (A) Funções de CADASTRO (Console) ---

def cadastrar_aluno():
    """Coleta dados e chama o DB para cadastrar um novo aluno."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}        CADASTRAR NOVO ALUNO             {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    while True:
        rgm = input(f"{BOLD}Digite o RGM (apenas números): {RESET}")
        if not rgm.isdigit(): 
            print(f"{VERMELHO}Erro: O RGM deve conter apenas números. {EMOJI_ALERTA}{RESET}")
            continue
        if db.checar_se_existe_db('Aluno', 'RGM_ALUNO', rgm): 
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
    sucesso, erro = db.cadastrar_aluno_db(rgm, nome, senha, agora)
    
    if sucesso:
        print(f"\n{VERDE}Aluno {nome} cadastrado com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    else:
        print(f"\n{VERMELHO}Erro ao cadastrar aluno: {erro} {EMOJI_ALERTA}{RESET}")
        
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def cadastrar_organizacao():
    """Coleta dados e chama o DB para cadastrar uma nova organização."""
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
        if db.checar_se_existe_db('Organizacao', 'CNPJ_ORG', cnpj): 
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
    sucesso, erro = db.cadastrar_organizacao_db(cnpj, nome, senha, agora)

    if sucesso:
        print(f"\n{VERDE}Organização {nome} cadastrada com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    else:
        print(f"\n{VERMELHO}Erro ao cadastrar organização: {erro} {EMOJI_ALERTA}{RESET}")

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

# --- (B) Funções de LOGIN (Console) ---

def login_aluno():
    """Coleta dados e chama o DB para validar o login do aluno."""
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
        
        if not db.checar_se_existe_db('Aluno', 'RGM_ALUNO', rgm):
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
            
        nome_aluno = db.login_aluno_db(rgm, senha)
            
        if nome_aluno:
            print(f"\n{VERDE}Login bem-sucedido! Bem-vindo(a), {nome_aluno}! {EMOJI_SUCESSO}{RESET}")
            time.sleep(2)
            menu_aluno(rgm, nome_aluno)
            return 
        else:
            print(f"\n{VERMELHO}Senha incorreta. {EMOJI_ALERTA}{RESET}")
                
    login_aluno() 

def login_organizacao():
    """Coleta dados e chama o DB para validar o login da organização."""
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
        
        if not db.checar_se_existe_db('Organizacao', 'CNPJ_ORG', cnpj):
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
        
        nome_org = db.login_organizacao_db(cnpj, senha)
            
        if nome_org:
            print(f"\n{VERDE}Login bem-sucedido! Bem-vinda, {nome_org}! {EMOJI_SUCESSO}{RESET}")
            time.sleep(2)
            menu_organizacao(cnpj, nome_org) 
            return 
        else:
            print(f"\n{VERMELHO}Senha incorreta. {EMOJI_ALERTA}{RESET}")

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
        
        print(f"{CIANO}1 - Listar Projetos Disponíveis (Ver Descrição){RESET}")
        print(f"{CIANO}2 - Me candidatar a um Projeto{RESET}")
        print(f"{CIANO}3 - Ver minhas candidaturas (Remover){RESET}")
        print(f"{VERMELHO}0 - Logout (Sair){RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        opt = input(f"{BOLD}Escolha uma opção: {RESET}")
        
        if opt == '1':
            listar_projetos_disponiveis(rgm_aluno)
        elif opt == '2':
            candidatar_a_projeto(rgm_aluno)
        elif opt == '3':
            ver_minhas_candidaturas(rgm_aluno)
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
        print(f"{CIANO}5 - Relatório de Pesquisa{RESET}")
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
        elif opt == '5':
            relatorio_pesquisa(cnpj_org, nome_org)
        elif opt == '0':
            print(f"Fazendo logout, até logo {nome_org}!")
            time.sleep(2)
            break 
        else:
            print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
            input(f"{AZUL}Digite enter para voltar ao menu{RESET}")

def cadastrar_projeto(cnpj_org, nome_org):
    """(C) Coleta dados e chama o DB para cadastrar um projeto."""
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
        descricao = input(f"{BOLD}Digite a Descrição do projeto (máx 350 palavras): {RESET}")
        if not descricao.strip():
            print(f"{VERMELHO}Erro: A Descrição não pode ser vazia. {EMOJI_ALERTA}{RESET}")
            continue
        
        contagem_palavras = len(descricao.split()) 
        
        if contagem_palavras > 350:
            print(f"{VERMELHO}Erro: A Descrição ultrapassou 350 palavras. (Atual: {contagem_palavras}) {EMOJI_ALERTA}{RESET}")
            continue
        break

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, erro = db.cadastrar_projeto_db(titulo, descricao, cnpj_org, agora)

    if sucesso:
        print(f"\n{VERDE}Projeto '{titulo}' cadastrado com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    else:
        print(f"\n{VERMELHO}Erro ao cadastrar projeto: {erro} {EMOJI_ALERTA}{RESET}")
    
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

# --- (D) Funções de CRUD da Organização (R, U, D) ---

def _criar_tabela_rich(titulo_tabela):
    """Cria um objeto Table base do Rich."""
    return Table(
        title=titulo_tabela,
        title_style="bold cyan",
        border_style="bright_blue",
        show_lines=True,
        header_style="bold blue"
    )

def _mostrar_projetos_org(cnpj_org):
    """Função auxiliar que busca e exibe a tabela de projetos."""
    resultados, erro = db.listar_projetos_org_db(cnpj_org)
    
    if erro:
        print(f"\n{VERMELHO}Erro ao buscar projetos: {erro} {EMOJI_ALERTA}{RESET}")
        return False
    if not resultados:
        print(f"\n{AMARELO}Você ainda não cadastrou nenhum projeto. {EMOJI_ALERTA}{RESET}")
        return False 
    
    table = _criar_tabela_rich("")
    table.add_column("ID PROJETO", justify="center")
    table.add_column("TÍTULO", justify="left")
    table.add_column("Nº DE CANDIDATOS", justify="center")
    table.add_column("DATA CRIAÇÃO", justify="left")
    
    for linha in resultados:
        table.add_row(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3]))
        
    console.print(table)
    return True 

def _mostrar_detalhes_projeto_org(id_projeto, cnpj_org):
    """Mostra os detalhes completos de um projeto e a lista de candidatos."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}       DETALHES DO PROJETO ID {id_projeto}        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    projeto, erro_proj = db.get_projeto_detalhes_db(id_projeto, cnpj_org)
    
    if erro_proj:
        print(f"\n{VERMELHO}Erro ao buscar projeto: {erro_proj} {EMOJI_ALERTA}{RESET}")
        return
    if not projeto:
        print(f"\n{VERMELHO}Projeto ID {id_projeto} não encontrado ou não pertence à sua organização. {EMOJI_ALERTA}{RESET}")
        return

    titulo, desc, data_c = projeto
    print(f"\n{BOLD}ID:{RESET}         {id_projeto}")
    print(f"{BOLD}Título:{RESET}     {titulo}")
    print(f"{BOLD}Data Criação:{RESET} {data_c}")
    print(f"\n{BOLD}Descrição Completa:{RESET}\n {desc}")
    print(f"\n{BOLD}{AZUL}--- CANDIDATOS ---{RESET}")

    candidatos, erro_cand = db.listar_candidatos_db(id_projeto)

    if erro_cand:
        print(f"\n{VERMELHO}Erro ao buscar candidatos: {erro_cand} {EMOJI_ALERTA}{RESET}")
    elif not candidatos:
        print(f"{AMARELO}Este projeto ainda não tem candidatos.{RESET}")
    else:
        table = _criar_tabela_rich("")
        table.add_column("RGM ALUNO", justify="center")
        table.add_column("NOME", justify="left")
        table.add_column("DATA CANDIDATURA", justify="left")
        
        for linha in candidatos:
            table.add_row(str(linha[0]), str(linha[1]), str(linha[2]))
        
        console.print(table)
        
    print(f"\n{BOLD}{AZUL}========================================={RESET}")


def listar_meus_projetos(cnpj_org, nome_org):
    """(R) Lista projetos e permite ver detalhes de um ID específico."""
    while True: 
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}          MEUS PROJETOS ({nome_org})        {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")

        if not _mostrar_projetos_org(cnpj_org):
            break 

        print(f"\n{CIANO}--- Opções ---{RESET}")
        id_proj = input(f"{BOLD}Digite o ID do projeto para ver detalhes (ou 0 para voltar): {RESET}")

        if id_proj == '0':
            break 
        
        if not id_proj.isdigit():
            print(f"\n{VERMELHO}ID inválido. Deve ser um número. {EMOJI_ALERTA}{RESET}")
            time.sleep(2)
            continue 

        _mostrar_detalhes_projeto_org(id_proj, cnpj_org)
        input(f"\n{AZUL}Pressione Enter para voltar à lista de projetos...{RESET}")
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")


def atualizar_projeto(cnpj_org, nome_org):
    """(U) Atualiza o título e a descrição de um projeto (FLUXO MELHORADO)."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}       ATUALIZAR PROJETO ({nome_org})        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    if not _mostrar_projetos_org(cnpj_org):
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
    
    projeto_atual, erro = db.get_projeto_detalhes_db(id_projeto, cnpj_org)

    if erro:
        print(f"\n{VERMELHO}Erro ao buscar projeto: {erro} {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        return
    if not projeto_atual:
        print(f"\n{VERMELHO}Nenhum projeto encontrado com este ID ou você não tem permissão. {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        return
        
    titulo_atual, desc_atual = projeto_atual
    
    print(f"\n{CIANO}--- DADOS ATUAIS (ID: {id_projeto}) ---{RESET}")
    print(f"{CIANO}Título Atual: {titulo_atual}{RESET}")
    print(f"{CIANO}Descrição Atual: {desc_atual}{RESET}")
    print(f"{CIANO}--------------------------------------{RESET}")
    
    print(f"\n{CIANO}Deixe em branco para manter a informação atual.{RESET}")
    novo_titulo = input(f"{BOLD}Novo Título: {RESET}")
    
    while True:
        nova_descricao = input(f"{BOLD}Nova Descrição (máx 350 palavras): {RESET}")
        
        if not nova_descricao.strip():
            break 
        
        contagem_palavras = len(nova_descricao.split())
        
        if contagem_palavras > 350:
            print(f"{VERMELHO}Erro: A Descrição ultrapassou 350 palavras. (Atual: {contagem_palavras}) {EMOJI_ALERTA}{RESET}")
            continue
        
        break 
    
    sucesso, erro = db.atualizar_projeto_db(novo_titulo, nova_descricao, id_projeto, cnpj_org)

    if sucesso:
        print(f"\n{VERDE}Projeto ID {id_projeto} atualizado com sucesso! {EMOJI_SUCESSO}{RESET}")
    else:
        print(f"\n{VERMELHO}Erro ao atualizar projeto: {erro} {EMOJI_ALERTA}{RESET}")
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def excluir_projeto(cnpj_org, nome_org):
    """(D) Exclui um projeto E SUAS CANDIDATURAS."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         EXCLUIR PROJETO ({nome_org})        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    if not _mostrar_projetos_org(cnpj_org):
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
        sucesso, erro = db.excluir_projeto_db(id_projeto, cnpj_org)
        
        if sucesso:
            print(f"\n{VERDE}Projeto ID {id_projeto} e todas as suas candidaturas foram excluídos! {EMOJI_SUCESSO}{RESET}")
        else:
            print(f"\n{VERMELHO}Erro ao excluir projeto: {erro} {EMOJI_ALERTA}{RESET}")
    else:
        print(f"\n{CIANO}Exclusão cancelada.{RESET}")
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

# --- (E) Funções de CRUD do Aluno ---

def _mostrar_detalhes_projeto_aluno(id_projeto):
    """Mostra os detalhes públicos de um projeto para o aluno."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}       DETALHES DO PROJETO ID {id_projeto}        {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    projeto, erro = db.get_projeto_detalhes_publico_db(id_projeto)
    
    if erro:
        print(f"\n{VERMELHO}Erro ao buscar projeto: {erro} {EMOJI_ALERTA}{RESET}")
        return
    if not projeto:
        print(f"\n{VERMELHO}Projeto ID {id_projeto} não encontrado. {EMOJI_ALERTA}{RESET}")
        return

    titulo, desc, nome_org, data_c = projeto
    print(f"\n{BOLD}ID:{RESET}           {id_projeto}")
    print(f"{BOLD}Título:{RESET}       {titulo}")
    print(f"{BOLD}Organização:{RESET}  {nome_org}")
    print(f"{BOLD}Data Criação:{RESET}   {data_c}")
    print(f"\n{BOLD}Descrição Completa:{RESET}\n {desc}")
    print(f"\n{BOLD}{AZUL}========================================={RESET}")

def listar_projetos_disponiveis(rgm_aluno):
    """(R) Lista todos os projetos e permite ver detalhes."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}        PROJETOS DISPONÍVEIS             {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        resultados, erro = db.listar_projetos_disponiveis_db(rgm_aluno) 

        if erro:
            print(f"\n{VERMELHO}Erro ao listar projetos: {erro} {EMOJI_ALERTA}{RESET}")
            break
        if not resultados:
            print(f"\n{AMARELO}Não há novos projetos disponíveis para você no momento. {EMOJI_ALERTA}{RESET}")
            break
        
        table = _criar_tabela_rich("")
        table.add_column("ID PROJETO", justify="center")
        table.add_column("TÍTULO", justify="left")
        table.add_column("ORGANIZAÇÃO", justify="left")
        table.add_column("DATA CRIAÇÃO", justify="left")

        for linha in resultados:
            table.add_row(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3]))
        
        console.print(table)
        
        print(f"\n{CIANO}--- Opções ---{RESET}")
        id_proj = input(f"{BOLD}Digite o ID do projeto para ver detalhes (ou 0 para voltar): {RESET}")

        if id_proj == '0':
            break 
        
        if not id_proj.isdigit():
            print(f"\n{VERMELHO}ID inválido. Deve ser um número. {EMOJI_ALERTA}{RESET}")
            time.sleep(2)
            continue 

        _mostrar_detalhes_projeto_aluno(id_proj)
        input(f"\n{AZUL}Pressione Enter para voltar à lista de projetos...{RESET}")
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def candidatar_a_projeto(rgm_aluno):
    """(C) Permite ao aluno se candidatar (INSERT) a um projeto."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}      CANDIDATAR-SE A UM PROJETO         {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    resultados, erro = db.listar_projetos_disponiveis_db(rgm_aluno)

    if erro:
        print(f"\n{VERMELHO}Erro ao buscar projetos: {erro} {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        return
    if not resultados:
        print(f"\n{AMARELO}Não há novos projetos disponíveis para você no momento. {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        return

    table = _criar_tabela_rich("")
    table.add_column("ID PROJETO", justify="center")
    table.add_column("TÍTULO", justify="left")
    table.add_column("ORGANIZAÇÃO", justify="left")

    for linha in resultados:
        table.add_row(str(linha[0]), str(linha[1]), str(linha[2]))
        
    console.print(table)

    print(f"\n{AMARELO}A qual projeto você deseja se candidatar?{RESET}")
    id_projeto = input(f"{BOLD}Digite o ID do Projeto (ou 0 para cancelar): {RESET}")
    
    if id_projeto == '0':
        return
    if not id_projeto.isdigit():
        print(f"\n{VERMELHO}ID inválido. {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        return
        
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sucesso, erro = db.candidatar_a_projeto_db(id_projeto, rgm_aluno, agora)
    
    if sucesso:
        print(f"\n{VERDE}Candidatura ao projeto ID {id_projeto} realizada com sucesso em {agora}! {EMOJI_SUCESSO}{RESET}")
    else:
        print(f"\n{VERMELHO}Erro ao se candidatar: {erro} {EMOJI_ALERTA}{RESET}")
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

def ver_minhas_candidaturas(rgm_aluno):
    """(R) Lista os projetos aos quais o aluno logado se candidatou."""
    while True:
        limpar_tela()
        print(f"{BOLD}{AZUL}========================================={RESET}")
        print(f"{BOLD}{AZUL}        MINHAS CANDIDATURAS              {RESET}")
        print(f"{BOLD}{AZUL}========================================={RESET}")
        
        resultados, erro = db.ver_minhas_candidaturas_db(rgm_aluno) 

        if erro:
            print(f"\n{VERMELHO}Erro ao listar suas candidaturas: {erro} {EMOJI_ALERTA}{RESET}")
            break
        if not resultados:
            print(f"\n{AMARELO}Você ainda não se candidatou a nenhum projeto. {EMOJI_ALERTA}{RESET}")
            break
        
        table = _criar_tabela_rich("")
        table.add_column("ID PROJETO", justify="center")
        table.add_column("TÍTULO", justify="left")
        table.add_column("ORGANIZAÇÃO", justify="left")
        table.add_column("DATA CANDIDATURA", justify="left")

        for linha in resultados:
            table.add_row(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3]))
        
        console.print(table)
        
        print(f"\n{CIANO}--- Opções ---{RESET}")
        id_proj = input(f"{BOLD}Digite o ID do projeto para REMOVER A CANDIDATURA (ou 0 para voltar): {RESET}")

        if id_proj == '0':
            break 
        
        if not id_proj.isdigit():
            print(f"\n{VERMELHO}ID inválido. Deve ser um número. {EMOJI_ALERTA}{RESET}")
            time.sleep(2)
            continue 

        confirmacao = input(f"\n{AMARELO}Tem certeza que deseja remover sua candidatura do projeto ID {id_proj}? {VERMELHO}{BOLD}(S/N): {RESET}").upper()
        
        if confirmacao == 'S':
            sucesso, erro_del = db.remover_candidatura_db(id_proj, rgm_aluno)
            if sucesso:
                print(f"\n{VERDE}Candidatura ao projeto ID {id_proj} removida com sucesso! {EMOJI_SUCESSO}{RESET}")
                time.sleep(2)
            else:
                print(f"\n{VERMELHO}Erro ao remover: {erro_del} {EMOJI_ALERTA}{RESET}")
                time.sleep(2)
        else:
            print(f"\n{CIANO}Remoção cancelada.{RESET}")
            time.sleep(1)
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")

# --- (F) Função de Relatório (Console) ---

def relatorio_pesquisa(cnpj_org, nome_org):
    """(R) Gera relatórios filtrados, como pedido no documento de trabalho."""
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}         RELATÓRIO DE PESQUISA           {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{CIANO}1 - Filtrar por Título (Busca Parcial){RESET}")
    print(f"{CIANO}2 - Filtrar por Status (Em Andamento){RESET}")
    print(f"{CIANO}3 - Filtrar por Status (Disponível){RESET}")
    print(f"{VERMELHO}0 - Voltar ao menu anterior{RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")
    
    filtro = input(f"{BOLD}Escolha o tipo de relatório: {RESET}")
    termo = None
    
    if filtro == '1':
        termo = input(f"{BOLD}Digite parte do título para buscar: {RESET}")
    elif filtro in ('2', '3'):
        pass 
    elif filtro == '0':
        return
    else:
        print(f"{VERMELHO}Opção inválida! {EMOJI_ALERTA}{RESET}")
        input(f"\n{AZUL}Digite enter para voltar...{RESET}")
        return

    resultados, erro = db.relatorio_pesquisa_db(cnpj_org, filtro, termo)
    
    limpar_tela()
    print(f"{BOLD}{AZUL}========================================={RESET}")
    print(f"{BOLD}{AZUL}            RESULTADO DO RELATÓRIO         {RESET}")
    print(f"{BOLD}{AZUL}========================================={RESET}")

    if erro:
        print(f"\n{VERMELHO}Erro ao gerar relatório: {erro} {EMOJI_ALERTA}{RESET}")
    else:
        print(f"\n{BOLD}{CIANO}Total de Projetos Encontrados: {len(resultados)}{RESET}\n")
        if not resultados:
            print(f"\n{AMARELO}Nenhum projeto encontrado com este filtro. {EMOJI_ALERTA}{RESET}")
        else:
            table = _criar_tabela_rich("")
            table.add_column("ID PROJETO", justify="center")
            table.add_column("TÍTULO", justify="left")
            table.add_column("Nº DE CANDIDATOS", justify="center")
            table.add_column("DATA CRIAÇÃO", justify="left")

            for linha in resultados:
                table.add_row(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3]))
            
            console.print(table)
            
    input(f"\n{AZUL}Digite enter para voltar...{RESET}")