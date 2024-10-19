from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime, date
import pandas as pd
from flask import session
from app.dash_app import *
from app.components.api.my_budget_api import *
from time import sleep

# ========= Layout ========= #

def render_layout(user_info: dict, cat_receitas: list, cat_despesas: list):

    cat_receita = cat_receitas['nome'].tolist()
    cat_despesa = cat_despesas['nome'].tolist()
    
    username = user_info.get('username', '')
    email = user_info.get('email', '')
    nome_completo = user_info.get('full_name')
    
    layout = dbc.Col([
        
        # Seção Logo
        dcc.Link(html.Img(src='assets/img/myBudget-logo.png', className='imagem-classe', style={'text-align': 'center'}), href='/home'),
        
        # Separador
        html.Hr(), 
        
        # Seção imagem de perfil
        dbc.Row([
            html.Img(src='assets/img/img_hom.png', id="avatar_change", alt="Avatar", className='perfil_avatar')
        ]),
        
        # Seção de upload de imagem de perfil
        html.Div([
            dcc.Upload(
                id='upload-image',
                children=html.Div([
                    html.A('Alterar imagem')
                ]),
                style={
                    "textAlign": "center",
                    "text-decoration": "underline",
                    "margin-bottom": "15px"
                },
                multiple=False
            ),
        ]),
        
        # Informações do usuário
        dbc.Row([
            dbc.Col([
                html.Strong("Nome", style={"margin-left": "15px"}), 
                html.P(nome_completo, style={"margin-left": "15px"})
            ], width=12),
            
            dbc.Col([
                html.Strong("E-mail", style={"margin-left": "15px"}), 
                html.P(email, style={"margin-left": "15px"})
            ], width=12),
                    
            dbc.Col([
                html.Strong("Username", style={"margin-left": "15px"}), 
                html.P(username, style={"margin-left": "15px"}, id="username-value", **{"data-username": username})
            ], width=12),
            
            html.Div([
                html.A('Sair', id="logout-btn", href="#")
                ], style={"text-align": "left", "margin-left": "15px"})
        ]),
        
        # Separador
        html.Hr(),
        
        # Seção de Navegação
        dbc.Nav([
            dbc.NavLink("Dashboard", href="/dashboard", active="exact"),
            dbc.NavLink("Extratos de Receitas", href="/extratos-receitas", active="exact"),
            dbc.NavLink("Extratos de Despesas", href="/extratos-despesas", active="exact"),
            ], vertical=True, pills=True, id='nav_buttons'),
        
        # Separador
        html.Hr(),
        
        # Seção Lançamento de Receitas/Despesas
        dbc.Row([
            dbc.Col([dbc.Button(color='success', id='open-novo-receita', children=['+ Receita'])], width=6, className='d-flex justify-content-center'),
            dbc.Col([dbc.Button(color='danger', id='open-novo-despesa', children=['- Despesa'])], width=6, className='d-flex justify-content-center')
            ]),
        
        # Modal Receita
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Adicionar receita')),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição'),
                        dbc.Input(placeholder='Ex.: Salário, Rendimentos, etc...', id='txt-receita'),
                        ], width=6),
                    dbc.Col([
                        dbc.Label('Valor: '),
                        dbc.Input(placeholder='R$100,00', id='valor_receita', value='')
                        ], width=6)
                    ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data: "),
                        dcc.DatePickerSingle(id='date-receitas',
                                            min_date_allowed=date(2020, 1, 1),
                                            max_date_allowed=date(2030, 12, 31),
                                            date=datetime.datetime.today(),
                                            style={"width": "100%"}
                                            ),
                        ], width=4),
                    
                    dbc.Col([
                        dbc.Label("Extras"),
                        dbc.Checklist(
                            options=[
                                {"label": "Foi recebida", "value": 1},
                                {"label": "Receita Recorrente", "value": 2}],
                            value=[1],
                            id="switches-input-receita",
                            switch=True),
                        ], width=4),
                    
                    dbc.Col([
                        html.Label("Categoria da receita"),
                        dbc.Select(id="select_receita", options=[{'label': i, 'value': i} for i in cat_receita], value=cat_receita[0])
                        ], width=4)
                    
                    ], style={"margin-top": "25px"}),
                
                # Accordion de categorias receitas
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend("Adicionar categoria", style={'color': 'green'}),
                                    
                                    dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
                                    
                                    dbc.Button("Adicionar", className="btn btn-success", id="add-category-receita", style={"margin-top": "20px"}),
                                    
                                    html.Br(),
                                    
                                    html.Div(id="category-div-add-receita"),
                                    ], width=6),
                                
                                dbc.Col([
                                    html.Legend("Excluir categorias", style={'color': 'red'}),
                                    
                                    dbc.Checklist(
                                        id="checklist-selected-style-receita",
                                        options=[{"label": i, "value": i} for i in cat_receita],
                                        value=[],
                                        label_checked_style={"color": "red"},
                                        input_checked_style={"backgroundColor": "#fa7268", "borderColor": "#ea6258"},
                                        ),
                                    
                                    dbc.Button("Remover", color="warning", id="remove-category-receita", style={"margin-top": "20px"}),
                                    ], width=6)
                                ]),
                            ], title="Adicionar/Remover Categorias"),
                        ], flush=True, start_collapsed=True, id='accordion-receita'),
                    
                    html.Div(id="id_teste_receita", style={"padding-top": "20px"}),
                    dbc.ModalFooter([
                        dbc.Button("Adicionar Receita", id="salvar_receita", color="success"),
                        dbc.Popover(dbc.PopoverBody("Receita Salva!"), id="popover_enviar_receita", target="salvar_receita", placement="left", trigger="click"),
                        ])
                    ], style={"margin-top": "25px"}),  
                ])
            ],
                id='modal-novo-receita',
                style={"background-color": "rgba(17, 140, 79, 0.05)"},
                size='lg',
                is_open=False,
                centered=True,
                backdrop=True
                ),
        
        # Modal Despesa
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição'),
                        dbc.Input(placeholder='Ex.: Contas de água/luz, cartão de crédito, supermercado, etc...', id='txt-despesa'),
                        ], width=6),
                    
                    dbc.Col([
                        dbc.Label('Valor: '),
                        dbc.Input(placeholder='R$100,00', id='valor_despesa', value='')
                        ], width=6)
                    ]),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data: "),
                        dcc.DatePickerSingle(id='date-despesas',
                                            min_date_allowed=date(2020, 1, 1),
                                            max_date_allowed=date(2030, 12, 31),
                                            date=datetime.datetime.today(),
                                            style={"width": "100%"}
                                            ),
                        ], width=4),
                    
                    dbc.Col([
                        dbc.Label("Extras"),
                        dbc.Checklist(
                            options=[{"label": "Foi recebida", "value": 1}, {"label": "Despesa Recorrente", "value": 2}],
                            value=[1],
                            id="switches-input-despesa",
                            switch=True),
                        
                        ], width=4),
                    
                    dbc.Col([
                        html.Label("Categoria da despesa"),
                        dbc.Select(id="select_despesa", options=[{'label': i, 'value': i} for i in cat_despesa], value=cat_despesa[0])
                        ], width=4)
                    
                    ], style={"margin-top": "25px"}),
                
                # Accordion de categorias despesas
                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                            dbc.Row([
                                dbc.Col([
                                    html.Legend("Adicionar categoria", style={'color': 'green'}),
                                    dbc.Input(type="text", placeholder="Nova categoria...", id="input-add-despesa", value=""),
                                    html.Br(),
                                    dbc.Button("Adicionar", className="btn btn-success", id="add-category-despesa", style={"margin-top": "20px"}),
                                    html.Br(),
                                    html.Div(id="category-div-add-despesa", style={}),
                                    ], width=6),
                                
                                dbc.Col([
                                    html.Legend("Excluir categorias", style={'color': 'red'}),
                                    dbc.Checklist(
                                        id="checklist-selected-style-despesa",
                                        options=[{"label": i, "value": i} for i in cat_despesa],
                                        value=[],
                                        label_checked_style={"color": "red"},
                                        input_checked_style={"backgroundColor": "#fa7268", "borderColor": "#ea6258"},
                                        ),
                                    
                                    dbc.Button("Remover", color="warning", id="remove-category-despesa", style={"margin-top": "20px"}),
                                    ], width=6)
                                ]),
                            
                            ], title="Adicionar/Remover Categorias"),
                        
                        ], flush=True, start_collapsed=True, id='accordion-despesa'),
                    
                    html.Div(id="id_teste_despesa", style={"padding-top": "20px"}),
                    dbc.ModalFooter([
                        dbc.Button("Adicionar Despesa", id="salvar_despesa", color="success"),
                        dbc.Popover(dbc.PopoverBody("Despesa Salva!"), id="popover_enviar_despesa", target="salvar_despesa", placement="left", trigger="click"),
                        ])
                    ], style={"margin-top": "25px"}),
                ])
            ],
                id='modal-novo-despesa',
                style={"background-color": "rgba(17, 140, 79, 0.05)"},
                size='lg',
                is_open=False,
                centered=True,
                backdrop=True
                ),
        
        # Separador
        html.Hr(),
             
    ], id='sidebar_completa')
    
    return layout

# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output("modal-novo-receita", "is_open"),
    Input("open-novo-receita", "n_clicks"),
    State("modal-novo-receita", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Pop-up despesa
@app.callback(
    Output("modal-novo-despesa", "is_open"),
    Input("open-novo-despesa", "n_clicks"),
    State("modal-novo-despesa", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Enviar Form receita
@app.callback(
    [
        Output('store-receitas', 'data'),
        Output("txt-receita", "value"),
        Output("valor_receita", "value"),
        Output("popover_enviar_receita", "is_open")
    ],
    
    Input("salvar_receita", "n_clicks"),

    [
        State("txt-receita", "value"),
        State("valor_receita", "value"),
        State("date-receitas", "date"),
        State("switches-input-receita", "value"),
        State("select_receita", "value"),
        State("login-state", "data"),
        State('store-receitas', 'data')
    ]
)
def save_form_receita(n, descricao, valor, data, switches, categoria, login_state, receitas):
    
    # user_info = session.get(username)
    token = login_state.get('token', None)
    
    df_receitas = pd.DataFrame(receitas)
    
    if n and not(valor == "" or valor == None):
        valor = round(float(valor), 2)
        data = pd.to_datetime(data)
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0
        
        PostReceive(
            token,
            valor,
            recebido,
            fixo,
            data.isoformat(),
            categoria,
            descricao
        )
        
        new_row = {
            'valor': valor,
            'recebido': recebido,
            'fixo': fixo,
            'data': data.strftime('%Y-%m-%d'),
            'categoria': categoria,
            'descricao': descricao
        }
    
        df_receitas.loc[len(df_receitas)] = new_row
        
        sleep(1)
        
        return df_receitas.to_dict(), '', '', False
    
    else:
        return df_receitas.to_dict(), '', '', False

# Enviar Form despesa
@app.callback(
    [
        Output('store-despesas', 'data'),
        Output("txt-despesa", "value"),
        Output("valor_despesa", "value"),
        Output("popover_enviar_despesa", "is_open")
    ],

    Input("salvar_despesa", "n_clicks"),

    [
        State("txt-despesa", "value"),
        State("valor_despesa", "value"),
        State("date-despesas", "date"),
        State("switches-input-despesa", "value"),
        State("select_despesa", "value"),
        State("login-state", "data"),
        State('store-despesas', 'data')
    ]
)
def save_form_despesa(n, descricao, valor, data, switches, categoria, login_state, despesas):
    
    # user_info = session.get(login_state['session_id'])
    token = login_state.get('token', None)
    
    df_despesas = pd.DataFrame(despesas)

    if n and not(valor == "" or valor == None):
        valor = round(float(valor), 2)
        data = pd.to_datetime(data)
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 0 if 2 in switches else 0
        
        PostExpense(
            token,
            valor,
            recebido,
            fixo,
            data.isoformat(),
            categoria,
            descricao
        )
        
        new_row = {
            'valor': valor,
            'recebido': recebido,
            'fixo': fixo,
            'data': data.strftime('%Y-%m-%d'),
            'categoria': categoria,
            'descricao': descricao
        }
        
        df_despesas.loc[len(df_despesas)] = new_row
        
        sleep(1)
        
        return df_despesas.to_dict(), '', '', False
    
    else:
        return df_despesas.to_dict(), '', '', False
    
# Adicionar/excluir categorias Receitas
@app.callback(
    [
        Output('select_receita', 'options'),
        Output('checklist-selected-style-receita', 'options'),
        Output('checklist-selected-style-receita', 'value'),
        Output('stored-cat-receitas', 'data'),
        Output('input-add-receita', 'value')
        
    ],
    
    [
        Input('add-category-receita', 'n_clicks'),
        Input('remove-category-receita', 'n_clicks')
    ],
    
    [
        State('input-add-receita', 'value'),
        State('checklist-selected-style-receita', 'value'),
        State('stored-cat-receitas', 'data'),
        State("login-state", "data")
    ]
)
def dropdown_category_receita(n, n2, nome_categoria, check_delete, cat_receitas, login_state):
    
    # user_info = session.get(login_state['session_id'])
    token = login_state.get('token', None)
    
    cat_receita = list(cat_receitas['nome'].values())
    
    if n and not (nome_categoria == '' or nome_categoria == None):
        if nome_categoria not in cat_receita:
            PostCategory(token, nome_categoria, 'receita')
            cat_receita.append(nome_categoria)
    
    if n2 and check_delete:
        for categoria in check_delete:
            if categoria in cat_receita:
                DeleteCategory(token, categoria, 'receita')
                cat_receita.remove(categoria)
                
    #Atualizando opções para os componentes de saída    
    opt_receita = [{'label': i, 'value': i} for i in cat_receita]
    
    df_cat_receita = pd.DataFrame(cat_receita, columns=['nome'])
    
    data_return = df_cat_receita.to_dict()
    
    return [opt_receita, opt_receita, [], data_return, '']

# Adicionar/excluir categorias Despesas
@app.callback(
    [
        Output('select_despesa', 'options'),
        Output('checklist-selected-style-despesa', 'options'),
        Output('checklist-selected-style-despesa', 'value'),
        Output('stored-cat-despesas', 'data'),
        Output('input-add-despesa', 'value')
    ],
    
    [
        Input('add-category-despesa', 'n_clicks'),
        Input('remove-category-despesa', 'n_clicks')
    ],
    
    [
        State('input-add-despesa', 'value'),
        State('checklist-selected-style-despesa', 'value'),
        State('stored-cat-despesas', 'data'),
        State("login-state", "data")
    ]
)
def dropdown_category_despesa(n, n2, nome_categoria, check_delete, cat_despesas, login_state):
       
    # user_info = session.get(login_state['session_id'])
    token = login_state.get('token', None)
    
    cat_despesa = list(cat_despesas['nome'].values())
    
    if n and not (nome_categoria == '' or nome_categoria == None):
        if nome_categoria not in cat_despesa:
            PostCategory(token, nome_categoria, 'despesa')
            cat_despesa.append(nome_categoria)
    
    if n2 and check_delete:
        for categoria in check_delete:
            if categoria in cat_despesa:
                DeleteCategory(token, categoria, 'despesa')
                cat_despesa.remove(categoria)
                
    #Atualizando opções para os componentes de saída    
    opt_despesa = [{'label': i, 'value': i} for i in cat_despesa]
    
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['nome'])
    
    data_return = df_cat_despesa.to_dict()
    
    return [opt_despesa, opt_despesa, [], data_return, '']

# Callback para abrir a janela de seleção de arquivo ao clicar no botão
@app.callback(Output('upload-image', 'style'),
              [Input('upload-button', 'n_clicks')])
def display_upload(n_clicks):
    if n_clicks is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback para exibir a imagem carregada
@app.callback(Output('uploaded-image', 'src'),
              [Input('upload-image', 'contents')])
def update_image(content):
    if content is not None:
        return content
    else:
        return 'assets/img/img_hom.png'
    
# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("botao_avatar", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Callback de logout    
@app.callback(
    Output('login-state', 'data'),
    
    Input("logout-btn", "n_clicks"),

    State("login-state", "data")
)
def handle_logout(n_clicks, login_state):
    if n_clicks and n_clicks > 0:
        
        token = login_state.get('token', None)
            
        logout_request = LogoutRequest(token)
        
        if logout_request == '200':
            new_login_state = {'login_status': 'error', 'token': '', 'message': ''}
            return new_login_state     
    else:
        return login_state
