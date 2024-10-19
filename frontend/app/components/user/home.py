from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app.dash_app import *
from app.components.user import sidebar, dashboard, extratos_receitas, extratos_despesas
from app.components.api.my_budget_api import GetCategories, GetReceives, GetExpenses

# =========  Layout  =========== #
def render_layout(token: str, user_info: dict):
    
    # username = user_info['username']
    # session_id = user_info['session_id']

    # Carregando receitas, despesas e categorias de receitas/despesas
    df_receitas  = GetReceives(token)
    df_despesas  = GetExpenses(token)  
    cat_receitas = GetCategories(token, 'receita')
    cat_despesas = GetCategories(token, 'despesa')

    layout = dbc.Container(children=[
        dcc.Store(id='store-receitas', data=df_receitas.to_dict()),
        dcc.Store(id='store-despesas', data=df_despesas.to_dict()),
        dcc.Store(id='stored-cat-receitas', data=cat_receitas.to_dict()),
        dcc.Store(id='stored-cat-despesas', data=cat_despesas.to_dict()),
        
        dbc.Row([
            dbc.Col([
                sidebar.render_layout(user_info, cat_receitas, cat_despesas)
            ], md=2),

            dbc.Col([
                html.Div(id="page-content-app")
            ], md=10),
        ])

    ], fluid=True, style={"padding": "0px"}, className="dbc")
    
    app.title = "Home - myBudget"
    
    return layout

@app.callback(
    Output("page-content-app", "children"), 
    
    [Input("app-url", "data")],
)
def render_app_content(endpoint):
       
    if endpoint == '/dashboard':
        return dashboard.render_layout()

    if endpoint == "/extratos-receitas":
        return extratos_receitas.render_layout()
    
    if endpoint == "/extratos-despesas":
        return extratos_despesas.render_layout()
    
    else:
        return html.Div("Página não encontrada")