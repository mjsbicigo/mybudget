from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from models.authentication import LoginRequest
from dependencies.database_requests import get_users_collection
from passlib.context import CryptContext
from config import settings
import jwt
import uuid

router = APIRouter()
redis_client = settings.redis_client

@router.post("/api/v1/login")
async def login(request: LoginRequest):
    
    user = get_users_collection().find_one({"username": request.username})
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Verificando se o usuário existe no banco de dados ou se a senha está incorreta
    # if not user or not verify_password(request.password, user['password']):
    if not user or not pwd_context.verify(request.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    else:
        try:
            session_id = str(uuid.uuid4())
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            expire_time = (datetime.now() + timedelta(hours=4)).strftime('%Y-%m-%d %H:%M:%S')

            # Gera os dados contidos no token de retorno
            user_data = {
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "session_id": session_id
            }
            
            try:              
                # Cria o token jwt
                token = jwt.encode(user_data, settings.SECRET_KEY, algorithm="HS256")

                # Armazenar a sessão no Redis
                redis_key = f'session:{session_id}'
                redis_client.hset(redis_key, mapping={
                    'username': user["username"],
                    "email": user["email"],
                    "full_name": user["full_name"],
                    'login_time': current_time,
                    'expire_time': expire_time
                })
                
                expire_timestamp = int(datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S').timestamp())
                redis_client.expireat(redis_key, expire_timestamp)
            
            except Exception as redis_error:
                print(f'Redis error: {redis_error}')
                raise HTTPException(status_code=500, detail="Failed to store session.")
                
            # Atualiza o último login do usuário no banco de dados
            get_users_collection().update_one({"_id": ObjectId(user["_id"])}, {"$set": {"last_login": current_time}})
                    
            # Retorna o token
            return JSONResponse(content={"Status": "Successful login", "access_token": token})

        except Exception as error:
            print(f'Authentication route error: {error}')
            raise HTTPException(status_code=500, detail="Internal error from authentication route.")

# Rota que verifica se a sessão do usuário é válida
# @router.get('/api/v1/session')
# async def register(request: SessionStatusRequest):
#     session = verify_session(request.username, request.session_id)
    
#     if session:
#         return JSONResponse(content={"Status": "Valid session."})
#     else:
#         raise HTTPException(status_code=401, detail="Invalid session or expired.")
    
    
# @app.get("/secure-data")
# async def secure_data(token: str):
#     decoded_token = verify_token(token)
#     session_id = decoded_token['session_id']
#     if redis_client.exists(session_id):
#         return {"secure_data": "Here is your secure data"}
#     raise HTTPException(status_code=401, detail="Invalid session")