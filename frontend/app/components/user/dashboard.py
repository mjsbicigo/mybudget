from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from app.dash_app import *

# Definindo card_icon para padronizar o estilo dos cards 
card_icon = {
    'width': '55px', 
    'height': '55px',
    'margin': 'auto'
}

graph_margin = dict(l=25, r=25, t=25, b=0)


def render_layout():
    # Obtém o primeiro dia do mês atual
    start_date = datetime(datetime.today().year, datetime.today().month, 1)

    # Obtém o último dia do mês atual
    if datetime.now().month == 12:
        end_date = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(datetime.now().year, datetime.now().month + 1, 1) - timedelta(days=1)

    # =========  Layout  =========== #
    layout = dbc.Col([
        dbc.Row([
            # Receita
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Receitas"),
                        html.H5("R$ -", id="p-receita-dashboards"),
                        ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(html.Img(src='assets/img/money_up.png', style=card_icon), style={"display": "flex", "align-items": "center", "justify-content": "center", "height": "100%"}),
                        color="#17ff78",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                        )])
                ], width=4),
            
            # Despesa
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Despesas"),
                        html.H5("R$ -", id="p-despesa-dashboards"),
                        ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(html.Img(src='assets/img/money_down.png', style=card_icon), style={"display": "flex", "align-items": "center", "justify-content": "center", "height": "100%"}),
                        color="#ff4942",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                        )])
                ], width=4),
            
            # Saldo Total
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Saldo"),
                        html.H5("R$ -", id="p-saldo-dashboards", style={}),
                        ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(html.Img(src='assets/img/money_bank.png', style=card_icon), style={"display": "flex", "align-items": "center", "justify-content": "center", "height": "100%"}),
                        color="warning",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                        )])
                ], width=4)
            ], style={"margin": "10px"}),
        
        # Seção FILTRAR LANÇLAMENTOS
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Legend("Filtrar lançamentos", className="card-title"),
                    
                    # Categorias das Receitas
                    html.Label("Categorias das receitas"),
                    html.Div(
                        dcc.Dropdown(
                            id="dropdown-receita",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True)
                        ),
                    
                    # Categorias das Despesas
                    html.Label("Categorias das despesas", style={"margin-top": "10px"}),
                    dcc.Dropdown(
                        id="dropdown-despesa",
                        clearable=False,
                        style={"width": "100%"},
                        persistence=True,
                        persistence_type="session",
                        multi=True
                        ),
                    
                    # Datepicker de análise por período
                    html.Legend("Período de Análise", style={"margin-top": "10px"}),
                    dcc.DatePickerRange(
                        month_format='Do MMM, YY',
                        end_date_placeholder_text='Data...',
                        start_date=start_date,
                        end_date=end_date,
                        display_format='DD-MM-YYYY',
                        with_portal=True,
                        updatemode='singledate',
                        id='date-picker-config',
                        style={'z-index': '100'})
                ], style={"height": "100%", "padding": "20px"}),
                
            ], width=4),
            
            dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px"}), width=8),
            
        ], style={"margin": "10px"}),

        #Gráficos parte inferior
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}), width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}), width=3),
        ], style={"margin": "10px"})

    ])
    
    return layout

# =========  Callbacks  =========== #

# Valor total receitas
@app.callback(
    [
        Output('dropdown-receita', 'options'),
        Output('dropdown-receita', 'value'),
        Output('p-receita-dashboards', 'children')
    ], 
    [
        Input('store-receitas', 'data')
    ]
)
def populate_dropdown_receitas(data):
    
    df = pd.DataFrame(data)
    
    valor = df['valor'].sum()
    
    val = df['categoria'].unique().tolist()
    
    return ([{'label': x, 'value': x} for x in val], val, f'R$ {valor}')

# Valor total despesas
@app.callback(
    [
        Output('dropdown-despesa', 'options'),
        Output('dropdown-despesa', 'value'),
        Output('p-despesa-dashboards', 'children')
    ], 
    [
        Input('store-despesas', 'data')
    ]
)
def populate_dropdown_despesas(data):
    
    df = pd.DataFrame(data)
    
    valor = df['valor'].sum()
    
    val = df['categoria'].unique().tolist()
    
    return ([{'label': x, 'value': x} for x in val], val, f'R$ {valor}')

# Valor Saldo total
@app.callback(
    Output("p-saldo-dashboards", "children"),
    
    [
        Input("store-despesas", "data"),
        Input("store-receitas", "data")
    ]
)
def saldo_total(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)

    valor = df_receitas['valor'].sum() - df_despesas['valor'].sum()

    return f"R$ {valor}"

#  Gráfico 1
@app.callback(
    
    Output('graph1', 'figure'),
    
    [
        Input('store-despesas', 'data'),
        Input('store-receitas', 'data'),
        Input("dropdown-despesa", "value"),
        Input("dropdown-receita", "value")
    ]
)
def update_output(data_despesa, data_receita, despesa, receita):
    df_despesas = pd.DataFrame(data_despesa).set_index('data')[['valor']]
    df_ds = df_despesas.groupby('data').sum().rename(columns={'valor': 'Despesa'})
    
    df_receita = pd.DataFrame(data_receita).set_index('data')[['valor']]
    df_rc = df_receita.groupby('data').sum().rename(columns={'valor': 'Receita'})
    
    df_acum = df_ds.join(df_rc, how='outer').fillna(0)
    df_acum['Acum'] = df_acum['Receita'] - df_acum['Despesa']
    df_acum['Acum'] = df_acum['Acum'].cumsum()
    
    # Montando o gráfico
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Fluxo de caixa', x=df_acum.index, y=df_acum['Acum'], mode='lines'))
    
    
    fig.update_layout(margin=graph_margin, title='Receitas x Despesas', height=370)
    fig.update_layout(title={'font': {'color': 'white',
                                      'size': 15,
                                      'family': 'Arial, sans-serif',
                                      'weight': 'bold'}
                             })
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig

#  Gráfico 2
@app.callback(
    
    Output('graph2', 'figure'),
    
    [
        Input('store-receitas', 'data'),
        Input('store-despesas', 'data'),
        Input('dropdown-receita', 'value'),
        Input('dropdown-despesa', 'value'),
        Input('date-picker-config', 'start_date'),
        Input('date-picker-config', 'end_date')
    ]   
)
def graph2_show(data_receita, data_despesa, receita, despesa, start_date, end_date):
    
    df_rc = pd.DataFrame(data_receita)
    df_ds = pd.DataFrame(data_despesa)
    
    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    
    df_final = pd.concat([df_ds, df_rc])
    
    df_final['data'] = pd.to_datetime(df_final['data'])
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_final = df_final[(df_final['data'] >= start_date) & (df_final['data'] <= end_date)]
    df_final = df_final[(df_final['categoria'].isin(receita) | (df_final['categoria'].isin(despesa)))]
    
    fig = px.bar(df_final, x="data", y="valor", 
                 color='Output', barmode="group", 
                 title="Receitas e Despesas por período", 
                 color_discrete_map={'Receitas': '#17ff78', 'Despesas': '#d12828'})
    
    fig.update_layout(title={'font': {'color': 'white',
                                      'size': 15,
                                      'family': 'Arial, sans-serif',
                                      'weight': 'bold'},
                             'x': 0.5})
    fig.update_layout(margin=graph_margin, height=370)
    fig.update_layout(legend_title_text = "Legenda")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig

#  Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    
    [
        Input('store-receitas', 'data'),
        Input('dropdown-receita', 'value')
    ]
)
def pie_receita(data_receita, receita):
    df = pd.DataFrame(data_receita)
    
    df = df[df['categoria'].isin(receita)]

    fig = px.pie(df, values=df['valor'], names=df['categoria'], hole=.2)
    
    fig.update_layout(title={'text': "Receitas por categoria (%)",
                             'font': {'color': 'white',
                                      'size': 15,
                                      'family': 'Arial, sans-serif',
                                      'weight': 'bold'},
                             'x': 0.5})
    
    fig.update_layout(margin=graph_margin, height=370)
    fig.update_layout(legend_title_text = "Legenda")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                  
    return fig  

#  Gráfico 4
@app.callback(
    Output('graph4', "figure"),
    [
        Input('store-despesas', 'data'),
        Input('dropdown-despesa', 'value')
    ]
)
def pie_despesa(data_despesa, despesa):
    df = pd.DataFrame(data_despesa)
    df = df[df['categoria'].isin(despesa)]

    fig = px.pie(df, values=df['valor'], names=df['categoria'], hole=.2)
    fig.update_layout(title={'text': "Despesas por categoria (%)",
                             'font': {'color': 'white',
                                      'size': 15,
                                      'family': 'Arial, sans-serif',
                                      'weight': 'bold'},
                             'x': 0.5})
    
    fig.update_layout(margin=graph_margin, height=370)
    fig.update_layout(legend_title_text = "Legenda")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig