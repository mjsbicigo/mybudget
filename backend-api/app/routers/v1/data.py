from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.data import PostReceive, PostExpense
from dependencies.database_requests import get_user_database_connection, insert_log
from config import settings
import jwt

router = APIRouter()

def extract_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = auth_header.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token, missing username")
        
        return username
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/api/v1/receives")
def load_receives(request: Request):
    username = extract_token(request)
    user_db = get_user_database_connection(username)
    
    receives = list(user_db['receitas'].find({}, {'_id': 0}))
    for receive in receives:
        if 'data' in receive:
            receive['data'] = receive['data'].strftime('%Y-%m-%d %H:%M:%S')
    
    return JSONResponse(content={"Content": receives})

@router.post("/api/v1/receives")
def post_data_receives(request: Request, postReceiveRequest: PostReceive):
    username = extract_token(request)
    user_db = get_user_database_connection(username)

    receive = {
        'valor': int(postReceiveRequest.valor),
        'recebido': bool(postReceiveRequest.recebido),
        'fixo': bool(postReceiveRequest.fixo),
        'data': postReceiveRequest.data,
        'categoria': postReceiveRequest.categoria,
        'descricao': postReceiveRequest.descricao
    }

    try:
        user_db['receitas'].insert_one(receive)
        insert_log(f'Inserted receive', 'log_operations', f'mb_{username}')
        return JSONResponse(content={"Content": "Success: Receive successfully added."})
    except Exception as error:
        print(f'Internal Error: {error}')
        raise HTTPException(status_code=500, detail="Internal error: The record could not be inserted into the database.")

@router.get("/api/v1/expenses")
def load_expenses(request: Request):
    username = extract_token(request)
    user_db = get_user_database_connection(username)
    
    expenses = list(user_db['despesas'].find({}, {'_id': 0}))
    for expense in expenses:
        if 'data' in expense:
            expense['data'] = expense['data'].strftime('%Y-%m-%d %H:%M:%S')
    
    return JSONResponse(content={"Content": expenses})

@router.post("/api/v1/expenses")
def post_data_expenses(request: Request, postExpenseRequest: PostExpense):
    username = extract_token(request)
    user_db = get_user_database_connection(username)

    expense = {
        'valor': int(postExpenseRequest.valor),
        'recebido': bool(postExpenseRequest.recebido),
        'fixo': bool(postExpenseRequest.fixo),
        'data': postExpenseRequest.data,
        'categoria': postExpenseRequest.categoria,
        'descricao': postExpenseRequest.descricao
    }

    try:
        user_db['despesas'].insert_one(expense)
        insert_log(f'Inserted expense', 'log_operations', f'mb_{username}')
        return JSONResponse(content={"Content": "Success: Expense successfully added."})
    except Exception as error:
        print(f'Internal Error: {error}')
        raise HTTPException(status_code=500, detail="Internal error: The record could not be inserted into the database.")



