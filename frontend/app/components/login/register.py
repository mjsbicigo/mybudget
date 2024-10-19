from dash import html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app.components.api.my_budget_api import RegisterRequest
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
    message = message if message != '' else ''

    layout = dbc.Card([
                html.Legend("Registrar"),
                dbc.Input(id="user_full_name", placeholder="Nome Completo", type="text", style={"margin-bottom": "10px"}),
                dbc.Input(id="email_register", placeholder="E-mail", type="email", style={"margin-bottom": "10px"}),
                dbc.Input(id="user_register", placeholder="Username", type="text", style={"margin-bottom": "10px"}),
                dbc.Input(id="pwd_register", placeholder="Senha", type="password", style={"margin-bottom": "10px"}),
                dbc.Button("Registrar", id='register-button'),
                html.Span(message, style={"text-align": "center"}),

                html.Div([
                    html.Label("Ou ", style={"margin-right": "5px"}),
                    dcc.Link("faça login", href="/login"),
                ], style={"padding": "20px", "justify-content": "center", "display": "flex"})

            ], style=card_style, className="align-self-center")
    return layout

# =========  Callbacks Page1  =========== #
@app.callback(
    Output('register-state', 'data'),
    Input('register-button', 'n_clicks'), 

    [
        State('user_full_name', 'value'),
        State('user_register', 'value'), 
        State('pwd_register', 'value'),
        State('email_register', 'value')
    ]
    )
def register(n_clicks, user_full_name, username, password, email):
    if n_clicks == None:
        raise PreventUpdate

    if user_full_name is not None and username is not None and password is not None and email is not None:
        register_request = RegisterRequest(username, user_full_name, email, password)
        return register_request
    else:
        return 'error'