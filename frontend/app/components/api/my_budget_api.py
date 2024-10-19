import datetime
import pandas as pd
from pymongo import MongoClient
import requests
from base64 import b64encode
from app.config import Settings

def insert_log(event: str, collection='log_mybudget', database_name="MyBudget"):
    try:
        client = MongoClient(Settings.MONGO_URI)
        db = client[database_name]
        
        app_log = db[collection]
        datetime_log = datetime.datetime.now()
        log = {'Evento': event, 'timestamp': datetime_log}
        app_log.insert_one(log)
    
    except requests.exceptions.RequestException as request_exception:
        print(f'Error inserting log: {request_exception}')

def RegisterRequest(username: str, user_full_name: str, email: str, password: str):
    try:
        register_endpoint = f'{Settings.API_URI}/api/v1/register'
        
        payload = {
            'username': username,
            'full_name': user_full_name,
            'email': email,
            'password': password
        }
        
        api_response = requests.post(register_endpoint, json=payload)
        
        if api_response.status_code == 200:
            return 'success'
            
        elif api_response.status_code == 400:
            return api_response.json().get('detail')
        
        else:
            return 'error'
        
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Register error: {request_exception}')
        print(f'Register error: {request_exception}')

def LoginRequest(username: str, password: str):
    try:
        
        login_endpoint = f'{Settings.API_URI}/api/v1/login'
        
        # Codificação das credenciais em Base64 para o cabeçalho de autenticação
        credentials = f'{username}:{password}'.encode('utf-8')
        credentials_base64 = b64encode(credentials).decode('utf-8')
        
        # Cabeçalho de autorização com credenciais básicas
        headers = {'Authorization': f'Basic {credentials_base64}'}
        
        # Payload com os dados do usuário
        payload = {
            'username': username,
            'password': password
            }
        
        # Chamada para a API de login
        api_response = requests.post(login_endpoint, headers=headers, json=payload)
        
        if api_response.status_code == 200:
            token = api_response.json().get('access_token')
            if token:
                return token
        return None
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Login error: {request_exception}')
        print(f'Login error: {request_exception}')
    
def LogoutRequest(token: str):
    try:
        logout_endpoint = f'{Settings.API_URI}/api/v1/logout'
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        api_response = requests.post(logout_endpoint, headers=headers)
        
        if api_response.status_code == 200:
            return '200'
        else:
            return None
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Logout error: {request_exception}')
        print(f'Logout error: {request_exception}')

def GetReceives(token: str):
    df_receitas = None
    try:
        get_receives_endpoint = f'{Settings.API_URI}/api/v1/receives'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        api_response = requests.get(get_receives_endpoint, headers=headers)
        
        if api_response.status_code == 200:
            data = api_response.json().get('Content')
            df_receitas = pd.DataFrame(data)
            
            if 'data' in df_receitas.columns:
                df_receitas['data'] = pd.to_datetime(df_receitas['data'])
                df_receitas['data'] = df_receitas['data'].dt.date
                
                df_receitas = df_receitas[df_receitas['descricao'] != '*transacao-inicial*']
            return df_receitas
        
        if api_response.status_code == 401:
            df_receitas = str(401)
            return df_receitas
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Get receives error: {request_exception}')
        print(f'Get receives error: {request_exception}')

def GetExpenses(token: str):
    df_despesas = None
    try:
        get_expenses_endpoint = f'{Settings.API_URI}/api/v1/expenses'
        headers = {
            'Authorization': f'Bearer {token}'
        }
    
        api_response = requests.get(get_expenses_endpoint, headers=headers)
        
        if api_response.status_code == 200:
            data = api_response.json().get('Content')
            df_despesas = pd.DataFrame(data)
            
            if 'data' in df_despesas.columns:
                df_despesas['data'] = pd.to_datetime(df_despesas['data'])
                df_despesas['data'] = df_despesas['data'].dt.date
                
                df_despesas = df_despesas[df_despesas['descricao'] != '*transacao-inicial*']
            return df_despesas
        if api_response.status_code == 401:
            df_despesas = str(401)
            return df_despesas
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Get expenses error: {request_exception}')
        print(f'Get expenses error: {request_exception}')

def PostReceive(token: str, valor: float, recebido: bool, fixo: bool, data: datetime, categoria: str, descricao: str):
    response = None
    try:
        post_receive_endpoint = f'{Settings.API_URI}/api/v1/receives'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        payload = {
            'valor': valor, 
            'recebido': recebido, 
            'fixo': fixo, 
            'data': data,
            'categoria': categoria, 
            'descricao': descricao
        }
        api_response = requests.post(post_receive_endpoint, headers=headers, json=payload)

        if api_response.status_code == 200:
            response = str(200)
            return response
        if api_response.status_code == 401:
            response = str(401)
            return response
        return response
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Post receive error: {request_exception}')
        print(f'Post receive error: {request_exception}')
        
def PostExpense(token: str, valor: float, recebido: bool, fixo: bool, data: datetime, categoria: str, descricao: str):
    response = None
    try:
        post_expense_endpoint = f'{Settings.API_URI}/api/v1/expenses'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        payload = {
            'valor': valor, 
            'recebido': recebido, 
            'fixo': fixo, 
            'data': data,
            'categoria': categoria, 
            'descricao': descricao
        }
        api_response = requests.post(post_expense_endpoint, headers=headers, json=payload)
        
        if api_response.status_code == 200:
            response = str(200)
            return response
        if api_response.status_code == 401:
            response = str(401)
            return response
        return response
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Post expense error: {request_exception}')
        print(f'Post expense error: {request_exception}')

def GetCategories(token: str, tipo_categoria: str):
    df_categorias = None
    try:
        get_categories_endpoint = f'{Settings.API_URI}/api/v1/categories'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        payload = {
            "tipo_categoria": tipo_categoria
        }
        
        api_response = requests.get(get_categories_endpoint, headers=headers, json=payload)
        
        if api_response.status_code == 200:
            dados = api_response.json().get('Content')
            df_categorias = pd.DataFrame(dados)
            return df_categorias
        else:
            return df_categorias
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Get categories error: {request_exception}')
        print(f'Get categories error: {request_exception}')
    
def PostCategory(token: str, nome_categoria: str, tipo_categoria: str):
    response = None
    try:
        post_category_endpoint = f'{Settings.API_URI}/api/v1/categories'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        payload = {
            "nome_categoria": nome_categoria,
            "tipo_categoria": tipo_categoria
        }
        
        api_response = requests.post(post_category_endpoint, headers=headers, json=payload)
        
        if api_response.status_code == 200:
            response = str(200)
            return response
        else:
            return response
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Post category error: {request_exception}')
        print(f'Post category error: {request_exception}')

def DeleteCategory(token: str, nome_categoria: str, tipo_categoria: str):
    response = None
    try:
        delete_category_endpoint = f'{Settings.API_URI}/api/v1/categories'
        
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        payload = {
            "nome_categoria": nome_categoria,
            "tipo_categoria": tipo_categoria
        }
        
        api_response = requests.delete(delete_category_endpoint, headers=headers, json=payload)
        
        if api_response.status_code == 200:
            response = str(200)
            return response
        else:       
            return response
    except requests.exceptions.RequestException as request_exception:
        insert_log(f'Delete category error: {request_exception}')
        print(f'Delete category error: {request_exception}')
        
# def SessionStatus(username: str, session_id: str):
#     response = None
    
#     try:
#         session_status_endpoint = f'{Settings.API_URI}/api/v1/session'
        
#         payload = {
#             "username": username,
#             "session_id": session_id
#         }
        
#         api_response = requests.get(session_status_endpoint, json=payload)
        
#         if api_response.status_code == 200:
#             response = str(200)
#             return response
        
#         if api_response.status_code == 401:
#             response = str(401)
#             return response
        
#         return response
#     except requests.exceptions.RequestException as request_exception:
#         insert_log(f'Get session status error: {request_exception}')
#         print(f'Get session status error: {request_exception}')