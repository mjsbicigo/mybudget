import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app.dash_app import *
from app.components.user import home
from app.components.login import login, register
import jwt

# =========  Layout  =========== #
app.layout = html.Div(children=[
                dbc.Row([
                        dbc.Col([
                            dcc.Location(id="base-url", refresh=False),
                            dcc.Store(id="app-url", data='', storage_type='session'), 
                            dcc.Store(id="login-state", data={'login_status': 'error', 'token': '', 'message': ''}, storage_type='local'),
                            dcc.Store(id="register-state", data=""),
                            
                            html.Div(id="page-content", style={"height": "100vh", "display": "flex", "justify-content": "center"})
                        ]),
                    ])
            ], style={"padding": "0px"})

# =========  Callbacks  =========== #   

@app.callback(
                Output("base-url", "pathname"), 
            [
                Input("login-state", "data"),
                Input("register-state", "data")
            ]
            )
def redirect_login(login_state, register_state):
    
    ctx = dash.callback_context
    
    login_status = login_state.get('login_status', 'error')
    
    if ctx.triggered:
        trigg_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigg_id == 'login-state':
            return '/home' if login_status == "success" else '/login'
        
        elif trigg_id == 'register-state':
            if register_state == 'success':
                return '/login'
            else:
                return '/register'
    else:
        return '/login'

@app.callback(
                [Output("page-content", "children"),
                 Output("app-url", "data")],
                
                Input("base-url", "pathname"),
                
                [
                State("login-state", "data"),
                State("register-state", "data")
                ]
)
def render_page_content(pathname: str, login_state, register_state):
    
    token = login_state.get('token', None)
    message = login_state.get('message', None)
    
    if token:
        user_info = jwt.decode(token, flask_server.config['SECRET_KEY'], algorithms=['HS256'])
    
    app_endpoints = ['/home', '/dashboard', '/extratos-receitas', '/extratos-despesas']
        
    if pathname == '/register':
        return register.render_layout(register_state), '/register'
    
    if message:
        return login.render_layout(message), '/login'
    
    elif pathname == '/' or pathname == '/login':
        if token:
            return home.render_layout(token, user_info), '/dashboard'
        else:
            return login.render_layout(''), '/login'
    
    elif pathname in app_endpoints:
        if token:
            # session_status = SessionStatus(user_info['username'], user_info['session_id'])

            if pathname == '/home' or pathname == '/dashboard':
                return home.render_layout(token, user_info), '/dashboard'
                
            elif pathname == '/extratos-receitas':
                return home.render_layout(token, user_info), '/extratos-receitas'
                
            elif pathname == '/extratos-despesas':
                return home.render_layout(token, user_info), '/extratos-despesas'
                
            return login.render_layout('Página inacessível ou sessão expirada, tente um novo login.'), '/login'
        else:
            return login.render_layout('Faça login para acessar essa página.'), '/login'
    else:
        return html.Div("Página não encontrada"), '/login'
    
if __name__ == '__main__':
    app.run_server(port=8080, host='0.0.0.0', debug=False)