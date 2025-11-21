import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime
import db_manager as db

# Aplica o tema 'FLATLY'
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
app.title = "Ponte Acadêmica"

# --- (A) Componentes de Layout Persistentes ---

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/gabrielgustav-art/ponte-academica", target="_blank"))
    ],
    brand="Ponte Acadêmica",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4"
)

footer = html.Footer(
    dbc.Container(
        html.P("© 2025 Ponte Acadêmica. Todos os direitos reservados.", className="text-center text-muted mt-5 p-3")
    )
)

# --- (B) Definição dos Layouts (As "Páginas") ---

form_login_aluno = dbc.Form([
    dbc.Row([
        dbc.Label("RGM", width=3),
        dbc.Col(dbc.Input(id='login-rgm', type='text', placeholder='Digite seu RGM'), width=9)
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Senha", width=3),
        dbc.Col(dbc.Input(id='login-senha-aluno', type='password', placeholder='Digite sua senha'), width=9)
    ], className="mb-3"),
    dbc.Button('Entrar como Aluno', id='login-aluno-button', color="primary", className="w-100", n_clicks=0),
    html.Div(id='login-aluno-output', style={'color': 'red', 'margin': '10px 0'})
])

form_login_org = dbc.Form([
    dbc.Row([
        dbc.Label("CNPJ", width=3),
        dbc.Col(dbc.Input(id='login-cnpj', type='text', placeholder='Digite seu CNPJ (14 números)'), width=9)
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Senha", width=3),
        dbc.Col(dbc.Input(id='login-senha-org', type='password', placeholder='Digite sua senha'), width=9)
    ], className="mb-3"),
    dbc.Button('Entrar como Organização', id='login-org-button', color="primary", className="w-100", n_clicks=0),
    html.Div(id='login-org-output', style={'color': 'red', 'margin': '10px 0'})
])

form_cadastro_aluno = dbc.Form([
    dbc.Row([
        dbc.Label("RGM", width=3),
        dbc.Col(dbc.Input(id='cadastro-rgm', type='text', placeholder='RGM (apenas números)'), width=9)
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Nome", width=3),
        dbc.Col(dbc.Input(id='cadastro-nome-aluno', type='text', placeholder='Nome Completo'), width=9)
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Senha", width=3),
        dbc.Col(dbc.Input(id='cadastro-senha-aluno', type='password', placeholder='Senha (6-8 caracteres)'), width=9)
    ], className="mb-3"),
    dbc.Button('Cadastrar Aluno', id='cadastro-aluno-button', color="success", className="w-100", n_clicks=0),
    html.Div(id='cadastro-aluno-output', style={'margin': '10px 0'})
])

form_cadastro_org = dbc.Form([
    dbc.Row([
        dbc.Label("CNPJ", width=3),
        dbc.Col(dbc.Input(id='cadastro-cnpj', type='text', placeholder='CNPJ (14 números)'), width=9)
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Nome", width=3),
        dbc.Col(dbc.Input(id='cadastro-nome-org', type='text', placeholder='Nome da Organização'), width=9)
    ], className="mb-3"),
    dbc.Row([
        dbc.Label("Senha", width=3),
        dbc.Col(dbc.Input(id='cadastro-senha-org', type='password', placeholder='Senha (6-8 caracteres)'), width=9)
    ], className="mb-3"),
    dbc.Button('Cadastrar Organização', id='cadastro-org-button', color="success", className="w-100", n_clicks=0),
    html.Div(id='cadastro-org-output', style={'margin': '10px 0'})
])

layout_tab_login = html.Div([
    dbc.Tabs(id="tabs-tipo-login", active_tab='tab-aluno-login', children=[
        dbc.Tab(label='Login Aluno', tab_id='tab-aluno-login'),
        dbc.Tab(label='Login Organização', tab_id='tab-org-login'),
    ]),
    html.Div(id='tabs-login-content', style={'marginTop': '20px'})
])

layout_tab_cadastro = html.Div([
    dbc.Tabs(id="tabs-tipo-cadastro", active_tab='tab-aluno-cadastro', children=[
        dbc.Tab(label='Cadastro Aluno', tab_id='tab-aluno-cadastro'),
        dbc.Tab(label='Cadastro Organização', tab_id='tab-org-cadastro'),
    ]),
    html.Div(id='tabs-cadastro-content', style={'marginTop': '20px'})
])

layout_login_cadastro = dbc.Row(
    dbc.Col([
        html.H1("Ponte Acadêmica", className="text-center"),
        html.P("A plataforma de microprojetos", className="text-center text-muted mb-4"),
        dbc.Card([
            dbc.CardHeader(
                dbc.Tabs(id="tabs-login-cadastro", active_tab='tab-login', children=[
                    dbc.Tab(label='Login', tab_id='tab-login'),
                    dbc.Tab(label='Cadastrar', tab_id='tab-cadastro'),
                ])
            ),
            dbc.CardBody(
                html.Div(id='tabs-content', style={'padding': '20px'})
            )
        ])
    ], width=12, md=8, lg=6),
    justify="center",
    className="mt-5"
)

layout_painel_aluno = html.Div([
    dbc.Row([
        dbc.Col(html.H1('Painel do Aluno'), width=10),
        dbc.Col(dbc.Button('Logout', href='/logout', color="secondary"), width=2, style={'textAlign': 'right'})
    ], align="center"),
    html.Div(id='aluno-boas-vindas'),
    html.Hr(),
    dbc.Tabs(id="tabs-aluno", active_tab='tab-listar-projetos', children=[
        dbc.Tab(label='Listar Projetos Disponíveis', tab_id='tab-listar-projetos'),
        dbc.Tab(label='Me Candidatar', tab_id='tab-candidatar'),
        dbc.Tab(label='Minhas Candidaturas', tab_id='tab-minhas-candidaturas'),
    ]),
    html.Div(id='aluno-tabs-content', style={'marginTop': '20px'})
])

layout_painel_org = html.Div([
    dbc.Row([
        dbc.Col(html.H1('Painel da Organização'), width=10),
        dbc.Col(dbc.Button('Logout', href='/logout', color="secondary"), width=2, style={'textAlign': 'right'})
    ], align="center"),
    html.Div(id='org-boas-vindas'),
    html.Hr(),
    dbc.Tabs(id="tabs-org", active_tab='tab-listar-meus-projetos', children=[
        dbc.Tab(label='Listar Meus Projetos', tab_id='tab-listar-meus-projetos'),
        dbc.Tab(label='Cadastrar Projeto', tab_id='tab-cadastrar-projeto'),
        dbc.Tab(label='Atualizar Projeto', tab_id='tab-atualizar-projeto'),
        dbc.Tab(label='Excluir Projeto', tab_id='tab-excluir-projeto'),
        dbc.Tab(label='Relatórios', tab_id='tab-relatorio'),
    ]),
    html.Div(id='org-tabs-content', style={'marginTop': '20px'})
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-storage', storage_type='session'),
    navbar,
    dbc.Container(
        html.Div(id='page-content'),
        fluid=False,
        style={'maxWidth': '1200px', 'padding': '20px', 'minHeight': '70vh'}
    ),
    footer
])

# --- Callbacks (Interface) ---

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/painel-aluno':
        return layout_painel_aluno
    elif pathname == '/painel-org':
        return layout_painel_org
    elif pathname == '/logout':
        return layout_login_cadastro
    else:
        return layout_login_cadastro

@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs-login-cadastro', 'active_tab')
)
def render_login_cadastro_tabs(tab):
    if tab == 'tab-login':
        return layout_tab_login
    elif tab == 'tab-cadastro':
        return layout_tab_cadastro

@app.callback(
    Output('tabs-login-content', 'children'),
    Input('tabs-tipo-login', 'active_tab')
)
def render_login_forms(tab):
    if tab == 'tab-aluno-login':
        return form_login_aluno
    elif tab == 'tab-org-login':
        return form_login_org

@app.callback(
    Output('tabs-cadastro-content', 'children'),
    Input('tabs-tipo-cadastro', 'active_tab')
)
def render_cadastro_forms(tab):
    if tab == 'tab-aluno-cadastro':
        return form_cadastro_aluno
    elif tab == 'tab-org-cadastro':
        return form_cadastro_org

# --- Login / Cadastro callbacks ---

@app.callback(
    [Output('login-aluno-output', 'children'),
     Output('url', 'pathname', allow_duplicate=True),
     Output('session-storage', 'data')],
    [Input('login-aluno-button', 'n_clicks')],
    [State('login-rgm', 'value'),
     State('login-senha-aluno', 'value')],
    prevent_initial_call=True
)
def tentar_login_aluno(n_clicks, rgm, senha):
    if not rgm or not senha:
        return "Por favor, preencha o RGM e a Senha.", dash.no_update, dash.no_update
    nome_aluno = db.login_aluno_db(rgm, senha)
    if nome_aluno:
        session_data = {'tipo': 'aluno', 'id': rgm, 'nome': nome_aluno}
        return f"Login bem-sucedido! Bem-vindo, {nome_aluno}!", '/painel-aluno', session_data
    else:
        return "RGM ou Senha incorretos.", dash.no_update, dash.no_update

@app.callback(
    [Output('login-org-output', 'children'),
     Output('url', 'pathname', allow_duplicate=True),
     Output('session-storage', 'data', allow_duplicate=True)],
    [Input('login-org-button', 'n_clicks')],
    [State('login-cnpj', 'value'),
     State('login-senha-org', 'value')],
    prevent_initial_call=True
)
def tentar_login_org(n_clicks, cnpj, senha):
    if not cnpj or not senha:
        return "Por favor, preencha o CNPJ e a Senha.", dash.no_update, dash.no_update
    nome_org = db.login_organizacao_db(cnpj, senha)
    if nome_org:
        session_data = {'tipo': 'org', 'id': cnpj, 'nome': nome_org}
        return f"Login bem-sucedido! Bem-vinda, {nome_org}!", '/painel-org', session_data
    else:
        return "CNPJ ou Senha incorretos.", dash.no_update, dash.no_update

@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('session-storage', 'data', allow_duplicate=True)],
    [Input('url', 'pathname')],
    prevent_initial_call=True
)
def handle_logout(pathname):
    if pathname == '/logout':
        return '/', None
    return dash.no_update, dash.no_update

@app.callback(
    Output('cadastro-aluno-output', 'children'),
    [Input('cadastro-aluno-button', 'n_clicks')],
    [State('cadastro-rgm', 'value'),
     State('cadastro-nome-aluno', 'value'),
     State('cadastro-senha-aluno', 'value')],
    prevent_initial_call=True
)
def tentar_cadastro_aluno(n_clicks, rgm, nome, senha):
    if not rgm or not nome or not senha:
        return html.Div("Por favor, preencha todos os campos.", style={'color': 'red'})
    if not rgm.isdigit():
        return html.Div("Erro: O RGM deve conter apenas números.", style={'color': 'red'})
    if 6 > len(senha) or len(senha) > 8:
        return html.Div("Erro: A senha deve ter entre 6 e 8 caracteres.", style={'color': 'red'})
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, erro = db.cadastrar_aluno_db(rgm, nome, senha, agora)
    if sucesso:
        return html.Div(f"Aluno {nome} cadastrado com sucesso! Você já pode fazer o login.", style={'color': 'green'})
    else:
        return html.Div(f"Erro ao cadastrar: {erro}", style={'color': 'red'})

@app.callback(
    Output('cadastro-org-output', 'children'),
    [Input('cadastro-org-button', 'n_clicks')],
    [State('cadastro-cnpj', 'value'),
     State('cadastro-nome-org', 'value'),
     State('cadastro-senha-org', 'value')],
    prevent_initial_call=True
)
def tentar_cadastro_org(n_clicks, cnpj, nome, senha):
    if not cnpj or not nome or not senha:
        return html.Div("Por favor, preencha todos os campos.", style={'color': 'red'})
    if not cnpj.isdigit() or len(cnpj) != 14:
        return html.Div("Erro: O CNPJ deve ter exatamente 14 números.", style={'color': 'red'})
    if 6 > len(senha) or len(senha) > 8:
        return html.Div("Erro: A senha deve ter entre 6 e 8 caracteres.", style={'color': 'red'})
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, erro = db.cadastrar_organizacao_db(cnpj, nome, senha, agora)
    if sucesso:
        return html.Div(f"Organização {nome} cadastrada com sucesso! Você já pode fazer o login.", style={'color': 'green'})
    else:
        return html.Div(f"Erro ao cadastrar: {erro}", style={'color': 'red'})

# -----------------------------------------
# Dash tables helper
# -----------------------------------------
def criar_tabela_dash(id_tabela, dados_lista, colunas_lista):
    return dash_table.DataTable(
        id=id_tabela,
        columns=[{"name": i, "id": i} for i in colunas_lista],
        data=[dict(zip(colunas_lista, linha)) for linha in dados_lista],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        row_selectable='single',
        selected_rows=[],
    )

@app.callback(
    Output('aluno-boas-vindas', 'children'),
    Input('session-storage', 'data')
)
def preencher_boas_vindas_aluno(data):
    if data and data.get('tipo') == 'aluno':
        return html.H4(f"Bem-vindo(a), {data.get('nome')}! (RGM: {data.get('id')})")
    return "Não autenticado"

@app.callback(
    Output('org-boas-vindas', 'children'),
    Input('session-storage', 'data')
)
def preencher_boas_vindas_org(data):
    if data and data.get('tipo') == 'org':
        return html.H4(f"Bem-vinda, {data.get('nome')}! (CNPJ: {data.get('id')})")
    return "Não autenticado"

# -----------------------
# Org: abas e CRUD
# -----------------------
@app.callback(
    Output('org-tabs-content', 'children'),
    [Input('tabs-org', 'active_tab')],
    [State('session-storage', 'data')]
)
def render_org_tabs_content(tab, data):
    if not data or data.get('tipo') != 'org':
        return "Erro de autenticação."
    cnpj_org = data.get('id')
    if tab == 'tab-listar-meus-projetos':
        resultados, erro = db.listar_projetos_org_db(cnpj_org)
        if erro:
            return f"Erro ao buscar projetos: {erro}"
        if not resultados:
            return html.P("Você ainda não cadastrou nenhum projeto.")
        colunas = ["ID_PROJETO", "TITULO", "CANDIDATOS", "DATA_CRIACAO"]
        return html.Div([
            html.H3("Meus Projetos"),
            html.P("Selecione um projeto na tabela para ver detalhes, atualizar ou excluir."),
            criar_tabela_dash('tabela-org-projetos', resultados, colunas),
            html.Hr(),
            html.Div(id='detalhes-projeto-org')  # container para detalhes (callback popula)
        ])
    elif tab == 'tab-cadastrar-projeto':
        return html.Div([
            html.H3("Cadastrar Novo Projeto"),
            dbc.Input(id='proj-titulo', placeholder='Título do Projeto', className="mb-2"),
            dbc.Textarea(id='proj-desc', placeholder='Descrição (máx 350 palavras)', style={'height': 100}, className="mb-2"),
            dbc.Button('Salvar Projeto', id='salvar-projeto-button', color="primary"),
            html.Div(id='salvar-projeto-output', style={'marginTop': '10px'})
        ])
    elif tab == 'tab-relatorio':
        return html.Div([
            html.H3("Relatório de Pesquisa"),
            dbc.Select(
                id='relatorio-filtro',
                options=[
                    {'label': 'Filtrar por Título', 'value': '1'},
                    {'label': 'Filtrar por Status (Em Andamento)', 'value': '2'},
                    {'label': 'Filtrar por Status (Disponível)', 'value': '3'},
                ],
                placeholder="Selecione um filtro",
            ),
            dbc.Input(id='relatorio-termo', placeholder='Termo de busca (para Título)', className="my-2"),
            dbc.Button('Gerar Relatório', id='gerar-relatorio-button', color="info"),
            html.Div(id='relatorio-output', style={'marginTop': '20px'})
        ])
    elif tab == 'tab-atualizar-projeto':
        resultados, erro = db.listar_projetos_org_db(cnpj_org)
        tabela = []
        if erro:
            tabela = [html.P(f"Erro ao buscar projetos: {erro}", style={'color': 'red'})]
        elif not resultados:
            tabela = [html.P("Você ainda não cadastrou nenhum projeto.")]
        else:
            colunas = ["ID_PROJETO", "TITULO", "CANDIDATOS", "DATA_CRIACAO"]
            tabela = [criar_tabela_dash('tabela-org-projetos-update', resultados, colunas)]
        return html.Div([
            html.H3("Atualizar Projeto"),
            html.P("Selecione um projeto na tabela abaixo para carregar seus dados."),
            *tabela,
            html.Hr(),
            dbc.Input(id='update-id-projeto', placeholder='ID do Projeto (selecionado da lista)', disabled=True, className="mb-2"),
            dbc.Input(id='update-titulo', placeholder='Novo Título (deixe em branco para manter)', className="mb-2"),
            dbc.Textarea(id='update-desc', placeholder='Nova Descrição (máx 350 palavras)', style={'height': 100}, className="mb-2"),
            dbc.Button('Atualizar Projeto', id='atualizar-projeto-button', color="warning"),
            html.Div(id='atualizar-projeto-output', style={'marginTop': '10px'})
        ])
    elif tab == 'tab-excluir-projeto':
        resultados, erro = db.listar_projetos_org_db(cnpj_org)
        tabela = []
        if erro:
            tabela = [html.P(f"Erro ao buscar projetos: {erro}", style={'color': 'red'})]
        elif not resultados:
            tabela = [html.P("Você ainda não cadastrou nenhum projeto.")]
        else:
            colunas = ["ID_PROJETO", "TITULO", "CANDIDATOS", "DATA_CRIACAO"]
            tabela = [criar_tabela_dash('tabela-org-projetos-excluir', resultados, colunas)]
        return html.Div([
            html.H3("Excluir Projeto"),
            html.P("Selecione um projeto na tabela abaixo para carregar o ID."),
            *tabela,
            html.Hr(),
            dbc.Input(id='excluir-id-projeto', placeholder='ID do Projeto (selecionado da lista)', disabled=True, className="mb-2"),
            dbc.Button('EXCLUIR PROJETO', id='excluir-projeto-button', color="danger", n_clicks=0),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Confirmar Exclusão")),
                dbc.ModalBody("Tem certeza que deseja excluir este projeto e todas as suas candidaturas? Esta ação não pode ser desfeita."),
                dbc.ModalFooter([
                    dbc.Button("Cancelar", id="cancelar-excluir-btn", className="ms-auto", n_clicks=0),
                    dbc.Button("Confirmar Exclusão", id="confirmar-excluir-btn", color="danger", n_clicks=0)
                ])
            ], id="modal-excluir", is_open=False),
            html.Div(id='excluir-projeto-output', style={'marginTop': '10px'})
        ])
    return "Selecione uma aba."

# -----------------------------------------
# Aluno: abas e CRUD
# -----------------------------------------
@app.callback(
    Output('aluno-tabs-content', 'children'),
    [Input('tabs-aluno', 'active_tab')],
    [State('session-storage', 'data')]
)
def render_aluno_tabs_content(tab, data):
    if not data or data.get('tipo') != 'aluno':
        return "Erro de autenticação."
    rgm_aluno = data.get('id')
    if tab == 'tab-listar-projetos':
        resultados, erro = db.listar_projetos_disponiveis_db(rgm_aluno)
        if erro:
            return f"Erro ao buscar projetos: {erro}"
        if not resultados:
            return html.P("Não há projetos disponíveis no momento.")
        colunas = ["ID_PROJETO", "TITULO", "ORGANIZACAO", "DATA_CRIACAO"]
        return html.Div([
            html.H3("Projetos Disponíveis"),
            html.P("Selecione um projeto na tabela para ver seus detalhes."),
            criar_tabela_dash('tabela-aluno-disponiveis', resultados, colunas),
            html.Hr(),
            html.Div(id='detalhes-projeto-aluno')
        ])
    elif tab == 'tab-candidatar':
        resultados_cand, erro_cand = db.listar_projetos_disponiveis_db(rgm_aluno)
        tabela_cand = []
        if erro_cand:
            tabela_cand = [html.P(f"Erro ao buscar projetos: {erro_cand}", style={'color': 'red'})]
        elif not resultados_cand:
            tabela_cand = [html.P("Não há novos projetos disponíveis para você no momento.")]
        else:
            colunas_cand = ["ID_PROJETO", "TITULO", "ORGANIZACAO", "DATA_CRIACAO"]
            tabela_cand = [criar_tabela_dash('tabela-aluno-candidatar', resultados_cand, colunas_cand)]
        return html.Div([
            html.H3("Candidatar-se a um Projeto"),
            html.P("Selecione um projeto na tabela abaixo para carregar o ID."),
            *tabela_cand,
            html.Hr(),
            html.Div(id='detalhes-projeto-candidatar'),
            html.Hr(),
            dbc.Input(id='candidatar-id-projeto', placeholder='ID do Projeto (selecionado da lista)', disabled=True, className="mb-2"),
            dbc.Button('Confirmar Candidatura', id='candidatar-projeto-button', color="success"),
            html.Div(id='candidatar-projeto-output', style={'marginTop': '10px'})
        ])
    elif tab == 'tab-minhas-candidaturas':
        resultados, erro = db.ver_minhas_candidaturas_db(rgm_aluno)
        if erro:
            return f"Erro ao buscar suas candidaturas: {erro}"
        if not resultados:
            return html.P("Você ainda não se candidatou a nenhum projeto.")
        colunas = ["ID_PROJETO", "TITULO", "ORGANIZACAO", "DATA_CANDIDATURA"]
        return html.Div([
            html.H3("Minhas Candidaturas"),
            html.P("Selecione um projeto para ver detalhes, conversar ou remover sua candidatura."),
            criar_tabela_dash('tabela-aluno-candidaturas', resultados, colunas),
            html.Hr(),
            html.Div(id='detalhes-minha-candidatura'),
            html.Hr(),
            dbc.Input(id='remover-id-projeto', placeholder='ID do Projeto (selecionado da lista)', disabled=True, className="mb-2"),
            dbc.Button('Remover Candidatura', id='remover-candidatura-button', color="danger", n_clicks=0),
            html.Div(id='remover-candidatura-output', style={'marginTop': '10px'})
        ])
    return "Selecione uma aba."

# -----------------------------------------
# Operações de Projeto (Org)
# -----------------------------------------
@app.callback(
    Output('salvar-projeto-output', 'children'),
    [Input('salvar-projeto-button', 'n_clicks')],
    [State('proj-titulo', 'value'),
     State('proj-desc', 'value'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def salvar_novo_projeto(n_clicks, titulo, descricao, data):
    if not data or data.get('tipo') != 'org':
        return "Erro de autenticação."
    cnpj_org = data.get('id')
    if not titulo or not descricao:
        return html.Div("Título e Descrição são obrigatórios.", style={'color': 'red'})
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, erro = db.cadastrar_projeto_db(titulo, descricao, cnpj_org, agora, agora)
    if sucesso:
        return html.Div(f"Projeto '{titulo}' cadastrado com sucesso!", style={'color': 'green'})
    else:
        return html.Div(f"Erro ao salvar projeto: {erro}", style={'color': 'red'})

@app.callback(
    Output('update-id-projeto', 'value'),
    Input('tabela-org-projetos-update', 'selected_rows'),
    State('tabela-org-projetos-update', 'data'),
    prevent_initial_call=True
)
def preencher_id_update(selected_rows, data):
    if not selected_rows:
        return ""
    id_projeto = data[selected_rows[0]]["ID_PROJETO"]
    return str(id_projeto)

@app.callback(
    Output('excluir-id-projeto', 'value'),
    Input('tabela-org-projetos-excluir', 'selected_rows'),
    State('tabela-org-projetos-excluir', 'data'),
    prevent_initial_call=True
)
def preencher_id_excluir(selected_rows, data):
    if not selected_rows:
        return ""
    id_projeto = data[selected_rows[0]]["ID_PROJETO"]
    return str(id_projeto)

# -----------------------------
# Mostrar detalhes (Org) + chat
# -----------------------------
@app.callback(
    Output('detalhes-projeto-org', 'children'),
    Input('tabela-org-projetos', 'selected_rows'),
    [State('tabela-org-projetos', 'data'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def mostrar_detalhes_org_lista(selected_rows, data_tabela, session_data):
    if not selected_rows or not session_data or session_data.get('tipo') != 'org':
        return ""
    try:
        id_projeto = data_tabela[selected_rows[0]]["ID_PROJETO"]
    except Exception:
        return dbc.Alert("Erro ao obter o ID do projeto selecionado.", color="warning")
    cnpj_org = session_data.get('id')
    projeto, erro = db.get_projeto_detalhes_db(id_projeto, cnpj_org)
    if erro:
        return dbc.Alert(f"Erro ao buscar detalhes: {erro}", color="danger")
    if not projeto:
        return dbc.Alert("Projeto não encontrado.", color="warning")
    # projeto: (titulo, desc, data_criacao, ultima_atualizacao)
    titulo, desc, data_c, ultima = projeto

    candidatos, erro_cand = db.listar_candidatos_db(id_projeto)
    lista_candidatos = html.P("Nenhum candidato ainda.", className="text-muted")
    if candidatos:
        rows = [html.Tr([html.Td(c[0]), html.Td(c[1]), html.Td(c[2])]) for c in candidatos]
        lista_candidatos = dbc.Table([html.Thead(html.Tr([html.Th("RGM"), html.Th("Nome"), html.Th("Data da Candidatura")])), html.Tbody(rows)], bordered=True, striped=True, hover=True)

    # Mensagens existentes
    mensagens, err_m = db.listar_mensagens_db(id_projeto)
    mensagens_view = html.Div()
    if mensagens:
        msgs = []
        for r in mensagens:
            remet, id_rem, text, dataenv = r
            who = f"{remet.upper()} ({id_rem})"
            msgs.append(html.Div([
                html.Small(who, className="text-muted"),
                html.Div(text, style={'marginBottom': '10px'}),
                html.Small(dataenv, className="text-muted"),
                html.Hr()
            ]))
        mensagens_view = html.Div(msgs, style={'maxHeight': '240px', 'overflowY': 'auto', 'padding': '6px', 'backgroundColor': '#f8f9fa', 'borderRadius': '4px'})
    else:
        mensagens_view = html.P("Nenhuma mensagem ainda.", className="text-muted")

    # Card com detalhes + chat
    card = dbc.Card([
        dbc.CardHeader(f"Detalhes do Projeto ID: {id_projeto}"),
        dbc.CardBody([
            html.H5(titulo, className="card-title"),
            html.P(f"Data de Criação: {data_c}", className="card-text text-muted"),
            html.P(f"Última Atualização: {ultima}", className="card-text text-muted"),
            html.P(desc, className="card-text"),
            html.Hr(),
            html.H6("Candidatos:"),
            lista_candidatos,
            html.Hr(),
            html.H6("Mensagens (Chat com candidatos):"),
            dcc.Store(id='chat-proj-org', data={'id_projeto': id_projeto}),  # armazena id do projeto para callbacks
            html.Div(id='mensagens-lista-org', children=mensagens_view),
            dbc.Row([
                dbc.Col(dbc.Input(id='mensagem-input-org', placeholder='Escreva uma mensagem...'), width=9),
                dbc.Col(dbc.Button('Enviar', id='enviar-mensagem-org', color='primary'), width=3)
            ], className="mt-2"),
            html.Div(id='enviar-mensagem-org-output', style={'marginTop': '6px'})
        ])
    ], className="mt-4")
    return card

# callback para enviar mensagem (ORG)
@app.callback(
    [Output('mensagens-lista-org', 'children'),
     Output('mensagem-input-org', 'value'),
     Output('enviar-mensagem-org-output', 'children')],
    [Input('enviar-mensagem-org', 'n_clicks')],
    [State('mensagem-input-org', 'value'),
     State('chat-proj-org', 'data'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def enviar_mensagem_org(n_clicks, mensagem, chat_data, session_data):
    if not session_data or session_data.get('tipo') != 'org':
        return dash.no_update, dash.no_update, "Erro de autenticação."
    if not mensagem or not chat_data:
        return dash.no_update, dash.no_update, html.Div("Digite uma mensagem.", style={'color': 'red'})
    id_projeto = chat_data.get('id_projeto')
    cnpj = session_data.get('id')
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, err = db.enviar_mensagem_db(id_projeto, 'org', cnpj, mensagem, agora)
    if not sucesso:
        return dash.no_update, dash.no_update, html.Div(f"Erro ao enviar: {err}", style={'color': 'red'})
    # rebuild mensagem view
    mensagens, err_m = db.listar_mensagens_db(id_projeto)
    msgs = []
    for r in mensagens:
        remet, id_rem, text, dataenv = r
        who = f"{remet.upper()} ({id_rem})"
        msgs.append(html.Div([html.Small(who, className="text-muted"), html.Div(text, style={'marginBottom': '10px'}), html.Small(dataenv, className="text-muted"), html.Hr()]))
    view = html.Div(msgs, style={'maxHeight': '240px', 'overflowY': 'auto', 'padding': '6px', 'backgroundColor': '#f8f9fa', 'borderRadius': '4px'})
    return view, "", html.Div("Mensagem enviada.", style={'color': 'green'})

# -----------------------------------------
# Atualizar projeto (org)
# -----------------------------------------
@app.callback(
    Output('atualizar-projeto-output', 'children'),
    [Input('atualizar-projeto-button', 'n_clicks')],
    [State('update-id-projeto', 'value'),
     State('update-titulo', 'value'),
     State('update-desc', 'value'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def tentar_atualizar_projeto(n_clicks, id_projeto, novo_titulo, nova_descricao, data):
    if not data or data.get('tipo') != 'org':
        return "Erro de autenticação."
    if not id_projeto:
        return html.Div("Por favor, selecione um projeto na lista acima primeiro.", style={'color': 'red'})
    cnpj_org = data.get('id')
    sucesso, erro = db.atualizar_projeto_db(novo_titulo, nova_descricao, id_projeto, cnpj_org)
    if sucesso:
        return html.Div(f"Projeto ID {id_projeto} atualizado com sucesso!", style={'color': 'green'})
    else:
        return html.Div(f"Erro ao atualizar: {erro}", style={'color': 'red'})

# -----------------------------------------
# Excluir / Modal
# -----------------------------------------
@app.callback(
    [Output('modal-excluir', 'is_open'),
     Output('excluir-projeto-output', 'children')],
    [Input('excluir-projeto-button', 'n_clicks'),
     Input('confirmar-excluir-btn', 'n_clicks'),
     Input('cancelar-excluir-btn', 'n_clicks')],
    [State('excluir-id-projeto', 'value'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def gerenciar_modal_excluir(n_excluir, n_confirmar, n_cancelar, id_projeto, data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, ""
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'excluir-projeto-button':
        if not id_projeto:
            return False, html.Div("Por favor, selecione um projeto na lista acima primeiro.", style={'color': 'red'})
        return True, ""
    if button_id == 'cancelar-excluir-btn':
        return False, ""
    if button_id == 'confirmar-excluir-btn':
        if not data or data.get('tipo') != 'org':
            return False, "Erro de autenticação."
        if not id_projeto:
            return False, html.Div("ID do projeto se perdeu. Tente novamente.", style={'color': 'red'})
        cnpj_org = data.get('id')
        sucesso, erro = db.excluir_projeto_db(id_projeto, cnpj_org)
        if sucesso:
            return False, html.Div(f"Projeto ID {id_projeto} e suas candidaturas foram excluídos!", style={'color': 'green'})
        else:
            return False, html.Div(f"Erro ao excluir: {erro}", style={'color': 'red'})
    return False, ""

@app.callback(
    Output('relatorio-output', 'children'),
    [Input('gerar-relatorio-button', 'n_clicks')],
    [State('relatorio-filtro', 'value'),
     State('relatorio-termo', 'value'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def gerar_relatorio_org(n_clicks, filtro, termo, data):
    if not data or data.get('tipo') != 'org':
        return "Erro de autenticação."
    if not filtro:
        return "Por favor, selecione um tipo de filtro."
    cnpj_org = data.get('id')
    resultados, erro = db.relatorio_pesquisa_db(cnpj_org, filtro, termo)
    if erro:
        return f"Erro ao gerar relatório: {erro}"
    if not resultados:
        return "Nenhum projeto encontrado com este filtro."
    colunas = ["ID_PROJETO", "TITULO", "CANDIDATOS", "DATA_CRIACAO"]
    return [
        html.H4(f"Total de Projetos Encontrados: {len(resultados)}"),
        criar_tabela_dash('tabela-relatorio', resultados, colunas)
    ]

# -----------------------------------------
# Aluno: detalhes / candidaturas / chat
# -----------------------------------------
def criar_card_detalhes_projeto_publico(id_projeto):
    projeto, erro = db.get_projeto_detalhes_publico_db(id_projeto)
    if erro:
        return dbc.Alert(f"Erro ao buscar detalhes: {erro}", color="danger")
    if not projeto:
        return dbc.Alert("Projeto não encontrado.", color="warning")
    try:
        titulo, desc, nome_org, data_c, ultima = projeto
    except Exception:
        titulo = projeto[0] if len(projeto) > 0 else "—"
        desc = projeto[1] if len(projeto) > 1 else ""
        nome_org = projeto[2] if len(projeto) > 2 else ""
        data_c = projeto[3] if len(projeto) > 3 else ""
        ultima = projeto[4] if len(projeto) > 4 else ""
    return dbc.Card([
        dbc.CardHeader(f"Detalhes do Projeto ID: {id_projeto}"),
        dbc.CardBody([
            html.H5(titulo, className="card-title"),
            html.H6(f"Organização: {nome_org}", className="card-subtitle"),
            html.P(f"Data de Criação: {data_c}", className="card-text text-muted"),
            html.P(f"Última Atualização: {ultima}", className="card-text text-muted"),
            html.Hr(),
            html.P(desc, className="card-text"),
        ])
    ], className="mt-4")

@app.callback(
    Output('detalhes-projeto-aluno', 'children'),
    Input('tabela-aluno-disponiveis', 'selected_rows'),
    State('tabela-aluno-disponiveis', 'data'),
    prevent_initial_call=True
)
def mostrar_detalhes_aluno_disponiveis(selected_rows, data):
    if not selected_rows:
        return ""
    id_projeto = data[selected_rows[0]]["ID_PROJETO"]
    return criar_card_detalhes_projeto_publico(id_projeto)

@app.callback(
    [Output('candidatar-id-projeto', 'value'),
     Output('detalhes-projeto-candidatar', 'children')],
    Input('tabela-aluno-candidatar', 'selected_rows'),
    State('tabela-aluno-candidatar', 'data'),
    prevent_initial_call=True
)
def preencher_id_candidatura(selected_rows, data):
    if not selected_rows:
        return "", ""
    id_projeto = data[selected_rows[0]]["ID_PROJETO"]
    card_detalhes = criar_card_detalhes_projeto_publico(id_projeto)
    return str(id_projeto), card_detalhes

@app.callback(
    Output('candidatar-projeto-output', 'children'),
    [Input('candidatar-projeto-button', 'n_clicks')],
    [State('candidatar-id-projeto', 'value'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def tentar_candidatura(n_clicks, id_projeto, data):
    if not data or data.get('tipo') != 'aluno':
        return "Erro de autenticação."
    if not id_projeto:
        return html.Div("Por favor, selecione um projeto na lista acima primeiro.", style={'color': 'red'})
    rgm_aluno = data.get('id')
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, erro = db.candidatar_a_projeto_db(id_projeto, rgm_aluno, agora)
    if sucesso:
        return html.Div(f"Candidatura ao projeto ID {id_projeto} realizada com sucesso!", style={'color': 'green'})
    else:
        return html.Div(f"Erro ao se candidatar: {erro}", style={'color': 'red'})

# Quando aluno seleciona uma candidatura: mostra detalhes + chat para conversar com org
@app.callback(
    [Output('detalhes-minha-candidatura', 'children'),
     Output('remover-id-projeto', 'value')],
    Input('tabela-aluno-candidaturas', 'selected_rows'),
    State('tabela-aluno-candidaturas', 'data'),
    State('session-storage', 'data'),
    prevent_initial_call=True
)
def mostrar_detalhes_minhas_candidaturas(selected_rows, data, session_data):
    if not selected_rows:
        return "", ""
    id_projeto = data[selected_rows[0]]["ID_PROJETO"]
    # card com detalhes publicos
    card = criar_card_detalhes_projeto_publico(id_projeto)
    # mensagens
    mensagens, err_m = db.listar_mensagens_db(id_projeto)
    mensagens_view = html.P("Nenhuma mensagem ainda.", className="text-muted")
    if mensagens:
        msgs = []
        for r in mensagens:
            remet, id_rem, text, dataenv = r
            who = f"{remet.upper()} ({id_rem})"
            msgs.append(html.Div([html.Small(who, className="text-muted"), html.Div(text, style={'marginBottom': '10px'}), html.Small(dataenv, className="text-muted"), html.Hr()]))
        mensagens_view = html.Div(msgs, style={'maxHeight': '240px', 'overflowY': 'auto', 'padding': '6px', 'backgroundColor': '#f8f9fa', 'borderRadius': '4px'})
    # montagem final com chat
    chat_block = html.Div([
        dcc.Store(id='chat-proj-aluno', data={'id_projeto': id_projeto}),
        html.H6("Mensagens (Chat com a organização):"),
        html.Div(id='mensagens-lista-aluno', children=mensagens_view),
        dbc.Row([
            dbc.Col(dbc.Input(id='mensagem-input-aluno', placeholder='Escreva uma mensagem...'), width=9),
            dbc.Col(dbc.Button('Enviar', id='enviar-mensagem-aluno', color='primary'), width=3)
        ], className="mt-2"),
        html.Div(id='enviar-mensagem-aluno-output', style={'marginTop': '6px'})
    ])
    return html.Div([card, html.Hr(), chat_block]), str(id_projeto)

# callback para enviar mensagem (ALUNO)
@app.callback(
    [Output('mensagens-lista-aluno', 'children'),
     Output('mensagem-input-aluno', 'value'),
     Output('enviar-mensagem-aluno-output', 'children')],
    [Input('enviar-mensagem-aluno', 'n_clicks')],
    [State('mensagem-input-aluno', 'value'),
     State('chat-proj-aluno', 'data'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def enviar_mensagem_aluno(n_clicks, mensagem, chat_data, session_data):
    if not session_data or session_data.get('tipo') != 'aluno':
        return dash.no_update, dash.no_update, "Erro de autenticação."
    if not mensagem or not chat_data:
        return dash.no_update, dash.no_update, html.Div("Digite uma mensagem.", style={'color': 'red'})
    id_projeto = chat_data.get('id_projeto')
    rgm = session_data.get('id')
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sucesso, err = db.enviar_mensagem_db(id_projeto, 'aluno', rgm, mensagem, agora)
    if not sucesso:
        return dash.no_update, dash.no_update, html.Div(f"Erro ao enviar: {err}", style={'color': 'red'})
    mensagens, err_m = db.listar_mensagens_db(id_projeto)
    msgs = []
    for r in mensagens:
        remet, id_rem, text, dataenv = r
        who = f"{remet.upper()} ({id_rem})"
        msgs.append(html.Div([html.Small(who, className="text-muted"), html.Div(text, style={'marginBottom': '10px'}), html.Small(dataenv, className="text-muted"), html.Hr()]))
    view = html.Div(msgs, style={'maxHeight': '240px', 'overflowY': 'auto', 'padding': '6px', 'backgroundColor': '#f8f9fa', 'borderRadius': '4px'})
    return view, "", html.Div("Mensagem enviada.", style={'color': 'green'})

@app.callback(
    Output('remover-candidatura-output', 'children'),
    Input('remover-candidatura-button', 'n_clicks'),
    [State('remover-id-projeto', 'value'),
     State('session-storage', 'data')],
    prevent_initial_call=True
)
def tentar_remover_candidatura(n_clicks, id_projeto, data):
    if not data or data.get('tipo') != 'aluno':
        return "Erro de autenticação."
    if not id_projeto:
        return html.Div("Por favor, selecione um projeto na lista acima primeiro.", style={'color': 'red'})
    rgm_aluno = data.get('id')
    sucesso, erro = db.remover_candidatura_db(id_projeto, rgm_aluno)
    if sucesso:
        return html.Div(f"Candidatura ao projeto ID {id_projeto} removida com sucesso!", style={'color': 'green'})
    else:
        return html.Div(f"Erro ao remover: {erro}", style={'color': 'red'})

# --- Roda o servidor ---
if __name__ == '__main__':
    app.run(debug=True)
