from dash import html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app.components.api.my_budget_api import LoginRequest
from app.dash_app import *

card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
}

# =========  Layout  =========== #
def render_layout(message):
    login = dbc.Card([
                html.Legend("Login", style={"margin-bottom": "15px"}),
                dbc.Input(id="user_login", placeholder="Username", type="text", style={"margin-bottom": "15px"}),
                dbc.Input(id="pwd_login", placeholder="Password", type="password", style={"margin-bottom": "15px"}),
                dbc.Button("Login", id="login_button"),
                html.Span(message, style={"text-align": "center", "margin-top": "15px"}),
                
                html.Div([
                    dcc.Link("Registre-se", href="/register")
                ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

            ], style=card_style, className="align-self-center") 
    return login

#====================================================================#
    
# Callback que trata do login
@app.callback(
    Output('login-state', 'data', allow_duplicate=True),
    
    Input('login_button', 'n_clicks'), 
    
    [
        State('user_login', 'value'), 
        State('pwd_login', 'value')
    ]
)
def login_request(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate
    
    # Autenticação do usuário
    try:
        user_token = LoginRequest(username, password)
        
        if user_token:
            login_response = {'login_status': 'success', 'token': user_token, 'message': ''}
            
            return login_response
        else:
            login_response = {'login_status': 'error', 'token': '', 'message': 'Nome de usuário e/ou senha invalido(s)'}
            return login_response
            
    except Exception as error:
        print(error)
        return {'login_status': 'error', 'token': '', 'message': 'Internal error.'}