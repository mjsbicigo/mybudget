from dash.dependencies import Input, Output
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from app.dash_app import *

graph_margin = dict(l=25, r=25, t=25, b=0)

def render_layout():
    # =========  Layout  =========== #
    layout = dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H4('Total de despesas', style={'text-align': 'center'}),
                        html.Legend('R$ -', id='valor_despesa_card', style={'font-size': '60px', 'text-align': 'center'})
                    ], style={'text-align': 'center', 'padding-top': '30px'})
                )
            ], width=12)
        ]),
        dbc.Row([
            html.Div(id='tabela-despesas', className='dbc', style={"margin-top": "10px"})
        ], style={'flex': '1 0 auto'}),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar-graph-despesas', style={'margin-right': '20px'})
            ], width=12)
        ], style={'flex': '1 0 auto', 'margin-top': 'auto'})
    ], style={'display': 'flex', 'flex-direction': 'column', 'height': '100vh', 'padding': '10px'})

    return layout

# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('tabela-despesas', 'children'),
    Input('store-despesas', 'data')
)
def imprimir_tabela(data):
    if not data:
        return html.Div("Nenhuma despesa encontrada.")

    df = pd.DataFrame(data)

    # Verificar se as colunas esperadas existem
    expected_columns = ['data', 'recebido', 'fixo', 'valor', 'categoria', 'descricao']
    for col in expected_columns:
        if col not in df.columns:
            return html.Div(f"Coluna ausente: {col}")

    df['data'] = pd.to_datetime(df['data']).dt.date
    df['recebido'] = df['recebido'].astype(str).map({'0': 'Não', '1': 'Sim'})
    df['fixo'] = df['fixo'].astype(str).map({'0': 'Não', '1': 'Sim'})

    df = df.fillna('-')
    df['data'] = pd.to_datetime(df['data']).dt.strftime('%d-%m-%Y')
    df.sort_values(by='data', ascending=True, inplace=True)

    order_columns = ['descricao', 'categoria', 'data', 'valor', 'recebido', 'fixo']

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False} for i in order_columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_header={'text-align': 'center'},
        style_cell={
            'textAlign': 'center',
            'padding': '5px'
        }
    )

    return tabela

# Bar Graph
@app.callback(
    Output('bar-graph-despesas', 'figure'),
    Input('store-despesas', 'data')
)
def bar_chart(data):
    if not data:
        return px.bar(title="Nenhuma despesa encontrada.")

    df = pd.DataFrame(data)
    df_grouped = df.groupby("categoria").sum()[["valor"]].reset_index()

    graph = px.bar(df_grouped, 
                   x='categoria', 
                   y='valor',
                   title='Distribuição das Despesas'
                   )
    
    graph.update_layout(
        title={
            'text': 'Distribuição das Despesas',
            'font': {
                'color': 'white',
                'size': 18,
                'family': 'Arial, sans-serif',
                'weight': 'bold'
            },
            'x': 0.5
        },
        margin=graph_margin,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    graph.update_traces(marker_color='#d12828')

    return graph

# Simple card
@app.callback(
    Output('valor_despesa_card', 'children'),
    Input('store-despesas', 'data')
)
def display_despesas(data):
    if not data:
        return "R$ 0.00"

    df = pd.DataFrame(data)
    valor = df['valor'].sum()

    return f"R$ {valor:.2f}"
