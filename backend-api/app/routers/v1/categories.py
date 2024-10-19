from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from models.categories import *
from dependencies.database_requests import get_user_database_connection, insert_log
from config import settings
import jwt

router = APIRouter()

# Função auxiliar para obter o username do token JWT
def get_username_from_token(auth_header: str):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    token = auth_header.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token: Missing username")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/api/v1/categories")
async def load_categories(getCategoriesRequest: GetCategories, request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        username = get_username_from_token(auth_header)
        
        user_db = get_user_database_connection(username)
        
        if getCategoriesRequest.tipo_categoria == 'receita':
            categories = list(user_db['categorias_receita'].find({}, {'_id': 0, 'nome': 1}))
            return JSONResponse(content={"Content": categories})

        if getCategoriesRequest.tipo_categoria == 'despesa':
            categories = list(user_db['categorias_despesa'].find({}, {'_id': 0, 'nome': 1}))
            return JSONResponse(content={"Content": categories})
    
    except Exception as error:
        print(f'getCategories route error: {error}')
        raise HTTPException(status_code=500, detail="Internal error in the getCategories route.")
    
@router.post("/api/v1/categories")
async def insert_category(postCategoriesRequest: PostCategory, request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        username = get_username_from_token(auth_header)
        
        user_db = get_user_database_connection(username)
    except Exception as error:
        print(f'postCategories route error: {error}')
        raise HTTPException(status_code=500, detail="Internal error in the postCategories route.")
        
    if postCategoriesRequest.tipo_categoria == 'receita':
        existing_category = user_db['categorias_receita'].find_one({'nome': postCategoriesRequest.nome_categoria})
            
        if not existing_category:
            user_db['categorias_receita'].insert_one({'nome': postCategoriesRequest.nome_categoria})
            insert_log(f'Added receive category: {postCategoriesRequest.nome_categoria}', 'log_operacoes', f'mb_{username}')
                
            return JSONResponse(content={"Content": "Success: Income category successfully added."})
        else:
            raise HTTPException(status_code=409, detail="Conflict: Income category already exists.")

    if postCategoriesRequest.tipo_categoria == 'despesa':
        existing_category = user_db['categorias_despesa'].find_one({'nome': postCategoriesRequest.nome_categoria})
            
        if not existing_category:
            user_db['categorias_despesa'].insert_one({'nome': postCategoriesRequest.nome_categoria})
            insert_log(f'Added expense category: {postCategoriesRequest.nome_categoria}', 'log_operacoes', f'mb_{username}')
                
            return JSONResponse(content={"Content": "Success: Expense category successfully added."})
        else:
            raise HTTPException(status_code=409, detail="Conflict: Expense category already exists.")
    
@router.delete("/api/v1/categories")
async def remove_category(deleteCategoryRequest: DeleteCategory, request: Request):
    try:
        auth_header = request.headers.get("Authorization")
        username = get_username_from_token(auth_header)
    except Exception as error:
        print(f'removeCategory route error: {error}')
        raise HTTPException(status_code=500, detail="Error: {error}")
        
    user_db = get_user_database_connection(username)
        
    if deleteCategoryRequest.tipo_categoria == 'receita':
        existing_category = user_db['categorias_receita'].find_one({'nome': deleteCategoryRequest.nome_categoria})
            
        if existing_category:
            user_db['categorias_receita'].delete_one({'nome': deleteCategoryRequest.nome_categoria})
            insert_log(f'Deleted receive category: {deleteCategoryRequest.nome_categoria}', 'log_operacoes', f'mb_{username}')
                
            return JSONResponse(content={"Content": "Income category successfully removed."})
        else:
            raise HTTPException(status_code=404, detail="Not found: Income category does not exist.")

    if deleteCategoryRequest.tipo_categoria == 'despesa':
        existing_category = user_db['categorias_despesa'].find_one({'nome': deleteCategoryRequest.nome_categoria})
            
        if existing_category:
            user_db['categorias_despesa'].delete_one({'nome': deleteCategoryRequest.nome_categoria})
            insert_log(f'Deleted expense category: {deleteCategoryRequest.nome_categoria}', 'log_operations', f'mb_{username}')
                
            return JSONResponse(content={"Content": "Expense category successfully removed."})
        else:
            raise HTTPException(status_code=404, detail="Not found: Expense category does not exist.")
    
    
